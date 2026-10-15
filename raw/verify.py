"""Optional tamper check: do the prompts in PROMPTS.md match the raw session transcripts exactly?

Run from the repo root:  python raw/verify.py
Standard library only, no network, read-only, about 10 seconds.

What it checks: every operator prompt it extracts from raw/*.jsonl appears in PROMPTS.md, in the same
order, character for character, with the same source line and uuid, and PROMPTS.md holds nothing else.
What it cannot check: whether the .jsonl files were edited before they were uploaded. It prints their
SHA-256 so later edits are detectable against README.md and the git history.
"""
import glob, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SINCE = "2026-10-14T08:29:00Z"  # "the last 24 hours" as of the snapshot
ORDER = ["fa864524", "5e3de92a", "1d2a533c"]  # main session, first fork, second fork
SR = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
INJECTED = ("Tool loaded.", "[Request interrupted", "<task-notification", "[SYSTEM NOTIFICATION", "<local-command",
            "Caveat:", "Heartbeat for the overnight", "20-minute reminder", "Reminder (every 20 min)",
            "<command-name>", "<command-message>")


def text_of(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
            return None
        return "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
    return None


def extract(path):
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get("timestamp", "") < SINCE or o.get("isSidechain") or o.get("isMeta"):
            continue
        txt = None
        if o.get("type") == "user" and o.get("message", {}).get("role") == "user":
            raw = text_of(o["message"].get("content"))
            txt = SR.sub("", raw).strip() if raw is not None else None
        elif o.get("type") == "attachment" and isinstance(o.get("attachment"), dict) and o["attachment"].get("type") == "queued_command":
            a = o["attachment"]
            raw = a.get("prompt") if isinstance(a.get("prompt"), str) else text_of(a.get("prompt") or a.get("content"))
            txt = SR.sub("", raw).strip() if raw else None
        elif o.get("type") == "system" and o.get("subtype") == "local_command":
            m = re.search(r"<command-name>(.*?)</command-name>.*?<command-args>(.*?)</command-args>", o.get("content", ""), re.S)
            if m:
                yield n, o.get("uuid"), (m.group(1) + " " + m.group(2)).strip()
            continue
        if txt and not txt.startswith(INJECTED):
            yield n, o.get("uuid"), txt


files = {os.path.basename(p)[:8]: p for p in glob.glob(os.path.join(ROOT, "raw", "*.jsonl"))}
expected, seen = [], set()
for s in ORDER:
    for n, uuid, t in extract(files[s]):
        norm = t[len("/fork "):] if t.startswith("/fork ") else t
        if norm in seen:  # forks repeat the parent's history; a fork's first message repeats its /fork argument
            continue
        seen.add(norm)
        expected.append((os.path.basename(files[s]), n, uuid, t))

md = open(os.path.join(ROOT, "PROMPTS.md"), encoding="utf-8").read()
found = []
for m in re.finditer(r"^## P\d+ .*?\nSource: `raw/(\S+)` line (\d+), uuid `([^`]+)`\n\n(`{3,})text\n(.*?)\n\4\n", md, re.S | re.M):
    found.append((m.group(1), int(m.group(2)), m.group(3), m.group(5)))

bad = 0
for i in range(max(len(expected), len(found))):
    e = expected[i] if i < len(expected) else None
    f = found[i] if i < len(found) else None
    if e != f:
        bad += 1
        print(f"MISMATCH at P{i + 1:02d}: transcript={e and (e[0], e[1], len(e[3]))} prompts.md={f and (f[0], f[1], len(f[3]))}")
for s, p in sorted(files.items()):
    # hash with line endings normalised to LF, so a Windows checkout (CRLF) gives the same value as README.md
    print("sha256", hashlib.sha256(open(p, encoding="utf-8").read().encode("utf-8")).hexdigest(), os.path.basename(p))
print(("PASS: " if not bad else "FAIL: ") + f"{len(found)} prompts in PROMPTS.md, {len(expected)} extracted from the transcripts, {bad} mismatches")
sys.exit(1 if bad else 0)
