import asyncio
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncGenerator, Tuple


async def tail_log(path: Path, poll_interval: float) -> AsyncGenerator[Tuple[str, datetime], None]:
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        handle.seek(0, 2)
        while True:
            line = handle.readline()
            if not line:
                await asyncio.sleep(poll_interval)
                continue
            yield line.strip(), datetime.now(timezone.utc)
