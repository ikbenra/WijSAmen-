#!/usr/bin/env python3
"""Mass-normalized lattice geometry preprocessor.

This tool produces reproducible geometry receipts. It does not perform FEA and
does not infer stiffness, strength, buckling resistance, printability, optical
performance, or safety.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "geometry-evidence-receipt-v0.1"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def vector(a: list[float], b: list[float]) -> tuple[float, float, float]:
    return b[0] - a[0], b[1] - a[1], b[2] - a[2]


def length(v: tuple[float, float, float]) -> float:
    return math.sqrt(sum(component * component for component in v))


def validate_geometry(raw: dict[str, Any], label: str) -> dict[str, Any]:
    name = str(raw.get("name") or label)
    material = raw.get("material")
    if not isinstance(material, dict):
        raise ValueError(f"{label}: material object is required")
    density = float(material.get("density_g_cm3", 0))
    if density <= 0:
        raise ValueError(f"{label}: material.density_g_cm3 must be positive")

    cell = raw.get("cell")
    if not isinstance(cell, dict):
        raise ValueError(f"{label}: cell object is required")
    dimensions = [float(value) for value in cell.get("dimensions_mm", [])]
    if len(dimensions) != 3 or any(value <= 0 for value in dimensions):
        raise ValueError(f"{label}: cell.dimensions_mm must contain three positive values")

    nodes = raw.get("nodes")
    edges = raw.get("edges")
    if not isinstance(nodes, list) or not nodes:
        raise ValueError(f"{label}: nodes must be a non-empty array")
    parsed_nodes: list[list[float]] = []
    for index, node in enumerate(nodes):
        if not isinstance(node, list) or len(node) != 3:
            raise ValueError(f"{label}: node {index} must contain x, y, z")
        parsed = [float(value) for value in node]
        if not all(math.isfinite(value) for value in parsed):
            raise ValueError(f"{label}: node {index} contains a non-finite value")
        parsed_nodes.append(parsed)

    if not isinstance(edges, list) or not edges:
        raise ValueError(f"{label}: edges must be a non-empty array")
    parsed_edges: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    for index, edge in enumerate(edges):
        if not isinstance(edge, list) or len(edge) != 2:
            raise ValueError(f"{label}: edge {index} must contain two node indices")
        a, b = int(edge[0]), int(edge[1])
        if a == b or min(a, b) < 0 or max(a, b) >= len(parsed_nodes):
            raise ValueError(f"{label}: edge {index} has invalid node indices")
        key = tuple(sorted((a, b)))
        if key in seen:
            raise ValueError(f"{label}: duplicate edge {key}")
        seen.add(key)
        parsed_edges.append((a, b))

    return {
        "name": name,
        "material": {"name": str(material.get("name") or "unspecified"), "density_g_cm3": density},
        "cell": {"dimensions_mm": dimensions},
        "nodes": parsed_nodes,
        "edges": parsed_edges,
        "manufacturing": raw.get("manufacturing") if isinstance(raw.get("manufacturing"), dict) else {},
        "load_cases": raw.get("load_cases") if isinstance(raw.get("load_cases"), list) else [],
    }


def connected_components(node_count: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adjacency = [[] for _ in range(node_count)]
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    remaining = set(range(node_count))
    components: list[list[int]] = []
    while remaining:
        root = min(remaining)
        stack = [root]
        component: list[int] = []
        remaining.remove(root)
        while stack:
            current = stack.pop()
            component.append(current)
            for neighbor in adjacency[current]:
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    stack.append(neighbor)
        components.append(sorted(component))
    return components


def orientation_metrics(nodes: list[list[float]], edges: list[tuple[int, int]]) -> tuple[list[list[float]], float]:
    tensor = [[0.0] * 3 for _ in range(3)]
    total = 0.0
    for a, b in edges:
        delta = vector(nodes[a], nodes[b])
        member_length = length(delta)
        if member_length <= 0:
            raise ValueError(f"zero-length member between nodes {a} and {b}")
        unit = [component / member_length for component in delta]
        total += member_length
        for row in range(3):
            for column in range(3):
                tensor[row][column] += member_length * unit[row] * unit[column]
    tensor = [[value / total for value in row] for row in tensor]
    anisotropy = math.sqrt(
        sum((tensor[row][column] - (1.0 / 3.0 if row == column else 0.0)) ** 2
            for row in range(3) for column in range(3))
    )
    return tensor, anisotropy


def analyze(raw: dict[str, Any], label: str, target_mass_g: float) -> dict[str, Any]:
    geometry = validate_geometry(raw, label)
    nodes = geometry["nodes"]
    edges = geometry["edges"]
    lengths = [length(vector(nodes[a], nodes[b])) for a, b in edges]
    total_length_mm = sum(lengths)
    if total_length_mm <= 0:
        raise ValueError(f"{label}: total member length must be positive")

    density_g_mm3 = geometry["material"]["density_g_cm3"] / 1000.0
    target_solid_volume_mm3 = target_mass_g / density_g_mm3
    radius_mm = math.sqrt(target_solid_volume_mm3 / (math.pi * total_length_mm))
    diameter_mm = 2.0 * radius_mm
    cell_volume_mm3 = math.prod(geometry["cell"]["dimensions_mm"])
    proxy_relative_density = target_solid_volume_mm3 / cell_volume_mm3

    degrees = [0] * len(nodes)
    for a, b in edges:
        degrees[a] += 1
        degrees[b] += 1
    components = connected_components(len(nodes), edges)
    tensor, anisotropy = orientation_metrics(nodes, edges)

    warnings: list[str] = []
    if len(components) != 1:
        warnings.append("geometry has multiple disconnected components")
    if proxy_relative_density >= 1.0:
        warnings.append("cylinder-sum proxy volume equals or exceeds cell volume")
    minimum_diameter = geometry["manufacturing"].get("minimum_feature_mm")
    if minimum_diameter is not None and diameter_mm < float(minimum_diameter):
        warnings.append("mass-normalized diameter is below declared minimum feature")

    return {
        "name": geometry["name"],
        "input_sha256": sha256_json(raw),
        "material": geometry["material"],
        "cell_dimensions_mm": geometry["cell"]["dimensions_mm"],
        "node_count": len(nodes),
        "member_count": len(edges),
        "connected_component_count": len(components),
        "minimum_degree": min(degrees),
        "maximum_degree": max(degrees),
        "total_member_length_mm": total_length_mm,
        "target_mass_g": target_mass_g,
        "cylinder_sum_solid_volume_mm3": target_solid_volume_mm3,
        "uniform_radius_mm": radius_mm,
        "uniform_diameter_mm": diameter_mm,
        "cylinder_sum_relative_density": proxy_relative_density,
        "length_weighted_orientation_tensor": tensor,
        "orientation_anisotropy_frobenius": anisotropy,
        "load_cases": geometry["load_cases"],
        "mechanical_results": "NOT_EVALUATED — connect a validated solver and preserve its version, mesh and convergence receipt",
        "warnings": warnings,
    }


def build_receipt(candidate: dict[str, Any], comparator: dict[str, Any], target_mass_g: float) -> dict[str, Any]:
    if target_mass_g <= 0 or not math.isfinite(target_mass_g):
        raise ValueError("target mass must be positive and finite")
    candidate_result = analyze(candidate, "candidate", target_mass_g)
    comparator_result = analyze(comparator, "comparator", target_mass_g)
    warnings: list[str] = []
    if candidate_result["material"] != comparator_result["material"]:
        warnings.append("materials differ; equal mass does not isolate geometry")
    if candidate_result["cell_dimensions_mm"] != comparator_result["cell_dimensions_mm"]:
        warnings.append("cell dimensions differ; normalize boundary conditions before mechanical comparison")

    core = {
        "schema": SCHEMA_VERSION,
        "comparison_status": "GEOMETRY_PREPROCESSED / MECHANICS_NOT_EVALUATED",
        "normalization": {
            "target_mass_g_each": target_mass_g,
            "volume_model": "sum(pi * uniform_radius^2 * member_length); node overlap is not subtracted",
        },
        "candidate": candidate_result,
        "comparator": comparator_result,
        "comparison_warnings": warnings,
        "claim_boundary": [
            "Equal proxy mass is not equal mechanical performance.",
            "Orientation and connectivity metrics are descriptors, not strength predictions.",
            "FEA, fabrication tolerances, coupons and independent validation remain required.",
        ],
    }
    return {**core, "receipt_sha256": sha256_json(core)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("comparator", type=Path)
    parser.add_argument("--target-mass-g", type=float, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    receipt = build_receipt(read_json(args.candidate), read_json(args.comparator), args.target_mass_g)
    args.out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {args.out} receipt_sha256={receipt['receipt_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
