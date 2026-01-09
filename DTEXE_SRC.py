import csv, os, pyautogui, time
from win32gui import FindWindow, GetWindowRect
import logging
from datetime import datetime
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import *
import os
from pynput import keyboard
import pygetwindow as gw
from pynput.keyboard import Controller, Key
from time import sleep
import subprocess
import threading
import queue
import time
import sys



logger = logging.getLogger(__name__)
logging.basicConfig(filename="dtexe.log", encoding='utf-8', level=logging.DEBUG)
# pyinstaller DTEXEV2.py --onefile -n ""

# GLOBALS Login
csv_file = "usr_list.csv"
config_file = "config.csv"
user_list = []
config_list = []

user_x = 437
user_y = 244

ok_x = 530
ok_y = 519

connect_x = 362
connect_y = 297

start_x = 177
start_y = 513


# Globals Hopper
WINDOW_TITLE = "Old Metin2" 
writer_keyboard = Controller()
sleep_time = 0.1

ch_selec_y = 60

ok_x_ch = -50
ok_y_ch = +85

paused = False

#login part
def imp_conf():
    channel_x = 0
    channel_y = 0
    with open (config_file, "r", newline="") as file:
        reader = csv.reader(file, delimiter=",", quotechar="|")
        for row in reader:
            config_list.append(row)
    for e in config_list:
        if e[0].lower() == "ch":
            ch = e[1].replace(" ", "")
        if e[0].lower() == "filepath":
            game_path = e[1].replace("\\", "\\\\")

        else:
            pass
    print("Conencting to CH " + ch)
    if ch == "1":
        channel_x = 530
        channel_y = 208
    if ch == "2":
        channel_x = 530
        channel_y = 227
    if ch == "3":
        channel_x = 530
        channel_y = 242
    if ch == "4":
        channel_x = 530
        channel_y = 259
    logger.info(f"config import to ch: {ch} with path: {game_path}")
    return channel_x, channel_y, game_path

def import_user_csv():
    with open (csv_file, "r", newline="") as file:
        reader = csv.reader(file, delimiter=",", quotechar="|")
        for row in reader:
            if len(row) == 2:
                user_list.append((row[0].replace(" ", ""), row[1].replace(" ", "")))
            else:
                logger.warning(f"Too many empty lines in {csv_file}")
    return 0

def open_window(game_path):
    os.system("start " + game_path)

def move_window(counter):
    no_accounts = len(user_list)
    screen_res = pyautogui.size()
    x_res = screen_res[0]
    y_res = screen_res[1]
    x_win = 800
    y_win = 600

    
    cols = divmod(x_res, x_win-200)[0]
    rows = divmod(no_accounts, cols)[0]+1

    row_offset = y_win/5
    col_offset = x_win-200

    cur_row, cur_col = divmod(counter, cols)

    window_rect = GetWindowRect(FindWindow(None, "Old Metin2"))
    if window_rect[0] > -200:
        x_offset = window_rect[0]
        y_offset = window_rect[1]
        pyautogui.moveTo(x= x_win/2 + x_offset, y = y_offset+10)
        pyautogui.dragTo(x=cur_col*col_offset+x_win/2, y=cur_row*row_offset , duration= 0.2, button="left")

def login(username, password, channel_x, channel_y):
    window_rect = GetWindowRect(FindWindow(None, "Old Metin2"))
    if window_rect[0] > -200:
        x_offset = window_rect[0]
        y_offset = window_rect[1]
        #channel selection
        pyautogui.moveTo(x = channel_x + x_offset, y = channel_y + y_offset)
        pyautogui.click(duration = 0.1, button='left')

        #confirm channel
        pyautogui.moveTo(x = ok_x + x_offset, y = ok_y + y_offset)
        pyautogui.click(duration = 0.1, button='left')

        #enter login
        pyautogui.moveTo(x = user_x + x_offset, y = user_y + y_offset)
        pyautogui.click(duration = 0.1, button='left')
        print("Logging in: " + username)
        pyautogui.write(username)
        pyautogui.press("tab")
        pyautogui.write(password)
        pyautogui.press("enter")
        time.sleep(3)
        pyautogui.moveTo(x = start_x + x_offset, y = start_y + y_offset)
        pyautogui.click(duration = 0.1, button='left')
        time.sleep(0.5)

def login_main():
    print(f"\n\n\n\n\n\n\n\n\n\n\n")
    logger.info(f'Start Time: {datetime.now()}')
    counter = 0
    import_user_csv()
    ch_x, ch_y, gp = imp_conf()
    for user in user_list:
        open_window(gp)
        if (counter < 15):
            time.sleep(1.5)
        if (counter >= 15):
            time.sleep(3)
        login(username=user[0],password=user[1],channel_x=ch_x, channel_y=ch_y)
        move_window(counter)
        counter +=1
        time.sleep(0.5)
    logger.info(f"Logged in {counter} accounts")
    logger.info(f'End Time: {datetime.now()}')

