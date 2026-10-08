"""Map the script's spelling/punctuation onto the trimmed-audio ASR timings (1:1 word order)."""
import json, re, sys
script = open(sys.argv[1]).read().split()
asr = json.load(open(sys.argv[2]))
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower().replace("&", ""))
assert len(script) == len(asr), (len(script), len(asr))
out = []
for i, (s, a) in enumerate(zip(script, asr)):
    assert norm(s) == norm(a["text"]), (i, s, a["text"])
    out.append({"id": f"w{i}", "text": s, "start": round(a["start"], 3), "end": round(a["end"], 3)})
json.dump(out, open(sys.argv[3], "w"), indent=1)
print(len(out), "words; last ends", out[-1]["end"])
