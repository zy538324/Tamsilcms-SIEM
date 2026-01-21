from .exploit_generation import generate_exploit
from .payload_delivery import deliver_payload

def run_system_hacking(target, scan_context=None, exploit_type="default", payload=None):
    """
    Orchestrate system hacking: generate exploit and deliver payload.
    """
    # If scan_context is passed as second parameter, use it properly
    if isinstance(scan_context, dict):
        # Extract vulnerability data to choose better exploit type
        vulnerabilities = scan_context.get('vulnerabilities', {}).get('vulnerabilities', [])
        if vulnerabilities:
            # Choose exploit based on discovered vulnerabilities
            for vuln in vulnerabilities:
                if vuln.get('port') == 445:
                    exploit_type = "smb_attack"
                    break
                elif vuln.get('port') == 80:
                    exploit_type = "web_shell_php"
                    break
    
    exploit = generate_exploit(target, exploit_type)
    delivery = deliver_payload(target, payload or exploit.get("payload"))
    return {
        "exploit": exploit,
        "payload_delivery": delivery,
        "summary": f"System hacking attempted on {target} using exploit '{exploit_type}'."
    }
