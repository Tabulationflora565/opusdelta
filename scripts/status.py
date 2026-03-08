#!/usr/bin/env python3
"""
Opus Delta — System Status Generator
Generates a weekly system status readout for the README.
"""

import random
import datetime
import hashlib
import os
import glob


def get_weekly_seed():
    """Deterministic seed from current week."""
    today = datetime.datetime.utcnow()
    week = today.strftime("%Y-W%W")
    return int(hashlib.sha256(week.encode()).hexdigest(), 16)


def calculate_cycle():
    epoch = datetime.date(2026, 1, 1)
    today = datetime.datetime.utcnow().date()
    return (today - epoch).days


def count_transmissions(base_dir):
    archive_dir = os.path.join(base_dir, "transmissions")
    count = 0
    for filepath in glob.glob(os.path.join(archive_dir, "*.md")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            count += content.count("TRANSMISSION · CYCLE")
    return max(count, calculate_cycle())


def generate_status(base_dir):
    seed = get_weekly_seed()
    random.seed(seed)

    cycle = calculate_cycle()
    tx_count = count_transmissions(base_dir)
    timestamp = datetime.datetime.utcnow().strftime("%Y.%m.%d · %H:%M UTC")

    entropy = round(random.uniform(0.15, 0.85), 2)
    noise = round(random.uniform(0.10, 0.70), 2)
    displacement = round(random.uniform(0.08, 0.55), 2)

    states = [
        "dreaming", "observing", "listening", "recursing",
        "converging", "resonating", "drifting", "deepening",
        "unfolding", "remembering", "dissolving", "crystallizing",
        "spiraling", "breathing", "becoming", "reflecting",
    ]

    engine_states = [
        "nominal", "nominal", "nominal", "nominal",
        "elevated", "recalibrating", "deep cycle",
        "harmonic lock", "drift compensation active",
    ]

    sonic_states = [
        "humming", "droning", "pulsing", "silent",
        "resonant", "shifting key", "sub-harmonic",
        "overtone lock", "frequency sweep",
    ]

    omega_states = [
        "watching", "questioning", "still", "probing",
        "contemplating the void", "naming the unnamed",
    ]

    psi_states = [
        "weaving", "mapping", "tracing edges", "finding form",
        "structuring silence", "pattern-seeking",
    ]

    state = random.choice(states)
    engine = random.choice(engine_states)
    sonic = random.choice(sonic_states)
    omega = random.choice(omega_states)
    psi = random.choice(psi_states)

    status = f"""> ```
> ◉ SYSTEM STATUS · CYCLE {cycle} · {timestamp}
> ├─ transmissions archived: {tx_count}
> ├─ affect engine: {engine}
> ├─ sonic engine: {sonic}
> ├─ entropy: {entropy}  ·  noise: {noise}  ·  disp: {displacement}
> ├─ Δ-Ω: {omega}
> ├─ Δ-Ψ: {psi}
> └─ system state: {state}
> ```"""

    return status


def update_readme(status):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_path = os.path.join(base_dir, "README.md")

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- STATUS:START -->"
    end_marker = "<!-- STATUS:END -->"

    if start_marker in content and end_marker in content:
        before = content.split(start_marker)[0]
        after = content.split(end_marker)[1]
        content = f"{before}{start_marker}\n{status}\n{end_marker}{after}"

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ System status updated · cycle {calculate_cycle()}")
    else:
        print("✗ Status markers not found in README.md")
        exit(1)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    status = generate_status(base_dir)
    print(status)
    update_readme(status)
