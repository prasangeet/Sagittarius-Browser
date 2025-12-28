import time

_t0 = time.time()

def dbg(msg: str):
    dt = time.time() - _t0
    print(f"[DBG {dt:8.3f}s] {msg}", flush=True)

