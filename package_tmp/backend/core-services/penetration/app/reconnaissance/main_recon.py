# core/reconnaissance/main_recon.py

import dns.resolver
import logging
from collections import OrderedDict
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    OrderedDict as OrderedDictType,
    Sequence,
    Union,
)
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import os
import networkx as nx
import matplotlib.pyplot as plt
import json

from database.models import PenTestResult
from database.db_setup import db
from core.security import (
    TargetAuthorizationError,
    ensure_targets_authorized,
    load_approved_targets,
    normalise_approved_targets,
    record_audit_event,
)

from core.scanning.manager import Scanning
from core.gaining_access.system_hacking.exploit_generation import build_exploit_plan
from core.gaining_access.system_hacking.payload_delivery import compose_payload, deliver_payload
from core.maintaining_access.backdoors.create_backdoor import craft_backdoor_config, verify_backdoor
from core.covering_tracks.log_cleaning.clean_logs import detect_log_entries, clean_log_entries
from core.Reporting.report_builder import merge_phase_results

from .active_scanning.scan_ip_blocks import scan_ip_blocks
from .active_reconnaissance.port_scanner.port_scanner import parse_ports
from .service_enumeration import enumerate_services
from .gather_host_info.gather_host_info import gather_all_info
from .gather_identity_info.gather_identity_info import gather_identity_info
from .gather_network_info.gather_network_info import gather_network_info
from .phishing_for_info.phishing_for_info import phishing_for_info
from .passive_reconnaissance.whois.whois import unified_domain_lookup

recon_bp = Blueprint('recon', __name__)
logger = logging.getLogger(__name__)


def perform_dns_enumeration(domain: str, record_type: str = 'A') -> Union[List[str], str]:
    """Resolve DNS records for a given domain.

    Args:
        domain: Domain name to query.
        record_type: DNS record type (e.g. ``"A"`` or ``"MX"``).

    Returns:
        A list of record data strings on success or an error message if the
        lookup fails.
    """
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [rdata.to_text() for rdata in answers]
    except Exception as e:  # pragma: no cover - network errors depend on environment
        return f"Error: {e}"


def generate_topology_map(active_hosts: List[Dict[str, str]], filename: str = 'topology_map.png') -> str:
    """Generate and persist a simple network topology map.

    Args:
        active_hosts: List of dictionaries with ``hostname`` and ``ip`` keys.
        filename: Name of the output image file stored under the Flask
            application's static folder.

    Returns:
        The name of the generated image file.

    Raises:
        OSError: If the image cannot be written to disk.
    """
    G = nx.Graph()
    # Add nodes and edges
    for host in active_hosts:
        hostname = host['hostname']
        ip = host['ip']
        G.add_node(hostname, ip=ip)
        # Assuming a simple star topology with a central node (e.g., "Network")
        G.add_edge("Network", hostname)
    
    # Draw the graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold')
    labels = nx.get_node_attributes(G, 'ip')
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    # Save the graph as an image
    filepath = os.path.join(current_app.static_folder, filename)
    plt.savefig(filepath)
    plt.close()
    return filename

@recon_bp.route('/enumerate_dns', methods=['POST'])
def enumerate_dns() -> 'flask.Response':
    """API endpoint for DNS enumeration.

    Expects JSON with ``domain`` and optional ``record_type``.  Returns the
    resolved records or an error message.
    """
    data = request.json or {}
    domain = data.get('domain')
    record_type = data.get('record_type', 'A')

    if not domain:
        return jsonify({'error': 'Domain is required'}), 400

    result = perform_dns_enumeration(domain, record_type)

    return jsonify({'domain': domain, 'record_type': record_type, 'results': result})


