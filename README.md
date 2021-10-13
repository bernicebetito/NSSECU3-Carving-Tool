# NSSECU3-Carving-Tool
_A Data Carving Tool for Digital Forensics (NSSECU3)._\
Date Accomplished: September 22, 2021

## Use
This project finds and recovers files of different types.

## Pre-requisites
1. Python / Python3
  * Programming language used.
  * To download in **Linux**: `sudo apt-get install python3`
  * To download in **Windows**: [Python for Windows](https://www.python.org/downloads/windows/)
2. Curl
  * Command that allows the transfer (upload / download) of data using command line interface.
  * To download in **Linux**: `sudo apt-get install curl`
  * To download in **Windows**: [Curl for Windows](https://curl.se/windows/)
3. Pip
  * Tool which helps in installing packages written in Python.
  * To download in **Linux**: `sudo apt-get install pip`
  * To download in **Windows**: [Pip for Windows](https://pip.pypa.io/en/stable/installation/)
4. python-magic
  * Python library which can check file types.
  * To download in **Linux**: `sudo apt-get install libmagic1`
  * To download in **Windows**: `pip install python-magic-bin`

## Download
Download the project through the following commands:
* Linux:
``` sudo curl -O https://raw.githubusercontent.com/bernicebetito/NSSECU3-Carving-Tool/main/DATA-CARVING.py ```
* Windows:
``` curl -O https://raw.githubusercontent.com/bernicebetito/NSSECU3-Carving-Tool/main/DATA-CARVING.py ```

Once downloaded, the project can be used through the following commands:
* Linux: ` sudo python3 DATA-CARVING.py `
* Windows: ` python DATA-CARVING.py `

## Guide
Information would be asked from the user before recovery starts. This includes the name of the folder wherein the found files will be stored, file types to recover, path of the directory to be checked, number of threads to work on the recovery, and the end of the sector. Ensure that for Windows, the path of the directory must be of `\\.\C:` format.
