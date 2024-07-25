## Veikk Drawing Tablet Screen Area Modifier
### Video Demo: https://youtu.be/h7LApZPbG7Q
### Description:
My project is a program that makes it possible to easily resize the screen area in which the drawing tablet is usable.
This provides better accuracy, especially for people with big screen that can only focus their vision on part of its centre, or to match the size of the drawing tablet to the drawing area on the screen.
The program simply takes an input from the user (a percentage from 0 to 100 in the GUI or 0 to 1 as arguments in the command line version) and then makes a calculation to get new coordinates, inject them in configuration XML file of the drawing tablet's driver program, then reboots that program to have it read the newly written settings and take effect.

