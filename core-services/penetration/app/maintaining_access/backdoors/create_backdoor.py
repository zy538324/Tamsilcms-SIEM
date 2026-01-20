"""Backdoor creation helpers used during the maintaining access phase."""

from __future__ import annotations

from typing import Dict


def craft_backdoor_config(method: str, *, port: int | None = None, password: str | None = None) -> Dict[str, object]:
    """Produce a configuration dictionary for a simulated backdoor.

    Parameters
    ----------
    method:
        The persistence mechanism to emulate (e.g. ``"ssh"`` or ``"webshell"``).
    port:
        Optional port to expose.  Defaults are picked based on the method when
        not provided.
    password:
        Optional static credential to store in the configuration.  When omitted
        a deterministic placeholder is generated so that unit tests can make
        assertions without random data.
    """

    method = method.lower()
    default_ports = {"ssh": 22, "webshell": 8080, "service": 31337}
    port = port or default_ports.get(method, 2222)
    password = password or f"{method}_access"

    return {
        "method": method,
        "port": port,
        "credential": password,
        "persistence": "cron" if method != "service" else "systemd",
    }


def verify_backdoor(config: Dict[str, object], *, heartbeat: bool = True) -> Dict[str, object]:
    """Return a diagnostic structure indicating the backdoor is reachable."""

    status = "online" if heartbeat else "offline"
    reachable = heartbeat and config.get("port") is not None

    return {
        "config": config,
        "status": status,
        "reachable": reachable,
        "checks": [
            "port_open" if reachable else "port_closed",
            "auth_ok" if reachable else "auth_unknown",
        ],
    }


__all__ = ["craft_backdoor_config", "verify_backdoor"]

