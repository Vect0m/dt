import requests
import os
from time import sleep


all_exe_list = []
HISTORY_FILE = "https://raw.githubusercontent.com/Vect0m/dt/refs/heads/main/versionhistory.txt"
PYTHON_FILE = "https://raw.githubusercontent.com/Vect0m/dt/refs/heads/main/test.py"
target_history = "versionshistory_temp.txt"
target_file = "com_temp.py"
exe_name = "dtexe"
VERSION = ""
VERSION_local = ""


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

def main():
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

