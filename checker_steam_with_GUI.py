import os
import sys

import time
from datetime import date
from threading import Thread

from tkinter import messagebox, ttk, scrolledtext, Tk, INSERT
from tkinter.ttk import Progressbar

import requests
from bs4 import BeautifulSoup

root = Tk()
style = ttk.Style(root)
root.tk.call('source', 'awthemes/awdark.tcl')
style.theme_use('awdark')

th = None
stop_process = False
root.title('SteamInvestChecker')


# Create main frame of GUI
def generate_frame():
    frame_name = ttk.Frame(root)
    frame_name.grid(row=0, column=0, sticky='news')
    return frame_name


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def create_start_buttons():
    generate_button(text_btn='Add item', width_btn=11, sticky_btn='nw', x_btn=0, y_btn=0, ix_btn=0,
                    iy_btn=0, command_btn=add_item)  # Create button "Add item"
    generate_button(text_btn=' Load', width_btn=3, x_btn=53, ix_btn=10, command_btn=load)  # Create button "Load"
    generate_button(text_btn='Calculate', width_btn=11, command_btn=multi_calculate, x_btn=77, ix_btn=12,
                    sticky_btn='nw')  # Create button "Calculate"
    generate_button(text_btn='Save', command_btn=save)  # Create button "Save"
    generate_button(text_btn='✕', width_btn=2, x_btn=105, y_btn=0, state_btn='disabled',
                    command_btn=stop_calculation_thread)  # Create button "✕"


result = []

data_menu = generate_frame()
data_menu.tkraise()


def generate_elements(data_menu, text_: str, font_name: str = 'Arial', font_size: int = 14, row_: int = 0,
                      column_: int = 0, sticky_: str = 'ns'):
    element_name = ttk.Label(data_menu, text=text_)
    element_name.grid(row=row_, column=column_, sticky=sticky_)


#  Function for creating entry elements on main frame
def generate_entry(width_: int = 9, row_: int = 1, column_: int = 0):
    entry_name = ttk.Entry(data_menu, width=width_)
    entry_name.grid(row=row_, column=column_)
    return entry_name


def generate_button(text_btn: str, width_btn: int = 2, state_btn: str = "normal", command_btn=None, row_btn: int = 2,
                    column_btn: int = 0, column_span_btn: int = 3, sticky_btn: str = 'ne', x_btn: int = 0,
                    y_btn: int = 0, ix_btn: int = 13, iy_btn: int = 0):
    #  Function for creating button on main frame
    button_name = ttk.Button(text=text_btn, width=width_btn,
                             state=state_btn, command=command_btn)
    button_name.grid(row=row_btn, column=column_btn, columnspan=column_span_btn, sticky=sticky_btn, padx=x_btn,
                     pady=y_btn, ipadx=ix_btn, ipady=iy_btn)


#  The function belongs to the button "Add item", add information from entries (name, url, amount) at the end of the
#  file
def add_item():
    if name_entry.get() == '' or url_entry.get == '' or amount_entry.get() == '':
        messagebox.showerror('Error!', 'Fill all fields!')  # Return messagebox with error, if any entries is empty
        return None
    with open('urls.txt', 'a', encoding='utf-8') as f:
        get_data = '\n'f'{name_entry.get() + ", " + url_entry.get() + ", " + amount_entry.get()}'
        f.write(get_data)
    text_process.insert(INSERT, f'{name_entry.get()}, {url_entry.get()}, {amount_entry.get()}''\n')
    # Add entries information
    # at the end of the ScrolledText


#  The function belongs to the button "Calculate", calculate all prices added items with threading
def multi_calculate():
    global calculation_file_thread
    progress_bar['value'] = 0
    # Start function turn progress bar in "empty" position
    calculation_file_thread = Thread(target=calculate_file)
    calculation_file_thread.daemon = True  # Special thread for correctly ending threads
    calculation_file_thread.start()


# The function belongs to the button "✕", stopping threading of calculation and all process in program
def stop():
    global stop_process, calculation_file_thread
    stop_process = True
    calculation_file_thread.join()
    # Turn all elements on frame in "normal" condition after completed calculation
    generate_button(text_btn='Add item', width_btn=11, sticky_btn='nw', x_btn=0, y_btn=0, ix_btn=0,
                    iy_btn=0, command_btn=add_item)
    generate_button(text_btn=' Load', width_btn=3, x_btn=53, ix_btn=10, command_btn=load)
    generate_button(text_btn='Calculate', width_btn=11, command_btn=multi_calculate, x_btn=77, ix_btn=12,
                    sticky_btn='nw')
    generate_button(text_btn='Save', command_btn=save)
    name_entry.config(state='normal')
    url_entry.config(state='normal')
    amount_entry.config(state='normal')


#  This function for start calculation in threads mode
def stop_calculation_thread():
    stopping_thread = Thread(target=stop)
    stopping_thread.start()


#  Function for counting lines
def count_lines():
    count_line = 0  # the counter is used later for the correct gradation Progress Bar
    with open('urls.txt', 'r', encoding='utf-8') as r:
        for _ in r:
            count_line += 1
        return count_line


