import time
from datetime import date
from threading import Thread

from tkinter import messagebox, ttk, scrolledtext, Tk, INSERT
from tkinter.ttk import Progressbar

import requests
from bs4 import BeautifulSoup



def generate_frame():
    frame_name = ttk.Frame(root)  # Create main frame of GUI
    frame_name.grid(row=0, column=0, sticky='news')
    return frame_name


def create_start_buttons():
    generate_button(text_btn='Add item', width_btn=11, sticky_btn='nw', x_btn=0, y_btn=0, ix_btn=0,
                    iy_btn=0, command_btn=add_item)  # Create button "Add item"
    generate_button(text_btn=' Load', width_btn=3, x_btn=53, ix_btn=10, command_btn=load)  # Create button "Load"
    generate_button(text_btn='Calculate', width_btn=11, command_btn=multi_calculate, x_btn=77, ix_btn=12,
                    sticky_btn='nw')  # Create button "Calculate"
    generate_button(text_btn='Save', command_btn=save)  # Create button "Save"
    generate_button(text_btn='✕', width_btn=2, x_btn=105, y_btn=0, command_btn=stop_count_thread)  # Create button "✕"

data_menu = generate_frame()
data_menu.tkraise()


def generate_elements(data_menu, text_: str, font_name: str = 'Arial', font_size: int = 14, row_: int = 0,
                      column_: int = 0, sticky_: str = 'ns'):
    element_name = ttk.Label(data_menu, text=text_)
    element_name.grid(row=row_, column=column_, sticky=sticky_)


def generate_entry(text_for_entry: str, width_: int = 9, row_: int = 1, column_: int = 0):
    #  Function for creating entry elements on main frame
    entry_name = ttk.Entry(data_menu, width=width_, text=text_for_entry)
    entry_name.grid(row=row_, column=column_)
    return entry_name


def generate_button(text_btn: str, width_btn: int = 2, state_btn: str = "normal", command_btn=None, row_btn: int = 2,
                    column_btn: int = 0, column_span_btn: int = 3, sticky_btn: str = 'ne', x_btn: int = 0,
                    y_btn: int = 0, ix_btn: int = 13, iy_btn: int = 0):
    #  Function for creating button on main frame
    button_name = ttk.Button(text=text_btn, width=width_btn,
                         state=state_btn, command=command_btn)
    button_name.grid(row=row_btn, column=column_btn, columnspan=columnspan_btn, sticky=sticky_btn, padx=padx_btn,
                     pady=pady_btn, ipadx=ipadx_btn, ipady=ipady_btn)


def count_lines():
    #  Function for counting lines
    count_line = 0  # the counter is used later for the correct gradation Progress Bar
    with open('urls.txt', 'r', encoding='utf-8') as r:
        for _ in r:
            count_line += 1
        return count_line


generate_elements(data_menu, text_='Item')
name_entry = generate_entry(data_menu, text_entry='name', row_=1)
generate_elements(data_menu, text_='Url', column_=1)
url_entry = generate_entry(data_menu, width_=32, text_entry='Url', row_=1, column_=1)
generate_elements(data_menu, text_='Amount', column_=2)
amount_entry = generate_entry(data_menu, text_entry='Amount', row_=1, column_=2)
text_process = scrolledtext.ScrolledText(data_menu, width=40, height=12)
text_process.grid(row=2, column=0, columnspan=3)
progress_bar = Progressbar(data_menu, length=235, style='Horizontal.TProgressbar')
progress_bar['value'] = 0
progress_bar.grid(row=3, column=0, columnspan=3, padx=3, pady=0, ipadx=12, ipady=0)


def load():
    with open('urls.txt', 'r', encoding='utf-8') as r:
        text_process.delete("1.0", "end")
        for line in r:
            text_process.insert(INSERT, f'{line}')


def save():
    open('urls.txt', 'w').close()
    with open('urls.txt', 'a', encoding='utf-8') as f:
        f.write(text_process.get('1.0', 'end'))


def add_item():
    if name_entry.get() == '' or url_entry.get == '' or amount_entry.get() == '':
        messagebox.showerror('Error!', 'Fill all fields!')
        return None
    with open('urls.txt', 'a', encoding='utf-8') as f:
        get_data = '\n'f'{name_entry.get() + ", " + url_entry.get() + ", " + amount_entry.get()}'
        f.write(get_data)
    text_process.insert(INSERT, f'{name_entry.get()}, {url_entry.get()}, {amount_entry.get()}''\n')


