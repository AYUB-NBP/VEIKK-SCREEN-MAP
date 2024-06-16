#IMPORTANT!
#MAKE SURE SCREEN MAPPING is set to "PART" an NOT "ALL",
#  otherwise ScreenMapping with be reset at reboot to screen resolution

from Scrn_map import definition
import os
import xml.etree.ElementTree as ET
from subprocess import run
import signal
import psutil
import sys
import time

#Change f to change scale factor.

def main():
    c = coordinates()
    user = os.getlogin()

    pid1,pid2 = pid_finder()
    reboot(user,c,pid1,pid2)
    
      

def coordinates():
    w,h=definition() 
    w,h = int(w),int(h)
    f=0.8
############################
    top = (f*h)/2
    left = (f*w)/2
    bottom = h-(f*h)/2
    right = w- (f*w)/2
############################
    coordinates = [left,top,right,bottom] #Order matching XML file for ease of use.
    return coordinates

def pid_finder():
    pid1 = 0
    pid2 = 0
    process_name1 = "TabletDriverCenter"
    process_name2 = "TabletDriverSetting"
    for proc in psutil.process_iter():
        if process_name1 in proc.name():
            pid1 = proc.pid
        elif process_name2 in proc.name():
            pid2 = proc.pid
    print(pid1,pid2)
    return pid1,pid2
    

def config_modifier(user, c):
    config = ET.parse(f"C:/Users/{user}/AppData/Local/VKTablet/config_user.xml")
    root = config.getroot()
    tablet_model = 'VK_2FEB_0003'
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
    
def reboot(user,c,pid1,pid2):
    time.sleep(0.5)
    try:
        os.kill(pid1, signal.SIGILL)
    except OSError:
        run("C:/Program Files/VKTablet/TabletDriverCenter.exe")
        sys.exit(1)
    time.sleep(0.5)
    try:
        os.kill(pid2, signal.SIGILL)
    except OSError:
        run("C:/Program Files/VKTablet/TabletDriverSetting.exe")
        sys.exit(1)
    #########
    config_modifier(user, c)
    #########
    time.sleep(0.5)
    run("C:/Program Files/VKTablet/TabletDriverCenter.exe")
    time.sleep(0.5)
    run("C:/Program Files/VKTablet/TabletDriverSetting.exe")
    # input('Press CTRL+D')


if __name__ == "__main__":
    main()
    
    
