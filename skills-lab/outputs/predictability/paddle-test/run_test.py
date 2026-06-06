import sys, json, time
from paddleocr import ChartParsing

RAW = "/Users/gilllesmourgues/Workspace/chief-of-droids/skills-lab/outputs/predictability/ingest-fixture/raw"
img = sys.argv[1]
query = sys.argv[2] if len(sys.argv) > 2 else "Convert this chart to a table."
path = f"{RAW}/{img}"

t0 = time.time()
model = ChartParsing()
print(f"[load] {time.time()-t0:.1f}s", flush=True)

t1 = time.time()
out = model.predict({"image": path, "query": query})
print(f"[infer] {time.time()-t1:.1f}s", flush=True)

for res in out:
    j = res.json
    print("=== RESULT ===")
    print(json.dumps(j, ensure_ascii=False, indent=2, default=str))
