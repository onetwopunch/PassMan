PassMan (c) 2013 
developed by Ryan Canty jrcanty@gmail.com


This is a simple cross-platform, open source password manager application,
built using Python, including wx and passlib libraries.

INSTALL:
	Currently there is a Mac OSX app created with py2app that has all necessary libraries to run PassMan located at dist/PassMan.app. All you need to do is copy PassMan.app into your Application directory to install it. 

	If you would like to run PassMan from the python script itself on either Linux or Windows (neither have been tested yet), just make sure passlib and wx libraries are installed and in your PATH variable. Other than that, the only two files you need are passman.py and database.py

Usage:

Add new Password entry:
	1. Click New or (Ctrl/Cmd N)
	2. Fill out the description, username and password fields
	3. Click Add
	4. The Description field will be added to the list box

View Passwords:
	1. Click to highlight the description
	2. Click Show (Ctrl/Cmd S)
	3. The Username and Password will be shown respectively in the boxes
	to the right of the list box
	4. Click Clear (Ctrl/Cmd X) to clear the boxes
Delete:
	1. Click to highlight the description
	2. Click Delete

Change Password:
	1. Click File -> Change Password
	2. Follow the instructions to change password.

Forgotten Password:
	If you forget your password, and try 3 times to access PassMan, 
	you will be prompted to reset the application, deleting all your
	data and relaunch with a new password.
