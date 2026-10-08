"""Generate compositions/captions.html from transcript.json + scripts/caption_groups.txt.

usage: python3 -I scripts/build_captions.py <root-duration-seconds>
"""
import json
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
proj = os.path.dirname(here)
duration = float(sys.argv[1])

words = json.load(open(os.path.join(proj, "transcript.json")))
lines = open(os.path.join(here, "caption_groups.txt")).read().strip().split("\n")

sizes, i = [], 0
for line in lines:
    n = len(line.split())
    got = " ".join(w["text"] for w in words[i : i + n])
    assert got == line, f"caption group mismatch: {line!r} vs {got!r}"
    assert 1 <= n <= 4, f"group too long: {line!r}"
    sizes.append(n)
    i += n
assert i == len(words), "caption groups must cover every word"

end = min(words[-1]["end"] + 0.6, duration - 0.05)
slim = [{"text": w["text"], "start": w["start"], "end": w["end"]} for w in words]
html = open(os.path.join(here, "captions.template.html")).read()
html = (
    html.replace("__WORDS__", json.dumps(slim, separators=(",", ":")))
    .replace("__SIZES__", json.dumps(sizes))
    .replace("__END__", f"{end:.3f}")
    .replace("__DURATION__", f"{duration:g}")
)
os.makedirs(os.path.join(proj, "compositions"), exist_ok=True)
open(os.path.join(proj, "compositions", "captions.html"), "w").write(html)
print(f"captions.html: {len(sizes)} phrases, {len(words)} words, duration {duration:g}s")
