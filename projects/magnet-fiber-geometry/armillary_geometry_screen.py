#!/usr/bin/env python3
"""Stage-1A magnetic armillary geometry screen.

This is a quasi-static Biot-Savart comparison, not a levitation or thermal model.
It compares independently driven circular coils at an equal sum(I^2) proxy and
reports spatial-field and sensor-observability metrics.
"""

import json
import math

MU0_OVER_4PI = 1e-7


def add(a, b): return tuple(x + y for x, y in zip(a, b))
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def scale(a, s): return tuple(x * s for x in a)
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def norm(a): return math.sqrt(dot(a, a))
def unit(a):
    n = norm(a)
    return scale(a, 1.0/n)


def basis(normal):
    n = unit(normal)
    trial = (1.0, 0.0, 0.0) if abs(n[0]) < 0.8 else (0.0, 1.0, 0.0)
    u = unit(cross(n, trial))
    return u, cross(n, u)


def loop_segments(normal, radius=0.05, center=(0.0, 0.0, 0.0), pieces=180):
    u, v = basis(normal)
    points = []
    for k in range(pieces + 1):
        a = 2 * math.pi * k / pieces
        points.append(add(center, add(scale(u, radius*math.cos(a)), scale(v, radius*math.sin(a)))))
    return [(points[k], points[k+1]) for k in range(pieces)]


def field_from_loop(point, segments, current=1.0):
    out = (0.0, 0.0, 0.0)
    for p0, p1 in segments:
        dl = sub(p1, p0)
        mid = scale(add(p0, p1), 0.5)
        r = sub(point, mid)
        rn = norm(r)
        if rn < 1e-8:
            continue
        out = add(out, scale(cross(dl, r), MU0_OVER_4PI * current / rn**3))
    return out


def jacobi_eigenvalues(a, rounds=80):
    a = [row[:] for row in a]
    n = len(a)
    for _ in range(rounds):
        p, q = max(((i, j) for i in range(n) for j in range(i+1, n)), key=lambda ij: abs(a[ij[0]][ij[1]]))
        if abs(a[p][q]) < 1e-14:
            break
        phi = 0.5 * math.atan2(2*a[p][q], a[q][q]-a[p][p])
        c, s = math.cos(phi), math.sin(phi)
        for k in range(n):
            if k not in (p, q):
                apk, aqk = a[p][k], a[q][k]
                a[p][k] = a[k][p] = c*apk - s*aqk
                a[q][k] = a[k][q] = s*apk + c*aqk
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        a[p][p] = c*c*app - 2*s*c*apq + s*s*aqq
        a[q][q] = s*s*app + 2*s*c*apq + c*c*aqq
        a[p][q] = a[q][p] = 0.0
    return sorted(a[i][i] for i in range(n))


def observability(loops, sensors):
    cols = []
    for loop in loops:
        col = []
        for p in sensors:
            col.extend(field_from_loop(p, loop, 1.0))
        n = math.sqrt(sum(x*x for x in col))
        cols.append([x/n for x in col])
    gram = [[sum(cols[i][k]*cols[j][k] for k in range(len(cols[0]))) for j in range(len(cols))] for i in range(len(cols))]
    eig = jacobi_eigenvalues(gram)
    return {
        "normalized_condition_number": math.sqrt(eig[-1] / eig[0]) if eig[0] > 1e-12 else None,
        "gram_eigenvalues": eig,
    }


def currents(phases, t):
    raw = [math.cos(t+p) for p in phases]
    n = math.sqrt(sum(x*x for x in raw))
    return [x/n for x in raw]


def evaluate(name, normals, centers, phases):
    loops = [loop_segments(n, center=c) for n, c in zip(normals, centers)]
    sensors = [(0.07,0,0), (0,0.07,0), (0,0,0.07), (0.045,0.045,0.045)]
    path = [(0.075*math.cos(a), 0.075*math.sin(a), 0.03) for a in [2*math.pi*k/144 for k in range(144)]]
    obs = observability(loops, sensors)
    rms_values, min_values, direction_variations, signed_integrals = [], [], [], []
    for step in range(24):
        amps = currents(phases, 2*math.pi*step/24 + 0.17)
        fields = []
        for p in path:
            b = (0.0,0.0,0.0)
            for loop, amp in zip(loops, amps): b = add(b, field_from_loop(p, loop, amp))
            fields.append(b)
        mags = [norm(b) for b in fields]
        rms_values.append(math.sqrt(sum(m*m for m in mags)/len(mags)))
        min_values.append(min(mags))
        variation = 0.0
        for a, b in zip(fields, fields[1:]+fields[:1]):
            if norm(a) > 1e-12 and norm(b) > 1e-12:
                variation += math.acos(max(-1.0, min(1.0, dot(a,b)/(norm(a)*norm(b)))))
        direction_variations.append(variation)
        signed = 0.0
        for k, b in enumerate(fields):
            a = 2*math.pi*k/len(fields)
            tangent = (-math.sin(a), math.cos(a), 0.0)
            signed += dot(b, tangent)/len(fields)
        signed_integrals.append(signed)
    return {
        "configuration": name,
        "coils": len(loops),
        "equal_drive_proxy": "sum(I^2)=1 at every phase",
        "sensor_observability": obs,
        "closed_path_metrics": {
            "mean_rms_B_T": sum(rms_values)/len(rms_values),
            "worst_phase_min_B_T": min(min_values),
            "mean_total_direction_variation_rad": sum(direction_variations)/len(direction_variations),
            "max_abs_signed_tangential_average_T": max(abs(x) for x in signed_integrals),
            "warning": "Path-dependent geometry metrics; not a topological or levitation invariant."
        }
    }


def main():
    baseline = evaluate(
        "coaxial_opposed_pair",
        [(0,0,1),(0,0,1)], [(0,0,-0.02),(0,0,0.02)], [0, math.pi]
    )
    armillary = evaluate(
        "orthogonal_three_ring_armillary",
        [(1,0,0),(0,1,0),(0,0,1)], [(0,0,0)]*3, [0, 2*math.pi/3, 4*math.pi/3]
    )
    result = {
        "model": "quasi-static circular-coil Biot-Savart geometry screen",
        "scope": "field shape and source-state observability only",
        "excluded_claims": ["net levitation", "thermal feasibility", "mechanical rotation", "crystal effects", "3/6/9 privilege", "literal Mobius free-space topology"],
        "configurations": [baseline, armillary],
        "decision_rule": "Advance only if the armillary basis adds robust spatial-field or observability value under equal-drive controls; all whole-apparatus force/impulse claims require a separate conservation-complete model.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