def _normalise_port_spec(port_spec: Optional[Union[str, Iterable[int]]]) -> List[int]:
    """Convert assorted port specifications into a sorted list of integers."""

    if port_spec is None:
        return []

    if isinstance(port_spec, str):
        spec = port_spec.strip()
        if not spec:
            return []
        try:
            parsed = json.loads(spec)
        except (TypeError, ValueError):
            parsed = None
        if isinstance(parsed, (list, tuple, set)):
            port_spec = parsed  # type: ignore[assignment]
        else:
            return parse_ports(spec)

    if isinstance(port_spec, Iterable):
        ports: List[int] = []
        for value in port_spec:
            if isinstance(value, bool):
                continue
            try:
                port = int(value)
            except (TypeError, ValueError):
                continue
            if 0 < port < 65536:
                ports.append(port)
        return sorted(set(ports))

    try:
        if isinstance(port_spec, bool):
            return []
        port = int(port_spec)
    except (TypeError, ValueError):
        return []
    return [port] if 0 < port < 65536 else []


_PORT_CONTAINER_KEYS = {"open_ports", "ports", "open_port_numbers", "open_port_list"}
_SINGLE_PORT_KEYS = {"port", "port_number"}
_NESTED_PORT_HOLDERS = {"scan_summary"}


def _collect_port_numbers(value: Any) -> List[int]:
    ports: List[int] = []
    if isinstance(value, dict):
        for key, inner in value.items():
            if key in _PORT_CONTAINER_KEYS or key in _NESTED_PORT_HOLDERS:
                ports.extend(_collect_port_numbers(inner))
                continue
            if key in _SINGLE_PORT_KEYS:
                ports.extend(_collect_port_numbers(inner))
                continue
            if isinstance(key, (int, str)) and str(key).isdigit():
                number = int(key)
                if 1 <= number <= 65535:
                    ports.append(number)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            ports.extend(_collect_port_numbers(item))
    else:
        if isinstance(value, int) and 1 <= value <= 65535:
            ports.append(value)
        elif isinstance(value, str) and value.isdigit():
            number = int(value)
            if 1 <= number <= 65535:
                ports.append(number)
    return ports


def _collect_service_candidates(value: Any) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []

    def _merge(port: int, payload: Dict[str, Any]) -> None:
        existing = next((item for item in candidates if item.get("port") == port), None)
        if existing is None:
            merged = dict(payload)
            merged["port"] = port
            candidates.append(merged)
        else:
            existing.update({k: v for k, v in payload.items() if k != "port"})

    if isinstance(value, dict):
        port_value = value.get("port")
        if isinstance(port_value, int):
            payload = dict(value)
            payload.pop("port", None)
            _merge(port_value, payload)
        elif isinstance(port_value, str) and port_value.isdigit():
            payload = dict(value)
            payload.pop("port", None)
            _merge(int(port_value), payload)

        open_ports_value = value.get("open_ports")
        if open_ports_value is not None:
            candidates.extend(_collect_service_candidates(open_ports_value))

        if "scan_summary" in value and isinstance(value["scan_summary"], dict):
            summary_open_ports = value["scan_summary"].get("open_ports")
            if isinstance(summary_open_ports, dict):
                for raw_key, details in summary_open_ports.items():
                    port_number: Optional[int] = None
                    if isinstance(raw_key, int):
                        port_number = raw_key
                    elif isinstance(raw_key, str) and raw_key.isdigit():
                        port_number = int(raw_key)
                    elif isinstance(details, dict):
                        raw_port = details.get("port")
                        if isinstance(raw_port, int):
                            port_number = raw_port
                        elif isinstance(raw_port, str) and raw_port.isdigit():
                            port_number = int(raw_port)
                    if port_number is not None:
                        payload = dict(details) if isinstance(details, dict) else {}
                        payload.pop("port", None)
                        _merge(port_number, payload)

        for nested in value.values():
            if isinstance(nested, (dict, list, tuple, set)):
                candidates.extend(_collect_service_candidates(nested))

    elif isinstance(value, (list, tuple, set)):
        for item in value:
            candidates.extend(_collect_service_candidates(item))
    elif isinstance(value, int):
        _merge(value, {})
    elif isinstance(value, str) and value.isdigit():
        _merge(int(value), {})

    deduped: Dict[int, Dict[str, Any]] = {}
    ordered_ports: List[int] = []
    for entry in candidates:
        port = entry.get("port")
        if not isinstance(port, int):
            continue
        if port not in deduped:
            ordered_ports.append(port)
            deduped[port] = {k: v for k, v in entry.items() if k != "port"}
        else:
            deduped[port].update({k: v for k, v in entry.items() if k != "port"})

    return [{"port": port, **deduped[port]} for port in ordered_ports]