result = []


def multi_calculate():
    global calculation_file_thread
    progress_bar['value'] = 0
    calculation_file_thread = Thread(target=calculate_file)
    calculation_file_thread.daemon = True
    calculation_file_thread.start()


def stop():
    global stop_process, calculation_file_thread
    stop_process = True
    calculation_file_thread.join()
    generate_button(text_btn='Add item', width_btn=11, sticky_btn='nw', x_btn=0, y_btn=0, ix_btn=0,
                    iy_btn=0, command_btn=add_item)
    generate_button(text_btn=' Load', width_btn=3, x_btn=53, ix_btn=10, command_btn=load)
    generate_button(text_btn='Calculate', width_btn=11, command_btn=multi_calculate, x_btn=77, ix_btn=12,
                    sticky_btn='nw')
    generate_button(text_btn='Save', command_btn=save)
    name_entry.config(state='normal')
    url_entry.config(state='normal')
    amount_entry.config(state='normal')


def stop_count_thread():
    stopping_thread = Thread(target=stop)
    stopping_thread.start()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47'
}
cookie = {'steamLoginSecure': '12345'}

generate_button(text_btn='Add item', width_btn=11, bg_btn='#FE9A2E', sticky_btn='nw', padx_btn=0, pady_btn=0,
                ipadx_btn=0, ipady_btn=0, command_btn=add_item)
generate_button(text_btn=' Load', width_btn=3, padx_btn=53, ipadx_btn=10, command_btn=load)
generate_button(text_btn='Calculate', width_btn=11, command_btn=multi_calculate, padx_btn=77, ipadx_btn=12,
                       sticky_btn='nw')
generate_button(text_btn='Save', command_btn=save)
generate_button(text_btn='✕', width_btn=2, bg_btn='#FE2E2E', padx_btn=105, pady_btn=0, command_btn=stop_threading)


def check_price(url: str, count: int):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    main_block = soup.find('span', class_="normal_price")
    price_block = main_block.find_all('span')[1].text
    striped_price = float(price_block.strip('$').strip('USD'))
    current_case = striped_price * count
    result.append(current_case)
    text_process.insert(INSERT, '\n'f'{name_item + " " + str(current_case) + "$"}')
    count_of_lines = count_lines()
    progress_bar['value'] += 100 / count_of_lines
    generate_button(text_btn='Add item', width_btn=11, state_btn='disabled', sticky_btn='nw', x_btn=0, y_btn=0,
                    ix_btn=0, iy_btn=0, command_btn=add_item)
    generate_button(text_btn='Calculate', width_btn=11, state_btn='disabled', command_btn=multi_calculate, x_btn=77,
                    ix_btn=12, sticky_btn='nw')
    generate_button(text_btn='Save', command_btn=save, state_btn='disabled')
    generate_button(text_btn=' Load', width_btn=3, state_btn='disabled', x_btn=53, ix_btn=10, command_btn=load)
    name_entry.config(state='disabled')
    url_entry.config(state='disabled')
    amount_entry.config(state='disabled')


def calculate_file():
    global name_item, result, stop_process
    progress_bar['value'] = 0
    text_process.delete("1.0", "end")
    with open('urls.txt', 'r', encoding='utf-8') as r:
        for line in r:
            if stop_process:
                break
            content = line.strip().replace('\n', '').split(',')
            if len(content) != 3:
                continue
            name_item = content[0]
            url_item = content[1]
            amount_item = int(content[2])
            checker = True
            while checker and not stop_process:
                time.sleep(2.5)
                try:
                    check_price(url_item, amount_item)
                    checker = False
                except Exception:
                    print("Steam triggered!")
    if not stop_process:
        today = str(date.today())
        text_process.insert(INSERT, '\n' + '*' * 20)
        data = str(int(sum(result))) + '$  '
        with open('invest.txt', 'a', encoding='utf-8') as f:
            f.write('\n' + data) + f.write(today)
        text_process.insert(INSERT, '\n'f'{data}  {today}')

        result = []
    stop_process = False


data_menu.mainloop()
root.mainloop()
