from screen_definition import definition
import os
import xml.etree.ElementTree as ET
import subprocess
import signal
import psutil
import sys
import time

def main():
    f= factor() # This is the factor of multiplication of the screen area.
    core_func(f)

def core_func(factor):
    c = coordinates(factor)
    user = os.getlogin()
    pid1, pid2 = pid_finder()
    reboot(user, c, pid1, pid2)

def factor():
    try:
        factor = float(sys.argv[1])
        return factor
    except (ValueError, IndexError):
        print('Please provide a valid numeric scaling factor as an argument. (Between 0 and 1)')
        sys.exit(1)

def coordinates(factor):
    w, h = definition()
    w, h = int(w), int(h)
    
    left = int(w - (w * factor) - (w * ((1 - factor) / 2)))
    top = int(h - (h * factor) - (h * ((1 - factor) / 2)))
    right = int(w - w * ((1 - factor) / 2))
    bottom = int(h - h * ((1 - factor) / 2))
    
    return [left, top, right, bottom]

def pid_finder():
    pid1, pid2 = 0, 0
    for proc in psutil.process_iter():
        try:
            if "TabletDriverCenter" in proc.name():
                pid1 = proc.pid
            elif "TabletDriverSetting" in proc.name():
                pid2 = proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if pid1 == 0 or pid2 == 0:
        run_tab_setting()
        time.sleep(1)
        return pid_finder() # Retry finding PIDs after attempting to start processes
    
    print(f"TabletDriverCenter.exe PID: {pid1}")
    print(f"TabletDriverSetting.exe PID: {pid2}")
    
    return pid1, pid2

def config_modifier(user, c):
    config_path = f"C:/Users/{user}/AppData/Local/VKTablet/config_user.xml"
    if not os.path.exists(config_path):
        print(f"Configuration file not found at {config_path}")
        sys.exit(1)
        
    config = ET.parse(config_path)
    root = config.getroot()
    tablet_model = 'VK_2FEB_0003'
    
    tablet_config = root.find(f'{tablet_model}')
    if tablet_config is None:
        print(f"Tablet model {tablet_model} not found in the configuration file.")
        sys.exit(1)
        
    screen_map = tablet_config.find('ScreenMap')
    screenareamode = tablet_config.find('ScreenId')

    left, top, right, bottom = screen_map.find('left'), screen_map.find('top'), screen_map.find('right'), screen_map.find('bottom')
    
    left.text, top.text, right.text, bottom.text = map(str, c)
    screenareamode.text = '1'
    
    config.write(config_path)

def run_tab_setting():
    subprocess.Popen([r'C:\Program Files\VKTablet\TabletDriverSetting.exe'])

def reboot(user, c, pid1, pid2):
    print('Rebooting processes.')
    try:
        os.kill(pid1, signal.SIGTERM)
        os.kill(pid2, signal.SIGTERM)
    except OSError as e:
        print(f"Error killing processes: {e}")
    
    config_modifier(user, c)
    run_tab_setting()
    
    _pid1, _pid2 = pid_finder()
    if (_pid1, _pid2) == (pid1, pid2):
        print(f"Failed to reboot. Old PIDs: {pid1}, {pid2} | New PIDs: {_pid1}, {_pid2}")
    else:
        print(f"Reboot successful. Old PIDs: {pid1}, {pid2} | New PIDs: {_pid1}, {_pid2}")

if __name__ == "__main__":
    main()