def _extract_open_ports(recon_steps: "OrderedDictType[str, Any]") -> List[int]:
    ports: List[int] = []
    active_data = recon_steps.get("active_scanning")
    if isinstance(active_data, dict):
        ports.extend(_collect_port_numbers(active_data))
    elif isinstance(active_data, list):
        for entry in active_data:
            ports.extend(_collect_port_numbers(entry))
    return sorted(set(ports))


def _extract_target_metadata(
    recon_steps: "OrderedDictType[str, Any]", default_target: str
) -> Dict[str, Any]:
    metadata: Dict[str, Any] = {"name": default_target}
    host_info = recon_steps.get("host_info")
    if isinstance(host_info, dict):
        metadata.update(host_info)
        hostname = host_info.get("hostname")
        if isinstance(hostname, str) and hostname:
            metadata["name"] = hostname

    identity_info = recon_steps.get("identity_info")
    if isinstance(identity_info, dict):
        metadata["identity"] = identity_info
    return metadata


def _resolve_target_identifier(target: str, external_ip_target: Optional[str]) -> str:
    return external_ip_target or target


def _simulate_privilege_escalation(
    target: str,
    external_ip_target: Optional[str],
    accounts: Optional[Sequence[str]] = None,
    os_hint: Optional[str] = None,
) -> Dict[str, Any]:
    checks = [
        {
            "name": "sudo_no_password",
            "status": "pass",
            "details": "No password-less sudo entries detected.",
        },
        {
            "name": "world_writable_binaries",
            "status": "warn",
            "details": "Writable service binaries require review.",
        },
        {
            "name": "setuid_audit",
            "status": "pass",
            "details": "Setuid binaries follow baseline expectations.",
        },
    ]
    return {
        "target": _resolve_target_identifier(target, external_ip_target),
        "operating_system": os_hint or "linux",
        "accounts_reviewed": list(accounts or ("root", "admin")),
        "checks": checks,
        "potential_paths": [entry for entry in checks if entry["status"] == "warn"],
    }


