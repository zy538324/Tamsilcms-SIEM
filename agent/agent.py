import asyncio
from datetime import datetime, timezone
from typing import List

import aiohttp

from config import AgentConfig, load_config
from reader import tail_log
from spool import append_to_spool, read_from_spool


def _build_event(config: AgentConfig, message: str, timestamp: datetime) -> dict:
    return {
        "agent_id": config.agent_id,
        "hostname": config.hostname,
        "os_type": config.os_type,
        "os_version": config.os_version,
        "log_source": config.log_source,
        "event_time": timestamp.isoformat(),
        "event_level": "INFO",
        "event_id": "0",
        "message": message,
    }


async def _post_events(session: aiohttp.ClientSession, config: AgentConfig, events: List[dict]) -> bool:
    if not events:
        return True

    payload = {"agent_id": config.agent_id, "events": events}

    try:
        async with session.post(
            config.api_url,
            json=payload,
            headers={"X-Agent-Key": config.api_key},
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:
            if response.status == 202:
                return True
    except aiohttp.ClientError:
        return False

    return False


async def _flush_spool(session: aiohttp.ClientSession, config: AgentConfig) -> None:
    queued = read_from_spool(config.spool_path, config.batch_size)
    if not queued:
        return

    success = await _post_events(session, config, queued)
    if not success:
        append_to_spool(config.spool_path, queued)


async def run_agent() -> None:
    config = load_config()

    if not config.api_key or not config.agent_id:
        raise RuntimeError("API_KEY and AGENT_ID must be configured")

    async with aiohttp.ClientSession() as session:
        await _flush_spool(session, config)

        batch: List[dict] = []
        async for line, timestamp in tail_log(config.log_path, config.poll_interval):
            batch.append(_build_event(config, line, timestamp))

            if len(batch) >= config.batch_size:
                success = await _post_events(session, config, batch)
                if not success:
                    append_to_spool(config.spool_path, batch)
                batch = []


if __name__ == "__main__":
    asyncio.run(run_agent())
