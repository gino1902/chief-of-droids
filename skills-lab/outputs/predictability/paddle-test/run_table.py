import sys, json, time
from paddleocr import TableRecognitionPipelineV2

RAW = "/Users/gilllesmourgues/Workspace/chief-of-droids/skills-lab/outputs/predictability/ingest-fixture/raw"
path = f"{RAW}/{sys.argv[1]}"

t0 = time.time()
pipe = TableRecognitionPipelineV2()
print(f"[load] {time.time()-t0:.1f}s", flush=True)

t1 = time.time()
out = pipe.predict(path)
print(f"[infer] {time.time()-t1:.1f}s", flush=True)

for res in out:
    j = res.json
    tables = j.get("res", {}).get("table_res_list", [])
    print(f"=== {len(tables)} table(s) ===")
    for i, t in enumerate(tables):
        print(f"--- table {i} HTML ---")
        print(t.get("pred_html", ""))
