import os
import re
import socket
import subprocess
import sys
import time

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def update_retrofit_client(ip):
    retrofit_path = r"c:\Users\bharg\AndroidStudioProjects\final\app\src\main\java\com\simats\afinal\network\RetrofitClient.java"
    
    if not os.path.exists(retrofit_path):
        print(f"Warning: Could not find RetrofitClient.java at {retrofit_path}")
        return
        
    with open(retrofit_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Regex to find and replace the BASE_URL IP dynamically
    new_url = f'public static final String BASE_URL = "http://{ip}:8000/";'
    updated_content = re.sub(r'public\s+static\s+final\s+String\s+BASE_URL\s*=\s*"http://[^:]+:8000/";', new_url, content)
    
    if content != updated_content:
        with open(retrofit_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"[SUCCESS] Updated Android App (RetrofitClient) to use new Wi-Fi IP: {ip}")
    else:
        print(f"[INFO] Android App is already using the correct IP: {ip}")

def main():
    print("========================================")
    print("   AI DENTAL APP - BACKEND LAUNCHER     ")
    print("========================================\n")
    
    ip = get_local_ip()
    print(f"[*] Detected your current Local IP: {ip}")
    
    print("[*] Synchronizing Android App Network Configs...")
    update_retrofit_client(ip)
    
    print(f"\n[*] Starting Django Backend Server...")
    print(f"[*] The App will now connect to: http://{ip}:8000/\n")
    
    python_exec = sys.executable
    venv_python = r"venv\Scripts\python.exe"
    if os.path.exists(venv_python):
        python_exec = venv_python
        
    try:
        # Run server on all interfaces so the phone can reach it
        subprocess.run([python_exec, "manage.py", "runserver", "0.0.0.0:8000"])
    except KeyboardInterrupt:
        print("\n[*] Server stopped safely.")
    except Exception as e:
        print(f"\n[ERROR] Failed to start server: {e}")
        time.sleep(5)

if __name__ == "__main__":
    main()