def _simulate_misconfiguration_audit(
    target: str,
    external_ip_target: Optional[str],
    services: Optional[Sequence[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    evaluated_services = list(services or ()) or [
        {"service": "ssh", "port": 22},
        {"service": "http", "port": 80},
    ]
    findings: List[Dict[str, Any]] = []
    for service in evaluated_services:
        name = service.get("service") or service.get("name") or "unknown"
        port = service.get("port") or service.get("service_port")
        finding = {
            "service": name,
            "port": port,
            "status": "review",
            "notes": "Baseline hardening checks queued.",
        }
        if str(name).lower() in {"ssh", "rdp"}:
            finding.update(
                {
                    "status": "warn",
                    "notes": "Weak authentication policies detected.",
                }
            )
        findings.append(finding)
    return {
        "target": _resolve_target_identifier(target, external_ip_target),
        "findings": findings,
    }


def _simulate_default_credentials(
    target: str,
    external_ip_target: Optional[str],
    credential_inventory: Optional[Dict[str, Sequence[str]]] = None,
) -> Dict[str, Any]:
    inventory = credential_inventory or {
        "ssh": ["root:toor", "admin:admin"],
        "http": ["admin:password"],
    }
    exposed = [
        {"service": service, "credential": combo}
        for service, combos in inventory.items()
        for combo in combos
    ]
    recommendations = [
        {
            "service": entry["service"],
            "action": "Rotate credentials",
            "credential": entry["credential"],
        }
        for entry in exposed
    ]
    return {
        "target": _resolve_target_identifier(target, external_ip_target),
        "default_credentials": exposed,
        "recommendations": recommendations,
    }


def _simulate_backdoor_setup(
    target: str,
    external_ip_target: Optional[str],
    transport: str = "reverse_https",
    listen_port: int = 4444,
    password: Optional[str] = None,
) -> Dict[str, Any]:
    config = craft_backdoor_config(transport, port=listen_port, password=password)
    verification = verify_backdoor(config, heartbeat=True)
    return {
        "configuration": config,
        "verification": verification,
        "target": _resolve_target_identifier(target, external_ip_target),
    }


def _simulate_command_and_control(
    target: str,
    domain_target: Optional[str],
    external_ip_target: Optional[str],
    beacon_interval: int = 60,
    channels: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    selected_channels = list(channels or ("https", "dns"))
    controller = {
        "host": domain_target or _resolve_target_identifier(target, external_ip_target),
        "beacon_interval_seconds": beacon_interval,
        "channels": selected_channels,
    }
    agents = [
        {
            "id": "agent-1",
            "channel": selected_channels[0],
            "status": "listening",
        }
    ]
    return {"controller": controller, "agents": agents}


def _simulate_monitoring_deployment(
    target: str,
    external_ip_target: Optional[str],
    tools: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    selected_tools = list(tools or ("osquery", "filebeat"))
    deployments = [
        {
            "tool": tool,
            "status": "deployed",
            "target": _resolve_target_identifier(target, external_ip_target),
        }
        for tool in selected_tools
    ]
    return {"deployments": deployments, "total": len(deployments)}


def _simulate_artifact_cleanup(
    target: str,
    external_ip_target: Optional[str],
    artifacts: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    removal_targets = list(artifacts or ("/tmp/payload.bin", "/var/log/auth.log.bak"))
    removed = [
        {"path": path, "status": "removed"}
        for path in removal_targets
    ]
    return {
        "target": _resolve_target_identifier(target, external_ip_target),
        "removed_artifacts": removed,
        "removed_count": len(removed),
    }


def _simulate_temp_cleanup(
    temp_directories: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    directories = list(temp_directories or ("/tmp", "/var/tmp"))
    cleaned = [
        {"directory": directory, "files_removed": 5}
        for directory in directories
    ]
    return {"cleaned_directories": cleaned, "total_directories": len(cleaned)}


def _simulate_timestamp_reset(
    files: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    baseline_files = list(files or ("/etc/passwd", "/etc/shadow"))
    adjustments = [
        {"file": file_path, "timestamp": "1970-01-01T00:00:00Z"}
        for file_path in baseline_files
    ]
    return {"adjusted_files": adjustments, "total_files": len(adjustments)}


def perform_test(
    scan_task_id: int,
    target: str,
    scan_type: str,
    domain_target: Optional[str] = None,
    external_ip_target: Optional[str] = None,
    steps: Optional[List[str]] = None,
    context: Optional[Dict[str, Any]] = None,
    ports: Optional[Union[str, Iterable[int]]] = None,
) -> Dict[str, Dict[str, Any]]:
    """Execute the end-to-end engagement pipeline for a scan task."""

    steps = steps or []
    context = context or {}
    requested_ports = _normalise_port_spec(ports)

    persisted_steps: set[str] = set()
    approved_entries = load_approved_targets()
    normalised_entries = normalise_approved_targets(approved_entries)

    def _ensure_phase_authorized(phase_identifier: str) -> None:
        nonlocal normalised_entries
        try:
            normalised_entries = ensure_targets_authorized(
                phase_identifier,
                {
                    'network_target': target,
                    'domain_target': domain_target,
                    'external_ip_target': external_ip_target,
                },
                normalised_entries=normalised_entries,
            )
        except TargetAuthorizationError as exc:
            message = "; ".join(exc.errors)
            logger.warning(
                "Blocked phase %s for scan_task_id=%s: %s",
                phase_identifier,
                scan_task_id,
                message,
            )
            record_audit_event(
                {
                    'event': 'target_validation_failed',
                    'stage': phase_identifier,
                    'scan_task_id': scan_task_id,
                    'scan_type': scan_type,
                    'target': target,
                    'domain_target': domain_target,
                    'external_ip_target': external_ip_target,
                    'reason': message,
                    'rejected_targets': exc.rejected_targets,
                }
            )
            raise

    def _store_phase_result(step_name: str, data: Any) -> None:
        if step_name in persisted_steps:
            return
        try:
            serialized = json.dumps(data, default=str)
        except TypeError:
            serialized = json.dumps(str(data))
        db.session.add(
            PenTestResult(scan_task_id=scan_task_id, step=step_name, results=serialized)
        )
        db.session.commit()
        persisted_steps.add(step_name)

    recon_context = context.get("recon")
    if isinstance(recon_context, OrderedDict):
        ordered_context: "OrderedDictType[str, Any]" = recon_context  # type: ignore[assignment]
    elif isinstance(recon_context, dict):
        ordered_context = OrderedDict(recon_context.items())
    else:
        ordered_context = OrderedDict()

    recon_results: "OrderedDictType[str, Any]" = OrderedDict()
    recon_steps_detail: List[Dict[str, Any]] = []

    _ensure_phase_authorized('phase.Reconnaissance')

    for step_name, payload in ordered_context.items():
        _ensure_phase_authorized(f'step.{step_name}')
        recon_results[step_name] = payload
        recon_steps_detail.append({"step": step_name, "results": payload})

    for step in steps:
        if step in recon_results:
            continue

        _ensure_phase_authorized(f'step.{step}')

        if step == "active_scanning":
            try:
                data = scan_ip_blocks(
                    target,
                    "ping",
                    ports=requested_ports or None,
                )
            except Exception as exc:  # pragma: no cover - depends on environment
                data = {"error": str(exc)}
        elif step == "host_info":
            try:
                data = gather_all_info(external_ip_target or target)
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "identity_info":
            try:
                data = gather_identity_info(domain_target or target)
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "network_info":
            try:
                data = gather_network_info(domain_target)
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "phishing_info":
            try:
                data = phishing_for_info(domain_target or target)
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "dns_enum":
            try:
                data = perform_dns_enumeration(domain_target or target)
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "whois":
            try:
                data = unified_domain_lookup(domain_target or target)
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "vuln_scan":
            try:
                inferred_ports = (
                    _extract_open_ports(recon_results)
                    or requested_ports
                    or [80, 443]
                )
                services = {
                    port: {
                        "status": "open",
                        "protocol": "tcp",
                        "source": "perform_test",
                    }
                    for port in inferred_ports
                }
                scanner = Scanning()
                data = scanner.vulnerability_scan(external_ip_target or target, services)
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "exploit":
            try:
                metadata = _extract_target_metadata(
                    recon_results, external_ip_target or target
                )
                vuln_source = recon_results.get("vuln_scan") or {}
                vulnerabilities = []
                if isinstance(vuln_source, dict):
                    vulnerabilities = vuln_source.get("vulnerabilities", [])
                plan = build_exploit_plan(metadata, vulnerabilities)
                payload = compose_payload(plan, "shell")
                delivery = deliver_payload(payload, ["https", "ssh", "ftp"])
                data = {
                    "exploit_plan": plan,
                    "payload": payload,
                    "delivery": delivery,
                }
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "privilege_escalation":
            try:
                data = _simulate_privilege_escalation(
                    target, external_ip_target, accounts=None, os_hint=None
                )
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "misconfiguration_audit":
            try:
                data = _simulate_misconfiguration_audit(
                    target,
                    external_ip_target,
                    services=recon_results.get("service_enumeration"),
                )
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "default_credentials":
            try:
                data = _simulate_default_credentials(target, external_ip_target)
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "persistence":
            try:
                method = "ssh"
                exploit_data = recon_results.get("exploit")
                if isinstance(exploit_data, dict):
                    method = exploit_data.get("delivery", {}).get("channel", method)
                config = craft_backdoor_config(method)
                verification = verify_backdoor(config)
                data = {"configuration": config, "verification": verification}
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "backdoor_setup":
            try:
                data = _simulate_backdoor_setup(target, external_ip_target)
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "command_and_control":
            try:
                data = _simulate_command_and_control(
                    target, domain_target, external_ip_target
                )
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "monitoring":
            try:
                data = _simulate_monitoring_deployment(target, external_ip_target)
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "cover_tracks":
            try:
                exploit_data = recon_results.get("exploit") or {}
                delivery = exploit_data.get("delivery", {}) if isinstance(exploit_data, dict) else {}
                log_lines = [
                    f"Delivered payload via {delivery.get('channel', 'unknown')}",
                    f"Delivery status: {delivery.get('status', 'unknown')}",
                    "Connection closed",
                ]
                keywords = ["delivered", "status"]
                suspicious = detect_log_entries(log_lines, keywords=keywords)
                cleaned = clean_log_entries(log_lines, keywords=keywords)
                data = {"suspicious": suspicious, "cleaned": cleaned}
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "artifact_cleanup":
            try:
                data = _simulate_artifact_cleanup(target, external_ip_target)
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "temp_cleanup":
            try:
                data = _simulate_temp_cleanup()
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        elif step == "timestamp_reset":
            try:
                data = _simulate_timestamp_reset()
            except Exception as exc:  # pragma: no cover
                data = {"error": str(exc)}
        else:
            data = {"error": f"Unknown step '{step}'"}
        recon_results[step] = data
        recon_steps_detail.append({"step": step, "results": data})

    open_ports = _extract_open_ports(recon_results)
    if not open_ports:
        open_ports = requested_ports or [80, 443]

    target_ip = external_ip_target or target

    service_candidates = _collect_service_candidates(recon_results.get("active_scanning"))
    if service_candidates:
        enumerated_services = enumerate_services(target_ip, service_candidates)
    else:
        enumerated_services = enumerate_services(
            target_ip,
            [{"port": port, "status": "open", "protocol": "tcp"} for port in open_ports],
        )

    if not enumerated_services and open_ports:
        enumerated_services = {
            port: {
                "status": "open",
                "protocol": "tcp",
                "service_name": "unknown",
                "banner": None,
                "version": None,
                "source": "service_enumeration",
            }
            for port in open_ports
        }

    recon_phase = {
        "phase": "Reconnaissance",
        "summary": f"Completed {len(recon_steps_detail)} reconnaissance steps.",
        "steps": recon_steps_detail,
        "artifacts": {
            "open_ports": open_ports,
            "target_metadata": _extract_target_metadata(
                recon_results, external_ip_target or target
            ),
            "services": enumerated_services,
        },
    }
    _store_phase_result("phase.Reconnaissance", recon_phase)

    services = {
        port: {
            **details,
            "status": details.get("status", "open"),
            "protocol": details.get("protocol", "tcp"),
            "source": details.get("source", "recon"),
        }
        for port, details in enumerated_services.items()
    }
    if not services:
        services = {
            port: {"status": "open", "protocol": "tcp", "source": "recon"}
            for port in open_ports
        }

    _ensure_phase_authorized('phase.Scanning')

    scanning_manager = Scanning()
    vulnerability_results = scanning_manager.vulnerability_scan(target_ip, services)

    scanning_phase = {
        "phase": "Scanning",
        "summary": (
            f"Analysed {len(services)} services derived from reconnaissance."
            if services
            else "No services available from reconnaissance data."
        ),
        "services": services,
        "vulnerability_results": vulnerability_results,
    }
    _store_phase_result("phase.Scanning", scanning_phase)

    _ensure_phase_authorized('phase.GainingAccess')

    exploit_plan = build_exploit_plan(
        recon_phase["artifacts"]["target_metadata"],
        vulnerability_results.get("vulnerabilities", []),
    )
    payload = compose_payload(exploit_plan, "shell")
    delivery_result = deliver_payload(payload, ["https", "ssh", "ftp"])

    gaining_phase = {
        "phase": "Gaining Access",
        "summary": exploit_plan.get("summary", "No exploit plan generated."),
        "exploit_plan": exploit_plan,
        "payload": payload,
        "delivery": delivery_result,
    }
    _store_phase_result("phase.GainingAccess", gaining_phase)

    _ensure_phase_authorized('phase.MaintainingAccess')

    persistence_method = delivery_result.get("channel", "ssh")
    backdoor_config = craft_backdoor_config(str(persistence_method))
    backdoor_status = verify_backdoor(backdoor_config)
    maintaining_phase = {
        "phase": "Maintaining Access",
        "summary": (
            "Backdoor verified as reachable"
            if backdoor_status.get("reachable")
            else "Backdoor verification indicates limited access"
        ),
        "configuration": backdoor_config,
        "verification": backdoor_status,
        "privilege_escalation": recon_results.get("privilege_escalation"),
        "misconfiguration": recon_results.get("misconfiguration_audit"),
        "default_credentials": recon_results.get("default_credentials"),
        "backdoor": recon_results.get("backdoor_setup"),
        "command_and_control": recon_results.get("command_and_control"),
        "monitoring": recon_results.get("monitoring"),
    }
    _store_phase_result("phase.MaintainingAccess", maintaining_phase)

    _ensure_phase_authorized('phase.CoveringTracks')

    log_lines = [
        f"Delivered payload via {delivery_result.get('channel', 'unknown')}",
        f"Open ports analysed: {', '.join(str(port) for port in open_ports)}",
        "Normal operation entry",
    ]
    keywords = ["delivered", "open ports"]
    suspicious = detect_log_entries(log_lines, keywords=keywords)
    cleaned = clean_log_entries(log_lines, keywords=keywords)
    covering_phase = {
        "phase": "Covering Tracks",
        "summary": f"Removed {cleaned.get('removed_count', 0)} artefacts from logs.",
        "suspicious": suspicious,
        "cleaned_logs": cleaned,
        "artifact_cleanup": recon_results.get("artifact_cleanup"),
        "temp_cleanup": recon_results.get("temp_cleanup"),
        "timestamp_reset": recon_results.get("timestamp_reset"),
    }
    _store_phase_result("phase.CoveringTracks", covering_phase)

    _ensure_phase_authorized('phase.Reporting')

    report = merge_phase_results(
        [recon_phase, scanning_phase, gaining_phase, maintaining_phase, covering_phase]
    )
    reporting_phase = {
        "phase": "Reporting",
        "summary": report.get("overall_status", "unknown"),
        "report": report,
    }
    _store_phase_result("phase.Reporting", reporting_phase)

    return {
        "recon": recon_phase,
        "scanning": scanning_phase,
        "gaining_access": gaining_phase,
        "maintaining_access": maintaining_phase,
        "covering_tracks": covering_phase,
        "reporting": reporting_phase,
    }


def generate_summary(
    scan_task_id: int, scan_type: str, results: Dict[str, Dict[str, Any]]
) -> Dict[str, Union[str, int]]:
    """Create a basic summary for a scan task.

    Args:
        scan_task_id: Identifier of the scan task.
        scan_type: Type of scan executed.
        results: Aggregated results returned by :func:`perform_test`.

    Returns:
        Dictionary containing summary information including a timestamp.
    """
    reporting = results.get('reporting', {}) if isinstance(results, dict) else {}
    overall_status = reporting.get('report', {}).get('overall_status') if isinstance(reporting, dict) else None
    summary_text = reporting.get('summary') if isinstance(reporting, dict) else None

    summary = {
        'scan_task_id': scan_task_id,
        'scan_type': scan_type,
        'summary': summary_text or 'Summary of the penetration test',
        'overall_status': overall_status or 'unknown',
        'timestamp': datetime.utcnow().isoformat(),
    }
    return summary
