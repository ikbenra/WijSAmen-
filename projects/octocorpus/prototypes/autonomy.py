"""Bounded OctoCorpus self-improvement lab. Synthetic; not a consciousness test."""
import argparse, copy, hashlib, json, os, tempfile
from pathlib import Path
KINDS=("C","Si","SiC_N")
BASE={"C":[0,2,0],"Si":[2,0,0],"SiC_N":[1,1,0]}
def examples():
    return [((c,h,p),int(bool(h or (c and p)))) for c in (0,1) for h in (0,1) for p in (0,1)]
def score(weights,data):
    return sum(int(sum(w*x for w,x in zip(weights,obs))>=2)==target for obs,target in data)
def initial():
    return {"schema":"octocorpus.autonomy.v1","generation":0,"policies":{k:v.copy() for k,v in BASE.items()},"head":{"shared_nodule":True,"meta_learning":"holdout_gated"},"n_modules":4,"mode":"six_arms"}
def state_hash(state):
    payload = {key: value for key, value in state.items() if key != "state_hash"}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

def validate_state(state):
    if state.get("schema") != "octocorpus.autonomy.v1":
        raise ValueError("incompatible checkpoint")
    if "state_hash" in state and state["state_hash"] != state_hash(state):
        raise ValueError("checkpoint hash mismatch")
    if type(state.get("generation")) is not int or state["generation"] < 0:
        raise ValueError("invalid generation")
    policies = state.get("policies")
    if not isinstance(policies, dict) or set(policies) != set(KINDS):
        raise ValueError("invalid policy groups")
    for weights in policies.values():
        if not isinstance(weights, list) or len(weights) != 3:
            raise ValueError("invalid policy width")
        if any(type(weight) is not int or not -2 <= weight <= 2 for weight in weights):
            raise ValueError("invalid policy weight")

def save_state(path, state):
    """Replace a checkpoint atomically, leaving the old file intact on failure."""
    validate_state(state)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(json.dumps(state, indent=2, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)

def evolve(state,steps=24):
    if type(steps) is not int or not 1 <= steps <= 100:
        raise ValueError("steps must be 1..100")
    validate_state(state)
    state = copy.deepcopy(state)
    data=examples()
    train=[data[i] for i in (0,1,2,4,5,6)]
    holdout=[data[i] for i in (3,7)]
    log=[]
    for _ in range(steps):
        best=None
        for kind in KINDS:
            baseline=state["policies"][kind]
            base_score=score(baseline,train)
            for j in range(3):
                for delta in (-1,1):
                    proposed=baseline.copy()
                    proposed[j]=max(-2,min(2,proposed[j]+delta))
                    gain=score(proposed,train)-base_score
                    if proposed==baseline or gain<=0: continue
                    candidate=(gain,kind,j,delta,proposed)
                    if best is None or candidate[:4]>best[:4]: best=candidate
        if best is None:
            state["stop_reason"]="no_training_improvement"
            break
        gain,kind,j,delta,proposed=best
        before=state["policies"][kind]
        old,new=score(before,holdout),score(proposed,holdout)
        if new<old:
            log.append({"kind":kind,"status":"REJECTED_HOLDOUT"})
            state["stop_reason"]="holdout_regression"
            break
        state["policies"][kind]=proposed
        state["generation"]+=1
        log.append({"generation":state["generation"],"kind":kind,"from":before,"to":proposed,"train_gain":gain,"holdout_before":old,"holdout_after":new,"status":"ACCEPTED"})
    else: state["stop_reason"]="step_budget"
    state["last_log"]=log
    state["evidence"]="SYNTHETIC_POLICY_OPTIMIZATION"
    state["consciousness_proven"]=False
    state["state_hash"]=state_hash(state)
    return state
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--state",default="octocorpus-state.json")
    p.add_argument("--steps",type=int,default=24)
    a=p.parse_args()
    if not 1<=a.steps<=100: p.error("steps must be 1..100")
    path=Path(a.state)
    state=json.loads(path.read_text()) if path.exists() else initial()
    try:
        result=evolve(state,a.steps)
        save_state(path, result)
    except ValueError as error:
        p.error(str(error))
    print(json.dumps({"generation":result["generation"],"stop_reason":result["stop_reason"],"accepted":sum(x["status"]=="ACCEPTED" for x in result["last_log"]),"state_hash":result["state_hash"]}))
if __name__=="__main__": main()