# hopper part
def start_channel_switcher(
    window_title="Old Metin2",
    sleep_time=0.025,
    ch_selec_y=60,
    ok_x_ch=-50,
    ok_y_ch=85
):
    writer_keyboard = Controller()
    paused = False

    def get_current_window():
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            print("Window not found")
            return None
        return windows[0]

    def jump2(x, y):
        win = get_current_window()
        if not win:
            return

        x_center = (win.width / 2) + win.left
        y_center = (win.height / 2) + win.top
        old_x, old_y = pyautogui.position()
        # Open menu
        writer_keyboard.press(Key.esc)
        sleep(0.1)
        writer_keyboard.release(Key.esc)
        sleep(0.2)

        # Select channel change
        pyautogui.moveTo(x_center, y_center + ch_selec_y)
        pyautogui.click(duration=0.1, button="left")
        sleep(sleep_time)

        # Select channel
        pyautogui.moveTo(x_center + x, y_center + y)
        pyautogui.click(duration=0.1, button="left")
        sleep(sleep_time)

        # Press OK
        pyautogui.moveTo(x_center + ok_x_ch, y_center + ok_y_ch)
        pyautogui.click(duration=0.1, button="left")
        pyautogui.moveTo(old_x, old_y)
        sleep(sleep_time)

    def hopp2(ch):
        channel_offsets = {
            1: (0, -30),
            2: (0, 0),
            3: (0, 30),
            4: (0, 60),
        }
        if ch in channel_offsets:
            jump2(*channel_offsets[ch])

    def on_press(key):
        nonlocal paused
        try:
            if key.char == 'p':
                paused = not paused
                print("Paused!" if paused else "Resumed!")
                return

            if paused:
                return

            if key.char == '.':
                win = get_current_window()
                if win:
                    print("Title:", win.title)
                    print("Position (x, y):", win.left, win.top)
                    print("Size (width, height):", win.width, win.height)
                x, y = pyautogui.position()
                print(f"MOUSEPOS: x {x}, y {y}")

            elif key.char == "5":
                print("CH1")
                hopp2(1)
            elif key.char == "6":
                print("CH2")
                hopp2(2)
            elif key.char == "7":
                print("CH3")
                hopp2(3)
            elif key.char == "8":
                print("CH4")
                hopp2(4)
            elif key.char == 'k':
                print("Quitting program...")
                return False

        except AttributeError:
            pass
    print(f"\n\n\n\n\n\n")
    print("Listening for keys... (press 'k' to quit and 'p' to pause)")
    print("Ch1 - 5\nCh2 - 6\nCh3 - 7\nCh4 - 8")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    return listener

class StdoutRedirector:
    def __init__(self, text_widget, log_queue):
        self.text_widget = text_widget
        self.queue = log_queue

    def write(self, message):
        if message.strip():
            self.queue.put(message)

    def flush(self):
        pass

class ScriptGui:
    def __init__(self, root):
        self.root = root
        self.root.title("DT Helper")
        self.hopp_process = None
        self.loging_proccess = None
        self.config_process = None
        self.usr_process = None
        tk.Button(root, text="Start Hopper", command=self.start_hopp).pack(pady=5)
        tk.Button(root, text="Start Login", command=self.start_login).pack(pady=5)
        tk.Button(root, text="Open Config", command=self.open_config).pack(pady=5)
        tk.Button(root, text="Open Userlist", command=self.open_usr_list).pack(pady=5)

        self.log_queue = queue.Queue()
        self.text_area = ScrolledText(root, state="disabled")
        self.text_area.pack(fill="both", expand=True)
        sys.stdout = StdoutRedirector(self.text_area, self.log_queue)
        sys.stderr = StdoutRedirector(self.text_area, self.log_queue)

        self.root.after(100, self.process_log_queue)
    
    def process_log_queue(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get()
            self.text_area.configure(state="normal")
            self.text_area.insert(tk.END, msg + "\n")
            self.text_area.configure(state="disabled")
            self.text_area.yview(tk.END)
        self.root.after(100, self.process_log_queue)


    def start_hopp(self):
        threading.Thread(target=start_channel_switcher, daemon=True).start()
    
    def start_login(self):
        if self.loging_proccess is None or self.loging_proccess.poll() is not None:
            self.loging_proccess = subprocess.Popen([login_main()])

    def open_config(self):
        if self.config_process is None or self.config_process.poll() is not None:
            self.config_process = subprocess.Popen([os.system("notepad.exe " + config_file)])
    
    def open_usr_list(self):
        if self.usr_process is None or self.usr_process.poll() is not None:
            self.usr_process= subprocess.Popen([os.system("notepad.exe " + csv_file)])

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = ScriptGui(root)
    root.mainloop()
