# Robot Framework Find Redundancy

## Motivation

When a Robot Framework project start to become big, and many tests scenarios are written, it is normal have duplicated keywords names.
The native Robot Framework lib does not detected automatically duplicated keywords, so it is a good idea to keep just one keyword per file
and also in the whole project, to avoid unnecessary code and also the code can diverges from one keyword logic to another one.


## Initial setup

To use this tool, it is just necessary to have Python installed in the system.


## Using the tool

One step needed is to give the project path to the script. To do this, open the script program
and look for the variable PROJECT_PATH.
Here you will replace the single quotes for the root path of your project.

Example in Windows system: `PROJECT_PATH = C:\\workspace\\automation_project`

Example in MacOS / Linux system: `PROJECT_PATH = /home/workspace/automation_project`

To use this tool, just open a command terminal and type: python find_redundancy.py

## Results

The results provided are the duplicated keywords and similar keywords, in a list form, through the command terminal.

Duplicated keywords example:

- Occurrences 2: Then welcome page should be open
- Occurrences 2: Toggle Airplane Mode
- Occurrences 3: Trust Application
- Occurrences 3: Trust Developer If Needed

Similar keywords example:

- ['Adb Shell Tab', 'Adb Tab', 'Adb Shell Enter']
- ['Allow All Permissions', 'Allow All Permission', 'Allow Permissions',]
