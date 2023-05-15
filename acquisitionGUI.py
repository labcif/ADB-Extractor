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
DATA = ''
folder = ''


def update_output(text):
    window['-OUTPUT-'].print(text)


def extract_thread():
    if APP == '':
        sg.popup_error('Select a package')
        return
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
        DATA = 'private'
    elif values['public']:
        DATA = 'public'
    elif values['apk']:
        DATA = 'apk'

    if values['physical']:
        DEVICE = '-d'
    elif values['emulator']:
        DEVICE = '-e'

    adb_acquistion.get_acquistion(APP, DEVICE, DATA, update_output, folder)
    window.write_event_value('-EXTRACTION-COMPLETED-', None)


# Part of the GUI with radio buttons to choose the device and the type of acquisition
options_layout = [
    [sg.Text('Device', size=(15, 1)), sg.Radio('Physical', "RADIO1", default=True, size=(10, 1), key='physical'),
     sg.Radio('Emulator', "RADIO1", size=(10, 1), key='emulator')],
    [sg.Text('Type', size=(15, 1)), sg.Radio('Private', "RADIO2", default=True, size=(10, 1), key='private'),
     sg.Radio('Public', "RADIO2", size=(10, 1), key='public'),
     sg.Radio('APK', "RADIO2", size=(10, 1), key='apk')]
]

# Layout with the list of packages installed on the device

packages_layout = [
    [sg.Text('Packages Installed', size=(15, 1))],
    [sg.Listbox(values=packages, size=(300, 10), font=("Helvetica", 14), key='-PACKAGES-', enable_events=True)],
    [
        sg.Button('Get Packages', size=(15, 1), key='-GETPACKAGES-'),
        sg.Text('', size=(50, 1), key='-SELECTEDPACKAGE-'),
    ]
]

output_layout = [
    [sg.Text('Output', size=(15, 1))],
    [sg.Output(size=(300, 10), font=("Helvetica", 14), key='-OUTPUT-')],
]

# Layout
layout = [
    [
        sg.Push(),
        sg.Text('ADB Extractor', size=(30, 1), justification='center', font=("Helvetica", 25)),
        sg.Push(),
        sg.Button('?', size=(1, 1), key='-INFO-'),
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
        sg.Column(packages_layout, size=(300, 300), vertical_scroll_only=True),
        sg.VSeperator(),
        sg.Column(output_layout, size=(400, 300), vertical_scroll_only=True),
    ],
    [sg.VerticalSeparator(pad=((0, 0), (10, 10)))],
    [
        sg.Push(),
        sg.Button('Extract', size=(15, 1), key='-EXTRACT-'),
        sg.Button('Exit', size=(15, 1), key='-EXIT-'),
        sg.Push()
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
