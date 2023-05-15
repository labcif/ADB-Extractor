#!/usr/bin/python

# Author: Fabian Nunes
# Acquisition script to get the private folder application folder from and Android application in a rooted device or
# emulator, script based on the work of @mfrade and is bash implementation
# Example: python acquisition.py com.example.app -d emulator -t private
# Attention: In Windows, it is best to run the script in the PowerShell, additionaly use 7zip to extract the .tar.gz file, winrar does not work

import argparse
import modules.adb_acquistion as adb_acquistion

parser = argparse.ArgumentParser(description='Extract data from a device using ADB')
parser.add_argument('-a', '--app', help='Package name of the app', required=True)
parser.add_argument('-d', '--device', help='Device type', required=True, choices=["physical", "emulator"])
parser.add_argument('-t', '--type', help='Type of data to extract', required=True, choices=["private", "public", "apk"])
args = parser.parse_args()


if __name__ == "__main__":
    APP = args.app
    DEVICE = args.device
    if DEVICE == "physical":
        DEVICE = "-d"
    elif DEVICE == "emulator":
        DEVICE = "-e"
    DATA = args.type
    adb_acquistion.get_acquistion(APP, DEVICE, DATA)
