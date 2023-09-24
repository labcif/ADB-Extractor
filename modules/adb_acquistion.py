import os
import shutil
import subprocess
import gzip
import time
from datetime import datetime
import modules.sha_hashes as sha_hashes
import modules.utils as utils


class Bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


USER = 0


def print_message(callback, message, type="info"):
    if callback is not None:
        callback(message)
    else:
        if type == "ok":
            print(Bcolors.OKGREEN + message)
            print(Bcolors.ENDC)
        elif type == "error":
            print(Bcolors.FAIL + message)
            print(Bcolors.ENDC)
        elif type == "info":
            print(Bcolors.OKBLUE + message)
        else:
            print(Bcolors.ENDC)
    time.sleep(1)


def get_acquistion(APP, DEVICE, DATA, callback=None, folder=''):
    # check if folder exists
    if folder != '':
        if not os.path.exists(folder):
            print_message(callback, "[ERROR] Folder does not exist!", "error")
            print_message(callback, "[ERROR] Exiting...", "error")
            return
    if DEVICE == "-e":
        print_message(callback, "[Info ] Acquiring from device: emulator")
        CMD = "su 0"
        END = ""
        DEVNAME = "emu"
    elif DEVICE == "-d":
        print_message(callback, "[Info ] Acquiring from device: USB")
        CMD = "su -c '"
        END = "'"
        DEVNAME = "usb"
    else:
        print_message(callback, "[ERROR] Device not supported!", "error")
        return

    if os.name == 'nt':
        print_message(callback, "[Info ] Host OS: Windows")
        SHELL = False
        ADB = subprocess.run("where adb", shell=True, capture_output=True)
        ADB = ADB.stdout.decode("utf-8").strip()

        # ADB = os.popen('where adb').read().strip()
        print_message(callback, "[Info ] Checking if " + APP + " exists...")
        IsDir = subprocess.run(ADB + " " + DEVICE + " shell pm list packages | findstr " + APP, stdout=subprocess.PIPE,
                               shell=True)

        if IsDir.returncode == 0:
            print_message(callback, "[Info ] Yes!")
        else:
            print_message(callback, "[ERROR] " + APP + " does not exist!", "error")
            print_message(callback, "[ERROR] Exiting...", "error")
            return

        print_message(callback, "[Info ] Getting application version...")

        VERSION = subprocess.run(ADB + " " + DEVICE + " shell pm dump " + APP + " | findstr versionName", shell=True,
                                 capture_output=True)

    else:
        print_message(callback, "[Info ] Host OS: POSIX")
        SHELL = True
        ADB = subprocess.run("which adb", shell=True, capture_output=True)
        ADB = ADB.stdout.decode("utf-8").strip()

        print_message(callback, "[Info ] Checking if " + APP + " exists...")
        IsDir = subprocess.run(ADB + " " + DEVICE + " shell pm list packages | grep " + APP, stdout=subprocess.PIPE,
                               shell=True)

        if IsDir.returncode == 0:
            print_message(callback, "[Info ] Yes!")
        else:
            print_message(callback, "[ERROR] " + APP + " does not exist!", "error")
            print_message(callback, "[ERROR] Exiting...", "error")
            return

        print_message(callback, "[Info ] Getting application version...")

        VERSION = subprocess.run(ADB + " " + DEVICE + " shell pm dump " + APP + " | grep versionName", shell=True,
                                 capture_output=True)

    VERSION = VERSION.stdout.decode("utf-8").strip()
    VERSION = VERSION.split("=")[1]

    print_message(callback, "[Info ] Getting Android Version...")

    ANDROID = subprocess.run(ADB + " " + DEVICE + " shell getprop ro.build.version.release", shell=True,
                             capture_output=True)
    ANDROID = ANDROID.stdout.decode("utf-8").strip()

    FILENAME = APP + "-v" + str(VERSION) + "-" + DATA + "--" + DEVNAME + str(ANDROID) + "-u" + str(
        USER) + "--" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".tar"

    OUTPUT_FOLDER = FILENAME[:-4]
    #remove \r\n from the string
    OUTPUT_FOLDER = utils.sanitize_filename(OUTPUT_FOLDER)
    if folder != '':
        OUTPUT_FOLDER = folder + "/" + OUTPUT_FOLDER
    OUTPUT_FILE = OUTPUT_FOLDER + "/" + "sha256_hashes.txt"
    # create the folder
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    print_message(callback, "[Info ] " + APP + " version: " + str(VERSION))
    print_message(callback, "[Info ] Android version: " + str(ANDROID))

    print_message(callback, "[Info ] Copying data from " + APP + " version " + VERSION + " ...")

    if DATA == "private" or DATA == "public":
        if DATA == "private":
            print_message(callback, "[Info ] Acquiring private data")
            # Primary method used to copy the data from the application
            # In windows this process was better when dealing with threads such as in the GUI
            if callback is not None and os.name == 'nt':
                subprocess.run(
                    ADB + " " + DEVICE + " shell " + CMD + " tar -cvzf /sdcard/Download/" + FILENAME + " /data/data/" + APP + END,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            else:
                # Method used in the bash script to copy the data from the application
                # Check for filename with spaces
                subprocess.run(ADB + " " + DEVICE + " shell " + CMD + " find /data/user_de/" + str(
                    USER) + "/" + APP + " -print0 | tee /sdcard/Download/" + FILENAME + ".1.txt " + END,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=SHELL)
                subprocess.run(ADB + " " + DEVICE + " shell " + CMD + " find /data/user/" + str(
                    USER) + "/" + APP + " -print0 | tee /sdcard/Download/" + FILENAME + ".2.txt " + END,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=SHELL)
                subprocess.run(
                    ADB + " " + DEVICE + " shell " + CMD + " tar -cvzf /sdcard/Download/" + FILENAME + " -T /sdcard/Download/" + FILENAME + ".1.txt " + "-T /sdcard/Download/" + FILENAME + ".2.txt " + END,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

        elif DATA == "public":
            print_message(callback, "[Info ] Acquiring public data")
            # Primary method used to copy the data from the application
            # In windows this process was better when dealing with threads such as in the GUI
            if callback is not None and os.name == 'nt':
                subprocess.run(
                    ADB + " " + DEVICE + " shell " + CMD + " tar -cvzf /sdcard/Download/" + FILENAME + " /storage/emulated/0/Android/data/" + APP + END,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            else:
                # Method used in the bash script to copy the data from the application
                # Check for filename with spaces
                subprocess.run(
                    ADB + " " + DEVICE + " shell " + CMD + " tar -cvzf /sdcard/Download/" + FILENAME + " /storage/emulated/0/Android/data/" + APP + END,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=SHELL)

        # Retrieve the file from the device and save it to the current directory and remove the file from the device
        print_message(callback, "[Info ] Copying to local storage ...")
        print_message(callback, "[Info ] Compressing " + FILENAME + " ...")
        subprocess.run(ADB + " " + DEVICE + " shell gzip /sdcard/Download/" + FILENAME, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True)
        print_message(callback, "[Info] Compressing Terminated.")

        print_message(callback, "[Info ] Copying to local storage ...")
        subprocess.run(ADB + " " + DEVICE + " pull /sdcard/Download/" + FILENAME + ".gz " + OUTPUT_FOLDER,
                       stdout=subprocess.DEVNULL,
                       shell=True)
        print_message(callback, "[Info ] Copy Terminated.")
        print("[Info ] Creating hashes file...")
        # Check if the command executed successfully
        # Save the output to a file

        # unzip the file
        print_message(callback, "[Info ] Unzipping file...")
        #remove \r\n from the string
        FILENAME = utils.sanitize_filename(FILENAME)
        with gzip.open(OUTPUT_FOLDER + "/" + FILENAME + ".gz", 'rb') as f_in:
            with open(OUTPUT_FOLDER + "/" + FILENAME, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        print_message(callback, "[Info ] Unzip Terminated.")
        # untar the file
        print_message(callback, "[Info ] Untaring file...")
        subprocess.run("tar -xvf " + OUTPUT_FOLDER + "/" + FILENAME + " -C " + OUTPUT_FOLDER, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True)
        print_message(callback, "[Info ] Untar Terminated.")
        print_message(callback, "[Info ] Calculating hashes.")
        sha_hashes.calculate_sha256_for_directory(OUTPUT_FOLDER, OUTPUT_FILE)

        print_message(callback, "[Info ] Cleaning acquisition files from phone...")
        subprocess.run(ADB + " " + DEVICE + " shell rm /sdcard/Download/" + FILENAME + ".gz", stdout=subprocess.DEVNULL,
                       shell=True)
        print_message(callback, "[Info ] Clean Terminated.")
        print_message(callback, "[Done ] Operation Completed with success, generated file: " + FILENAME + ".gz", "ok")

    elif DATA == "apk":
        print_message(callback, "[Info ] Copying apk file from " + APP + " ...")
        APK = subprocess.run(ADB + " " + DEVICE + " shell pm path " + APP, shell=True, capture_output=True)
        APK = APK.stdout.decode("utf-8").strip()
        APK = APK.split(":")[1]
        print_message(callback, "[Info ] APK: " + APK)

        subprocess.run(ADB + " " + DEVICE + " pull " + APK + " " + APP + ".apk", stdout=subprocess.DEVNULL, shell=True)
        os.rename("base.apk", APP + ".apk")
        # move the apk to the output folder
        os.rename(APP + ".apk", OUTPUT_FOLDER + "/" + APP + ".apk")

        # calculate sha256 of the apk
        print_message(callback, "[Info ] Calculating hashes...")
        sha256 = sha_hashes.calculate_sha256(OUTPUT_FOLDER + "/" + APP + ".apk")
        # save the sha256 to a file
        with open(OUTPUT_FILE, "w") as file:
            file.write(f"{sha256} *{APP}.apk\n")

        print_message(callback, "[Done ] Operation Completed with success, generated file: " + APP + ".apk", "ok")
    else:
        print_message(callback, "[ERROR] Invalid data type!", "error")
        return
