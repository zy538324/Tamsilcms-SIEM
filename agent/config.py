import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class AgentConfig:
    api_url: str
    api_key: str
    agent_id: str
    hostname: str
    os_type: str
    os_version: str
    log_source: str
    log_path: Path
    batch_size: int
    poll_interval: float
    spool_path: Path


def load_config() -> AgentConfig:
    log_path = Path(os.getenv("LOG_PATH", "/var/log/syslog"))
    spool_path = Path(os.getenv("SPOOL_PATH", "/tmp/siem_spool.jsonl"))

    return AgentConfig(
        api_url=os.getenv("API_URL", "http://localhost:8080/api/v1/logs/ingest"),
        api_key=os.getenv("API_KEY", ""),
        agent_id=os.getenv("AGENT_ID", ""),
        hostname=os.getenv("HOSTNAME", ""),
        os_type=os.getenv("OS_TYPE", "linux"),
        os_version=os.getenv("OS_VERSION", ""),
        log_source=os.getenv("LOG_SOURCE", "syslog"),
        log_path=log_path,
        batch_size=int(os.getenv("BATCH_SIZE", "100")),
        poll_interval=float(os.getenv("POLL_INTERVAL", "1.5")),
        spool_path=spool_path,
    )