#  Function open "urls" file and take all lines transmit in "check price" function for parsing
def calculate_file():
    global name_item, result, stop_process
    text_process.delete("1.0", "end")
    with open('urls.txt', 'r', encoding='utf-8') as r:
        for line in r:
            if stop_process:
                break
            content = line.strip().replace('\n', '').split(',')
            if len(content) != 3:  # For avoid bug with unnecessary empty lines
                continue
            name_item = content[0]
            url_item = content[1]
            amount_item = int(content[2])
            checker = True
            while checker and not stop_process:  # Exception for avoid steam timeouts with delay
                time.sleep(2.5)
                try:
                    check_price(url_item, amount_item)
                    checker = False
                except Exception:  # If Steam triggered for requestes
                    print("Steam triggered!")
    if not stop_process:
        today = str(date.today())
        text_process.insert(INSERT, '\n' + '-' * 35)
        data = str(int(sum(result))) + '$  '
        with open('invest.txt', 'r', encoding='utf-8') as f:  # Open file for view last line for calculation diff
            first_line = f.readline()
            for last_line in f:
                pass
        last_line_lst = last_line.split('$')
        diff_data = int(sum(result)) - int(last_line_lst[0])
        with open('invest.txt', 'a', encoding='utf-8') as f:
            f.write('\n' + data) + f.write(today)
            text_for_process = '\n'f'{today.ljust(18, " ")}{(str(int(diff_data)) + "$").ljust(12, " ")}{data}'
            if diff_data < 0:
                text_process.config(fg='#FE2E2E')
                text_process.insert(INSERT, text_for_process)
            else:
                text_process.config(fg='#01DF01')
                text_process.insert(INSERT, text_for_process)
        text_process.insert(INSERT, '\n' + '-' * 35)
        result = []
    stop_process = False  # Flags to control calculation threads


generate_elements(data_menu, text_='Item')
name_entry = generate_entry(row_=1)
generate_elements(data_menu, text_='Url', column_=1)
url_entry = generate_entry(width_=32, row_=1, column_=1)
generate_elements(data_menu, text_='Amount', column_=2)
amount_entry = generate_entry(row_=1, column_=2)
text_process = scrolledtext.ScrolledText(data_menu, width=40, height=12)
text_process.grid(row=2, column=0, columnspan=3)
progress_bar = Progressbar(data_menu, length=235, style='Horizontal.TProgressbar')
progress_bar['value'] = 0
progress_bar.grid(row=3, column=0, columnspan=3, padx=3, pady=0, ipadx=12, ipady=0)


def check_price(url: str, count: int):
    global str_len, current_case
    response = requests.get(url).text  # Parsing data in text
    soup = BeautifulSoup(response, 'lxml')
    main_block = soup.find('span', class_="normal_price")
    price_block = main_block.find_all('span')[1].text
    striped_price = float(price_block.strip('$').strip('USD'))  # Strip "$" sign and strip 'USD' for clear float
    current_case = int(round(striped_price * count))
    result.append(current_case)  # Add sum in result list
    str_len = 33 - int(len(name_item))
    text_process.config(fg='#ffffff')
    text_process.insert(INSERT, '\n'f'{name_item + " " + (" " + str(current_case)).rjust(str_len, ".") + "$"}')
    count_of_lines = count_lines()  # Call count lines function
    progress_bar['value'] += 100 / count_of_lines
    # Turn all elements on frame in "disabled" condition for to avoid unnecessary clicks
    generate_button(text_btn='✕', width_btn=2, x_btn=105, y_btn=0, command_btn=stop_calculation_thread)
    generate_button(text_btn='Add item', width_btn=11, state_btn='disabled', sticky_btn='nw', x_btn=0, y_btn=0,
                    ix_btn=0, iy_btn=0, command_btn=add_item)
    generate_button(text_btn='Calculate', width_btn=11, state_btn='disabled', command_btn=multi_calculate, x_btn=77,
                    ix_btn=12, sticky_btn='nw')
    generate_button(text_btn='Save', command_btn=save, state_btn='disabled')
    generate_button(text_btn=' Load', width_btn=3, state_btn='disabled', x_btn=53, ix_btn=10, command_btn=load)
    name_entry.config(state='disabled')
    url_entry.config(state='disabled')
    amount_entry.config(state='disabled')


#  The function belongs to the button "Load", open working file on ScrolledText
def load():
    with open('urls.txt', 'r', encoding='utf-8') as r:
        text_process.config(fg='#ffffff')
        text_process.delete("1.0", "end")
        for line in r:
            text_process.insert(INSERT, f'{line}')


#  The function belongs to the button "Save", overwrites in the working file, everything that was in ScrolledText
def save():
    open('urls.txt', 'w').close()
    with open('urls.txt', 'a', encoding='utf-8') as f:
        f.write(text_process.get('1.0', 'end'))


create_start_buttons()
data_menu.mainloop()
root.mainloop()
