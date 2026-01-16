import json
from pathlib import Path
from typing import Iterable, List


def append_to_spool(spool_path: Path, events: Iterable[dict]) -> None:
    spool_path.parent.mkdir(parents=True, exist_ok=True)
    with spool_path.open("a", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def read_from_spool(spool_path: Path, max_events: int) -> List[dict]:
    if not spool_path.exists():
        return []

    events: List[dict] = []
    lines: List[str] = []

    with spool_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if len(events) >= max_events:
                lines.append(line)
                continue
            events.append(json.loads(line))

    with spool_path.open("w", encoding="utf-8") as handle:
        handle.writelines(lines)

    return events
