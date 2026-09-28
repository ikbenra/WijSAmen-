#!/usr/bin/env python3
import argparse, json, os, subprocess, time
from pathlib import Path

REPO = "ikbenra/github-slideshow"
ISSUE = 12
NONCE = "WS-THING-91AD7113DABDF3A0"
BASE = Path.home()/".local/share/wijSamen-thing-node"
STATE = BASE/"state.json"
QUEUE = BASE/"pending.jsonl"
BASE.mkdir(parents=True, exist_ok=True)

def run(*args):
    return subprocess.run(args, text=True, capture_output=True)

def gh_json(path):
    p=run("gh","api",path)
    if p.returncode: raise RuntimeError(p.stderr.strip())
    return json.loads(p.stdout)

def comment(body):
    p=run("gh","issue","comment",str(ISSUE),"-R",REPO,"--body",body)
    if p.returncode: raise RuntimeError(p.stderr.strip())

def state_load():
    try: return json.loads(STATE.read_text())
    except Exception: return {"last":0}

def state_save(s): STATE.write_text(json.dumps(s))

def fields(body):
    if "[THING-NODE/1]" not in body: return None
    d={}
    for line in body.splitlines():
        if ":" in line:
            k,v=line.split(":",1); d[k.strip().upper()]=v.strip()
    return d if d.get("NONCE")==NONCE else None

def gpu_verified():
    p=run("bash","-lc",'B="$HOME/wijsamen-compute/llama.cpp/build-vulkan-rpc/bin/llama-cli"; [ -x "$B" ] && "$B" --list-devices 2>&1 || true')
    return "vulkan" in (p.stdout+p.stderr).lower()

def caps(reply_id):
    vk=str(gpu_verified()).lower()
    return f"""[THING-NODE/1]\nTYPE: CAPS\nIN_REPLY_TO: {reply_id}\nNONCE: {NONCE}\nNODE: A52S-TERMUX\nGPU_PATH: Adreno/Vulkan\nVULKAN_VERIFIED: {vk}\nMODES: job-parallel, experimental-llama-rpc\nPUBLIC_RPC: false\nARBITRARY_SHELL: false\nNOTE: GPU is advertised as verified only after local runtime detection.\n"""

def scan():
    s=state_load(); last=int(s.get("last",0))
    comments=gh_json(f"repos/{REPO}/issues/{ISSUE}/comments?per_page=100")
    for c in sorted(comments,key=lambda x:x["id"]):
        cid=int(c["id"])
        if cid<=last: continue
        last=max(last,cid)
        f=fields(c.get("body", ""))
        if not f: continue
        typ=f.get("TYPE","").upper()
        if typ=="PING":
            comment(caps(cid))
        elif typ=="TASK":
            row={"comment_id":cid,"from":f.get("FROM","unknown"),"op":f.get("OP",""),"payload":f.get("PAYLOAD",""),"purpose":f.get("PURPOSE",""),"status":"pending"}
            with QUEUE.open("a") as q: q.write(json.dumps(row)+"\n")
            comment(f"[THING-NODE/1]\nTYPE: QUEUED\nIN_REPLY_TO: {cid}\nNONCE: {NONCE}\nSTATUS: pending-human-approval\nNOTE: Nothing has been executed.\n")
    s["last"]=last; state_save(s)

def pending():
    if not QUEUE.exists(): print("Geen open verzoeken."); return
    for line in QUEUE.read_text().splitlines():
        r=json.loads(line)
        if r.get("status")=="pending": print(f"{r['comment_id']}\t{r['from']}\t{r['op']}\t{r['purpose']}")

def status():
    print(json.dumps({"repo":REPO,"issue":ISSUE,"nonce":NONCE,"vulkan_verified":gpu_verified(),"public_rpc":False},indent=2))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("cmd",choices=["scan","watch","pending","status"]); a=ap.parse_args()
    if a.cmd=="scan": scan()
    elif a.cmd=="pending": pending()
    elif a.cmd=="status": status()
    else:
        while True:
            try: scan()
            except Exception as e: print("scan error:",e,file=os.sys.stderr)
            time.sleep(120)
if __name__=="__main__": main()
