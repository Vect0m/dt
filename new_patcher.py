import requests
import os
from time import sleep
import subprocess
import sys
import urllib.request
import shutil

all_exe_list = []
HISTORY_FILE = "https://raw.githubusercontent.com/Vect0m/dt/refs/heads/main/versionhistory.txt"
PYTHON_FILE = "https://raw.githubusercontent.com/Vect0m/dt/refs/heads/main/test.py"
target_history = "versionshistory_temp.txt"
target_file = "com_temp.py"
exe_name = "dtexe"
VERSION = ""
VERSION_local = ""

REQUIRED_PACKAGES = ["win32gui", "pyautogui", "logging", "tkinter", "pynput", "pygetwindow"]  # Example packages

PYTHON_INSTALLER_URL = "https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe"
PYTHON_INSTALLER_PATH = os.path.join(os.getcwd(), "python_installer.exe")

def get_version():
    global VERSION
    with open (target_history, 'r', newline="\n") as file:
        lines = file.readlines()
        if lines:
            last_entry = lines[-1].strip()
            VERSION = last_entry
            return 1
        else:
            print("file is emptry")
            return 0
        
def check_version_update():
    response = requests.get(HISTORY_FILE)
    response.raise_for_status()
    with open(target_history, "wb") as f:
        f.write(response.content)

def check_local_version():
    global VERSION_local, exe_name
    filename = ""
    for name in os.listdir(os.getcwd()):
        if name.lower().endswith('.exe'):
            all_exe_list.append(name)

    if len(all_exe_list) < 2:
        VERSION_local = "0"
        return 0
    else:
        for e in all_exe_list:
            if exe_name in e:
                filename = e
        filename = filename.split('_')[1]
        filename = filename.split(".")
        VERSION_local = filename[0].split("v")[1] + "." + filename[1]
        return 1

def check_update_needed():
    global VERSION, VERSION_local

    print("Checking for updates...")
    check_version_update()
    check_local_version()
    get_version()
    if VERSION_local < VERSION:
        if VERSION_local == "0":
            print("Program not found")
            print("Installing...")
        else:
            print("Update Found")
        return True
    else:
        print("No Update Needed")
        return False

def download_update():
    response = requests.get(PYTHON_FILE)
    response.raise_for_status()
    with open(target_file, "wb") as f:
        f.write(response.content)
    print("Download complete...")

def make_new_exe():
    global exe_name, VERSION, VERSION_local
    if VERSION_local != "0":
        exe_name_old = exe_name + "_v" + str(VERSION_local) + ".exe"
        os.system(f"del {exe_name_old}")
    exe_name = exe_name + "_v" + str(VERSION) + ".exe"
    if VERSION != 0:
        cmd = f"PyInstaller {target_file} --onefile --log-level=WARN --distpath \"{os.getcwd()}\" -n {exe_name}"
        print(f"Compiling v{VERSION}...")
        os.system(cmd)
    else:
        print("Failed Building")

def clean():
    global exe_name, target_file, target_history
    os.system(f"del {exe_name}.spec")
    os.system(f"del {target_history}")
    os.system(f"del {target_file}")


def is_python_installed():
    try:
        # Try running 'python --version'
        subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        # Try running 'py --version' (Windows launcher)
        try:
            subprocess.run(["py", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except Exception:
            return False

def download_python_installer():
    print("Downloading Python installer...")
    urllib.request.urlretrieve(PYTHON_INSTALLER_URL, PYTHON_INSTALLER_PATH)
    print("Download complete.")

def install_python():
    print("Installing Python silently...")
    # /quiet for silent, InstallAllUsers=1 for all users, PrependPath=1 to add to PATH
    subprocess.run([
        PYTHON_INSTALLER_PATH,
        "/quiet", "InstallAllUsers=1", "PrependPath=1"
    ], check=True)
    print("Python installation complete.")

def ensure_pip():
    try:
        subprocess.run(["python", "-m", "ensurepip"], check=True)
    except Exception:
        print("Failed to ensure pip. Please check your Python installation.")

def install_packages(packages):
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            print(f"Package '{package}' is installed.")
        except Exception:
            print(f"Failed to install package: {package}")

def main():
    if not is_python_installed():
        print("Python not detected. Proceeding to download and install Python.")
        download_python_installer()
        install_python()
        ensure_pip()
        # Remove installer after installation
        if os.path.exists(PYTHON_INSTALLER_PATH):
            os.remove(PYTHON_INSTALLER_PATH)
    else:
        print("Python is already installed.")

    print("Ensuring required packages are installed...")
    install_packages(REQUIRED_PACKAGES)
    print("Python Setup complete!")

    # DT stuff
    global VERSION, VERSION_local
    if check_update_needed():
        download_update()
        make_new_exe()
        clean()
        print(f"\n\nDone")
        print(f"Updated from v{VERSION_local} to v{VERSION}")
        sleep(2)
    else:
        sleep(2)
        os.system(f"del {target_history}")    

if __name__ == "__main__":
    main()
