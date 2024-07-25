## Veikk Drawing Tablet Screen Area Modifier
### Video Demo: https://youtu.be/h7LApZPbG7Q
### Description:
My project == script
, Veikk program == software

My project is a program that makes it possible to easily resize the screen area in which the Veikk A50 drawing tablet is usable. 

This provides better accuracy, especially for people with a big screen who can only focus their vision on part of its center, or to match the size of the drawing tablet to the drawing area on the screen for a 1:1 experience, and take advantage of being able to draw on canvas using the whole tablet’s work area.

 The program simply takes an input from the user (a percentage from 0 to 100 in the GUI or 0 to 1 as arguments in the command line version) and then makes a calculation to get new coordinates(left, top, right, bottom
) that make up the rectangle points, inject them in the configuration XML file of the drawing tablet's driver program located at “C:/Users/{user}/AppData/Local/VKTablet/config_user.xml” and then if the tablet’s software is running, it gets killed and rebooted in order for it to read the new screen area settings.

I have come across some challenges, as it took me a while to know that the software needed to be restarted.

Also, when implementing the script to reboot the software, I discovered that I didn’t need to run the two processes that make up the software (TabletDriverSettings.Exe, TabletDriverCenter.exe) after killing them. Running “TabletDriverSettings.Exe” was enough for it to run “TabletDriverCenter.exe”.

Another discovery I made was withing the config_user.xml file. The Tags used were a bit cryptic, I had to try different ones, until I found that that <VK_2FEB_0003> corresponds to my tablet model. 

I assume the tablet software is universal and works with multiple tablet models, so depending on the detected tablet it would read from the corresponding tag.

My script could hypothetically work on any windows 11 machine, since it dynamically retrieves the current OS user name and uses it as a value for a variable that is part of the configuration file directory path.

Additionally, the resolution of the screen is also retrieved using the module “screen_definition.py” thanks to the library “screeninfo”.

A big part of writing this script was troublshooting and coding defensively to guide the user and help me debug the code along the way.

I hope at least one person with the same tablet as me gets to use this script.

I could add some more features like an overlay showing the limits of the new screen area that can be activated using a toggle button or hotkey.

