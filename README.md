# ADB-Extractor
Python tool to extract Private, Public and APK File from Android emulator or device using ADB.

## Requirements
- Python 3
- ADB
- Android Emulator or Device
- tar 
- gzip
- PysimpleGUI (optional)

## Installation

```bash
git clone 
cd ADB-Extractor
pip3 install -r requirements.txt
```

## Script Usage

```bash
python3 acquisition.py -a <package name> -d [emulator | physical] -t [public | private | apk]
```

```bash
python3 acquisition.py -a com.example.app -d emulator -t private
```

## GUI Usage

```bash
python3 acquisitionGUI.py
```

## OS
Tested on Linux, Windows and MacOS.

## Credits

Script based on the work of @mfrade and is bash implementation https://github.com/labcif/AndroidAcquisitionScript .
