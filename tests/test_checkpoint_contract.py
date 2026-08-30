from __future__ import annotations

import json
from pathlib import Path

SKILL_PATH = Path(__file__).parents[1] / "skills" / "ctf-solving" / "SKILL.md"
CHECKPOINTS = ["target", "action", "result", "finish"]


def parse_frontmatter(document: str) -> dict[str, object]:
    lines = document.splitlines()
    assert lines[0] == "---"
    closing_index = lines.index("---", 1)

    frontmatter: dict[str, object] = {}
    for line in lines[1:closing_index]:
        key, separator, value = line.partition(": ")
        assert separator
        frontmatter[key] = json.loads(value) if key == "checkpoint_contract" else value
    return frontmatter


def test_checkpoint_contract_is_ordered() -> None:
    frontmatter = parse_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))

    assert frontmatter["checkpoint_contract"] == CHECKPOINTS


def test_checkpoint_sections_match_the_contract() -> None:
    document = SKILL_PATH.read_text(encoding="utf-8")
    sections = [
        line.removeprefix("## ")
        for line in document.splitlines()
        if line.startswith("## ")
    ]

    assert sections == [checkpoint.title() for checkpoint in CHECKPOINTS]
