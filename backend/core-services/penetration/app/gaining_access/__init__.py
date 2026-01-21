from .payload_generator import run_payload_generator
from .exploit_engine import run_exploit_engine
from .brute_force_attack import run_brute_force_attack
from .malware_threats import run_malware_threats
from .system_hacking import run_system_hacking
from .adaptive_exploit_engine import generate_adaptive_exploit
from .bespoke_virus_generator import generate_bespoke_virus
from .multi_vector_delivery import execute_multi_vector_attack

def run_gaining_access(target, steps=None, vulnerability_data=None, **kwargs):
    """
    Orchestrate all gaining access modules with adaptive exploitation capabilities.
    """
    results = {}
    steps = steps or [
        "payload_generator",
        "exploit_engine", 
        "brute_force_attack",
        "malware_threats",
        "system_hacking",
        "adaptive_exploit",
        "bespoke_virus",
        "multi_vector_attack"
    ]
    if "payload_generator" in steps:
        results["payload_generator"] = run_payload_generator(target)
    if "exploit_engine" in steps:
        results["exploit_engine"] = run_exploit_engine(target)
    if "brute_force_attack" in steps:
        results["brute_force_attack"] = run_brute_force_attack(target)
    if "malware_threats" in steps:
        results["malware_threats"] = run_malware_threats(target, **kwargs)
    if "system_hacking" in steps:
        results["system_hacking"] = run_system_hacking(target)
    # New adaptive capabilities
    if "adaptive_exploit" in steps and vulnerability_data:
        results["adaptive_exploit"] = generate_adaptive_exploit(
            target, vulnerability_data, kwargs.get('open_ports', {}), 
            kwargs.get('successful_creds'),
            conversational_ai=kwargs.get('conversational_ai')
        )
    
    if "bespoke_virus" in steps and vulnerability_data:
        results["bespoke_virus"] = generate_bespoke_virus(
            target, vulnerability_data, kwargs.get('open_ports', {}),
            kwargs.get('platform', 'windows')
        )
    
    if "multi_vector_attack" in steps and vulnerability_data:
        results["multi_vector_attack"] = execute_multi_vector_attack(
            target, vulnerability_data, kwargs.get('open_ports', {}),
            kwargs.get('successful_creds')
        )
    
    return results
