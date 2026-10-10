#!/usr/bin/env python3
import json, re, sys, subprocess, time, urllib.request, urllib.error, os
sys.path.insert(0, "/storage/emulated/0/HISTORIETA")
import webtoon_estilo as est

KEY = "x67A_9gPMfbXVRNn6ptzdw"
HORD = "https://stablehorde.net/api/v2"

def api(u, metodo="GET", datos=None):
    req = urllib.request.Request(u, json.dumps(datos).encode() if datos is not None else None,
                                 headers={"Content-Type": "application/json",
                                          "apikey": KEY, "User-Agent": "npad"}, method=metodo)
    try:
        return {"status": "ok", "body": json.loads(urllib.request.urlopen(req, timeout=90).read().decode())}
    except urllib.error.HTTPError as e:
        try:
            return {"status": e.code, "body": json.loads(e.read().decode())}
        except Exception:
            return {"status": e.code, "body": e.reason}

def cancela(rid):
    return api(HORD + "/generate/status/" + rid, "DELETE")

def gen(prompt, w, h, modelo="Hassaku XL", steps=24, cfg=7):
    return api(HORD + "/generate/async", "POST", {
        "prompt": prompt,
        "params": {"width": w, "height": h, "steps": steps, "cfg_scale": cfg,
                   "sampler_name": "k_euler_a", "karras": True, "n": 1},
        "nsfw": False, "r2": True, "models": [modelo]})

def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": "npad"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def status(rid):
    return api(HORD + "/generate/status/" + rid)

if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "subir"
    if modo == "cancel":
        print("cancel:", cancela(sys.argv[2]))