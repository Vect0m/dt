import csv, os, pyautogui, time
from win32gui import FindWindow, GetWindowRect
import logging
from datetime import datetime


logger = logging.getLogger(__name__)
logging.basicConfig(filename="dtexe.log", encoding='utf-8', level=logging.DEBUG)
# pyinstaller DTEXEV2.py --onefile -n ""

# GLOBALS
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

def main():
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


if __name__ == "__main__":
    main()