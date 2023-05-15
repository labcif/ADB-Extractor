import subprocess


def get_installed_packages():
    # Run the ADB command to list the installed packages
    cmd = "adb shell pm list packages -3"
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, error = proc.communicate()

    # Decode the output and split it into lines
    output = output.decode('utf-8').strip()
    lines = output.split('\n')

    # Extract the package names from the lines
    packages = []
    for line in lines:
        package = line.replace('package:', '')
        packages.append(package)

    # Return the list of package names
    return packages
