#!/usr/bin/env python3
import json, time, urllib.request, urllib.error, base64, sys
KEY = "x67A_9gPMfbXVRNn6ptzdw"

def h(url):
    req = urllib.request.Request(url, headers={"apikey": KEY, "User-Agent": "npad"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"err": str(e)}

def espera(rid, salida, max_t=3600):
    t = 0
    while t < max_t:
        time.sleep(20); t += 20
        j = h("https://stablehorde.net/api/v2/generate/status/" + rid)
        info = {k: j.get(k) for k in ["done", "faulted", "finished", "processing", "waiting", "queue_position"] if k in j}
        if "err" in j:
            info["err"] = j["err"]
        print(t, info, flush=True)
        if j.get("done"):
            g = (j.get("generations") or [{}])[0]
            if g.get("img"):
                img = g["img"]
                if img.startswith("http"):
                    with urllib.request.urlopen(urllib.request.Request(img, headers={"User-Agent": "npad"}), timeout=120) as r:
                        data = r.read()
                else:
                    img += "=" * (-len(img) % 4)
                    data = base64.b64decode(img)
                with open(salida, "wb") as f:
                    f.write(data)
                print("OK seed", g.get("seed"), "modelo", g.get("model"), flush=True)
            else:
                print("SIN IMAGEN", j, flush=True)
            return
        if j.get("faulted"):
            print("FAULTED", j, flush=True)
            return
    print("TIMEOUT", flush=True)

if __name__ == "__main__":
    espera(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 3600)