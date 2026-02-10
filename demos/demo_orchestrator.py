import asyncio
import subprocess
import json
import re
import sys
import os
import ast
from pathlib import Path
from typing import List, Dict

SYSTEM2 = "system2.py"
SYSTEM1 = "system1.py"
SHADOW_INPUT = Path("shadow_input.json")


# -----------------------------
# System 2 Runner
# -----------------------------

async def run_system2() -> str:
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        SYSTEM2,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(
            f"[System2 failed]\n{stderr.decode(errors='ignore')}"
        )

    return stdout.decode(errors="ignore")


# -----------------------------
# Signal Extraction
# -----------------------------

def extract_signals(text: str) -> List[Dict]:
    signals: List[Dict] = []

    cycles = re.findall(
        r"CYCLE\s+\d+.*?(?=CYCLE|\Z)",
        text,
        flags=re.S
    )

    for block in cycles:
        c = re.search(r"coherence:\s*([0-9.]+)", block)
        u = re.search(r"uncertainty:\s*([0-9.]+)", block)
        f = re.search(r"field:\s*({.*?})", block, re.S)

        if not (c and u and f):
            continue

        try:
            field = ast.literal_eval(f.group(1))
            coherence = float(c.group(1))
            uncertainty = float(u.group(1))
        except Exception:
            continue

        signals.append({
            "confidence": max(0.0, min(1.0, 1.0 - uncertainty)),
            "coherence": max(0.0, min(1.0, coherence)),
            "novelty": float(field.get("novelty", 0.0)),
            "complexity": float(field.get("complexity", 0.0)),
        })

    return signals


# -----------------------------
# System 1 Runner
# -----------------------------

async def run_system1(signals: List[Dict]) -> str:
    SHADOW_INPUT.write_text(json.dumps(signals, indent=2))

    env = dict(os.environ)
    env["AWARENESS_INPUT"] = str(SHADOW_INPUT.resolve())

    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        SYSTEM1,
        env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(
            f"[System1 failed]\n{stderr.decode(errors='ignore')}"
        )

    return stdout.decode(errors="ignore")


# -----------------------------
# Orchestration
# -----------------------------

async def orchestrate():
    system2_output = await run_system2()
    signals = extract_signals(system2_output)

    if not signals:
        raise RuntimeError("No awareness signals extracted from System 2")

    system1_output = await run_system1(signals)

    return {
        "signals_used": len(signals),
        "signals": signals,
        "system1_output": system1_output.strip()
    }


# -----------------------------
# Entry Point
# -----------------------------

if __name__ == "__main__":
    print(
        "9DA Demo Notice\n\n"
        "This replay demonstrates governed dimensional expansion,\n"
        "not autonomous decision authority.\n\n"
        "This repository includes a browser-first demo (demo_viewer.html).\n"
    )

    if "--run" in sys.argv:
        result = asyncio.run(orchestrate())
        print(json.dumps(result, indent=2))
