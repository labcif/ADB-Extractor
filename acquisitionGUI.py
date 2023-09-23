#!/usr/bin/python

# Author: Fabian Nunes
# Acquisition tool to get the private folder application folder from and Android application in a rooted device or
# emulator, script based on the work of @mfrade and is bash implementation
# This is the GUI version of the script and was made using PySimpleGUI
# Example: python acquisitionGUI.py
# Attention in case of module not found error in Windows, install the module with pip install PySimpleGUI

import PySimpleGUI as sg
import modules.find_packages as f_packages
import modules.adb_acquistion as adb_acquistion
import threading

# PySimpleGUI variables
title = 'ADB Extractor'
theme = sg.theme('DarkAmber')  # Add a touch of color

# Application variables
packages = ['']
APP = ''
DEVICE = ''
folder = ''


# Callback function to update the output
def update_output(text):
    window['-OUTPUT-'].print(text)


# Thread function that will occur in the background to extract the data
def extract_thread():
    DATA = []
    # Disable the extract button
    window['-EXTRACT-'].update(disabled=True)
    # Disable the package button
    window['-GETPACKAGES-'].update(disabled=True)
    # Disable the radio buttons
    window['physical'].update(disabled=True)
    window['emulator'].update(disabled=True)
    window['private'].update(disabled=True)
    window['public'].update(disabled=True)
    window['apk'].update(disabled=True)
    # Disable the package list
    window['-PACKAGES-'].update(disabled=True)
    # Disable the output
    window['-OUTPUT-'].update(disabled=True)
    # Disable the close button
    window['-EXIT-'].update(disabled=True)
    # Disable the folder button
    window['-FOLDER-'].update(disabled=True)
    # Disable the folder browse button
    window['Browse'].update(disabled=True)

    if values['private']:
        DATA.append('private')
    if values['public']:
        DATA.append('public')
    if values['apk']:
        DATA.append('apk')

    if values['physical']:
        DEVICE = '-d'
    elif values['emulator']:
        DEVICE = '-e'

    for data in DATA:
        adb_acquistion.get_acquistion(APP, DEVICE, data, update_output, folder)
        print('---NEXT Extraction---')
    window.write_event_value('-EXTRACTION-COMPLETED-', None)


# Part of the GUI with radio buttons to choose the device and the type of acquisition
options_layout = [
    [sg.Text('Device', size=(15, 1)), sg.Radio('Physical', "RADIO1", default=True, size=(10, 1), key='physical'),
     sg.Radio('Emulator', "RADIO1", size=(10, 1), key='emulator')],
    [sg.Text('Type', size=(15, 1)), sg.Checkbox('Private', default=True, size=(10, 1), key='private'),
     sg.Checkbox('Public', size=(10, 1), key='public'),
     sg.Checkbox('APK', size=(10, 1), key='apk')]
]

# Layout with the list of packages installed on the device

# Layout with the list of packages installed on the device
packages_layout = [
    [sg.Text('Packages Installed', size=(15, 1))],
    [sg.Listbox(values=packages, size=(350, 10), font=("Helvetica", 12), key='-PACKAGES-', enable_events=True)],
    [
        sg.Button('Get Packages', size=(15, 1), key='-GETPACKAGES-'),
        sg.Text('', size=(50, 1), key='-SELECTEDPACKAGE-'),
    ]
]

# Layout with the output of the script
output_layout = [
    [sg.Text('Output', size=(15, 1))],
    [sg.Output(size=(400, 10), font=("Helvetica", 12), key='-OUTPUT-')],
]

# Main layout
layout = [
    [
        sg.Push(),
        sg.Text('ADB Extractor', size=(30, 1), justification='center', font=("Helvetica", 25)),
        sg.Push(),
        #sg.Button('?', size=(1, 1), key='-INFO-'),
    ],
    [sg.VerticalSeparator(pad=((0, 0), (10, 10)))],
    *options_layout,
    [
        sg.Text("Output Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [sg.VerticalSeparator(pad=((0, 0), (10, 10)))],
    [
        sg.Push(),
        sg.Column(packages_layout, size=(350, 300)),
        sg.VSeperator(),
        sg.Column(output_layout, size=(400, 300)),
        sg.Push()
    ],
    [sg.VerticalSeparator(pad=((0, 0), (10, 10)))],
    [
        sg.Push(),
        sg.Button('Extract', size=(15, 1), key='-EXTRACT-'),
        sg.Button('Exit', size=(15, 1), key='-EXIT-'),
        sg.Push(),
        #sg.Text('LabCIF - 2023', size=(30, 1), justification='right', font=("Helvetica", 10)),
    ]
]

# Create the window
window = sg.Window(title, layout, finalize=True)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break
    elif event == '-GETPACKAGES-':
        packages = f_packages.get_installed_packages()
        window['-PACKAGES-'].update(packages)
        window['-SELECTEDPACKAGE-'].update('Packages Updated')
    elif event == '-PACKAGES-':
        APP = values['-PACKAGES-'][0]
        window['-SELECTEDPACKAGE-'].update(APP)
    elif event == '-FOLDER-':
        folder = values["-FOLDER-"]
    elif event == '-EXTRACT-':
        if APP == '':
            sg.popup_error('Select a package')
        else:
            # Clear the output
            window['-OUTPUT-'].update('')
            # Start the extraction thread
            threading.Thread(target=extract_thread).start()
    elif event == '-EXTRACTION-COMPLETED-':
        # Enable the extract button
        window['-EXTRACT-'].update(disabled=False)
        # Enable the package button
        window['-GETPACKAGES-'].update(disabled=False)
        # Enable the radio buttons
        window['physical'].update(disabled=False)
        window['emulator'].update(disabled=False)
        window['private'].update(disabled=False)
        window['public'].update(disabled=False)
        window['apk'].update(disabled=False)
        # Enable the package list
        window['-PACKAGES-'].update(disabled=False)
        # Enable the output
        window['-OUTPUT-'].update(disabled=False)
        # Enable the close button
        window['-EXIT-'].update(disabled=False)
        # Enable the folder button
        window['-FOLDER-'].update(disabled=False)
        # Enable the folder browse button
        window['Browse'].update(disabled=False)
        sg.popup('Extraction Completed')
    elif event == '-INFO-':
        sg.popup('ADB Extractor\n\n'
                 'This tool allows you to extract data from an Android device using ADB.\n\n'
                 'The tool is divided into two parts:\n'
                 '1. The first part allows you to select the device and the type of acquisition.\n'
                 '2. The second part allows you to select the package from which to extract the data.\n\n'
                 'If not specified the Output will be generated in the same folder as the tool.\n\n'
                 'Developed by @fabian-nunes as part of the LabCIF and is Master Thesis.\n\n'
                 'The tool is provided as is, without any warranty.\n\n')

window.close()
