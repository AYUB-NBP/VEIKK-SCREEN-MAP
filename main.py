#IMPORTANT!
#MAKE SURE SCREEN MAPPING is set to "PART" an NOT "ALL",
#  otherwise ScreenMapping will be reset after restarting TabletDriverCenter/Setting
#  This program assumes you're running Windows 11 like me, I haven't test on Linux or others operating systems.

from scrn_map import definition
import os
import xml.etree.ElementTree as ET
import subprocess
import signal
import psutil
import time
import sys

#Change f to change scale factor.---> f now is an argument taken at launch.

def main():
    global gui_f
    gui_f = 0
    f = factor() or gui_f
    core_func(f)
    
def core_func(f):
    c = coordinates(f)
    user = os.getlogin()
    pid1 = 0  
    pid2 = 0
    pid1,pid2 = pid_finder(pid1, pid2)
    reboot(user,c,pid1,pid2)

def factor():
    try:
        f=float(sys.argv[1])
        return f
    except ValueError:
        print('Only a numeric argument should be given.')
        sys.exit(1)
    except IndexError:
        print('Please provide a scaling factor.')
        sys.exit(1)

def coordinates(f):
    w,h=definition() 
    w,h = int(w),int(h)
    
    
############################
    left = w-(w*f)-(w*((1-f)/2)) #x1
    top =  h-(h*f)-(h*((1-f)/2))#y1
    ###############
    right = w - w*((1-f)/2)  #x2
    bottom = h - h*((1-f)/2) #y2
############################
    coordinates = [left,top,right,bottom] #Order matching XML file for ease of use. (CRITICAL ORDER FOR CALCULATION)
    # We're basically calculating the coordinates of two paints that make a rectangle left,top:x,y and right,bottom :x,y,this data format is just to inject in XML.
    return coordinates

def pid_finder(pid1,pid2):

    for proc in psutil.process_iter():
        if "TabletDriverCenter" in proc.name():
            pid1 = proc.pid
        elif "TabletDriverSetting" in proc.name():
            pid2 = proc.pid

    if pid1 == 0:
        print('TabletDriverCenter not running.')
        run_tab_setting()
        time.sleep(1)
        pid_finder(pid1,pid2)
    elif pid2 == 0:
        print('TabletDriverSetting not running.')
        run_tab_setting()
        pid_finder(pid1,pid2)
    if pid1 != 0:
        print(f"TabletDriverCenter.exe is running.")
    if pid2 != 0:
        print(f"TabletDriverSetting.exe is running.")
    return pid1,pid2
    
def config_modifier(user, c):
    config = ET.parse(f"C:/Users/{user}/AppData/Local/VKTablet/config_user.xml")
    root = config.getroot()
    tablet_model = 'VK_2FEB_0003' #Name of child element that has my tablet's settings.
    #in my case, my tablet code name is VK_2FEB_0003, since only the values in that child element change when changing settings from VKtablet software.
    tablet_config = root.find(f'{tablet_model}') #XML element selection process
    screen_map = tablet_config.find('ScreenMap')
    left = screen_map.find('left')
    right = screen_map.find('right')
    top = screen_map.find('top')
    bottom = screen_map.find('bottom')

    ########### Elements modification #############
    for x in c:
        c[c.index(x)] = int(x)

    left.text = str(c[0])
    top.text = str(c[1])
    right.text = str(c[2])
    bottom.text = str(c[3])

    config.write(f"C:/Users/{user}/AppData/Local/VKTablet/config_user.xml")
        
#Next we should make sure the TabletDriverCenter.exe is rebooted to read the new XML config file.

# def run_tab_center():
#     process = subprocess.Popen([r'C:\Program Files\VKTablet\TabletDriverCenter.exe'])
#     return process
####### The above function was unnecessary because TabletDriverSetting.Exe launches TabletDriverCenter.exe automatically with it.
def run_tab_setting():
    process = subprocess.Popen([r'C:\Program Files\VKTablet\TabletDriverSetting.exe'])
    return process
    
def reboot(user,c,pid1,pid2):

    time.sleep(0.5)

    print('Rebooting processes.')
#Killing TabletDriverCenter.exe and TabletDriverSetting.exe
    try:
        os.kill(pid1, signal.SIGTERM)
    except OSError:
        print("Error: Can't kill TabletDriverCenter.exe.")
        main()

    time.sleep(0.5)

    try:
        os.kill(pid2, signal.SIGTERM)
    except OSError:
        "Error: Can't kill TabletDriverSetting.exe."
        main()
    #########
    config_modifier(user, c)
    #########
    run_tab_setting()

    #Success/Failure check

    #Since everytime a non-system process gets assigned a different PID, checking if it changed would tell us if it rebooted.
    _pid1,_pid2 = pid_finder(pid1,pid2)
    if (_pid1,_pid2) == (pid1,pid2):
        print("Old PIDs:",pid1,pid2,"\nNew PIDs:",_pid1,_pid2)
        print('Failed to reboot.')
    elif (_pid1,_pid2) != (pid1,pid2):
        print("Old PIDs:",pid1,pid2,"\nNew PIDs:",_pid1,_pid2)
        print('Reboot success.')
    # input('Press CTRL+D')

if __name__ == "__main__":
    main()
    
    
