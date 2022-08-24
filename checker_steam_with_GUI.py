import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
import time
from datetime import date
from threading import Thread
from tkinter.ttk import Progressbar
from tkinter import ttk
from multiprocessing import Process

root = Tk()

th = None
stop_process = False
root.title('SteamInvestChecker')


def generate_frame():
    frame_name = Frame(root)
    frame_name.grid(row=0, column=0, sticky='news')
    return frame_name


data_menu = generate_frame()
data_menu.tkraise()


def generate_elements(data_menu, text_: str, font_name: str = 'Arial', font_size: int = 14, row_: int = 0,
                      column_: int = 0, sticky_: str = 'ns'):
    element_name = Label(data_menu, text=text_, font=(font_name, font_size))
    element_name.grid(row=row_, column=column_, sticky=sticky_)


def generate_entry(data_menu, text_entry: str, width_: int = 6, font_name: str = 'Arial', font_size: int = 14,
                   row_: int = 1,
                   column_: int = 0):
    entry_name = Entry(data_menu, width=width_, text=text_entry, font=(font_name, font_size))
    entry_name.grid(row=row_, column=column_)
    return entry_name


def generate_button(text_btn: str, width_btn: int = 2, height_btn: int = 1, bg_btn: str = '#81F781',
                    font_name: str = 'Arial', font_size: str = 13, state_btn: str = "normal", command_btn=None,
                    row_btn: int = 2,
                    column_btn: int = 0,
                    columnspan_btn: int = 3, sticky_btn: str = 'ne', padx_btn: int = 0, pady_btn: int = 0,
                    ipadx_btn: int = 13, ipady_btn: int = 0):
    button_name = Button(text=text_btn, width=width_btn, height=height_btn, bg=bg_btn, font=(font_name, font_size),
                         state=state_btn, command=command_btn)
    button_name.grid(row=row_btn, column=column_btn, columnspan=columnspan_btn, sticky=sticky_btn, padx=padx_btn,
                     pady=pady_btn, ipadx=ipadx_btn, ipady=ipady_btn)


def count_lines():
    count_line = 0
    with open('urls.txt', 'r', encoding='utf-8') as r:
        for _ in r:
            count_line += 1
        return count_line


generate_elements(data_menu, text_='Item')
name_entry = generate_entry(data_menu, text_entry='name', row_=1)
generate_elements(data_menu, text_='Url', column_=1)
url_entry = generate_entry(data_menu, width_=20, text_entry='Url', row_=1, column_=1)
generate_elements(data_menu, text_='Amount', column_=2)
amount_entry = generate_entry(data_menu, text_entry='Amount', row_=1, column_=2)
text_process = scrolledtext.ScrolledText(data_menu, width=43, height=12)
text_process.grid(row=2, column=0, columnspan=3)
style = ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background='#5882FA')
progress_bar = Progressbar(data_menu, length=235, style='black.Horizontal.TProgressbar')
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
    global th
    progress_bar['value'] = 0
    th = Thread(target=calculate_file)
    th.daemon = True
    th.start()


def stop():
    global stop_process, th
    stop_process = True
    th.join()
    generate_button(text_btn='Add item', width_btn=9, bg_btn='#FE9A2E', sticky_btn='nw', padx_btn=0,
                    pady_btn=0,
                    ipadx_btn=0, ipady_btn=0, command_btn=add_item)
    generate_button(text_btn=' Load', width_btn=3, padx_btn=53, ipadx_btn=10, command_btn=load)
    generate_button(text_btn='Calculate', width_btn=10, command_btn=multi_calculate, padx_btn=91, ipadx_btn=12,
                    sticky_btn='nw')
    generate_button(text_btn='Save', command_btn=save)
    name_entry.config(state='normal')
    url_entry.config(state='normal')
    amount_entry.config(state='normal')


def get_free_proxies():
    url = "https://free-proxy-list.net/"
    soup1 = BeautifulSoup(requests.get(url).text, "html.parser")
    proxies = []
    for row in soup1.find("table", class_='table table-striped table-bordered').find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies


def stop_threading():
    thr = Thread(target=stop)
    thr.start()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47'
}
cookie = {'steamLoginSecure': '12345'}

generate_button(text_btn='Add item', width_btn=9, bg_btn='#FE9A2E', sticky_btn='nw', padx_btn=0, pady_btn=0,
                ipadx_btn=0, ipady_btn=0, command_btn=add_item)
generate_button(text_btn=' Load', width_btn=3, padx_btn=53, ipadx_btn=10, command_btn=load)
calc = generate_button(text_btn='Calculate', width_btn=10, command_btn=multi_calculate, padx_btn=91, ipadx_btn=12,
                       sticky_btn='nw')
generate_button(text_btn='Save', command_btn=save)
generate_button(text_btn='✕', width_btn=1, bg_btn='#FE2E2E', padx_btn=105, pady_btn=0, command_btn=stop_threading)


def check_price(url: str, count: int):
    global check_price, calc_btn, count_lines
    # responce = requests.get(url, headers=headers, proxies=free_proxies).text
    # responce = requests.get(url, headers=headers, proxies={'https': f'http://{proxy}'}, cookies=cookie).text
    responce = requests.get(url, headers=headers, cookies=cookie).text
    soup = BeautifulSoup(responce, 'lxml')
    block = soup.find('span', class_="normal_price")
    checking = block.find_all('span')[1].text
    total_check_price = float(checking.strip('$').strip('USD'))
    current_case = total_check_price * count
    result.append(current_case)
    text_process.insert(INSERT, '\n'f'{name_ + " " + str(current_case) + "$"}')
    count_li = count_lines()
    progress_bar['value'] += 100 / count_li
    generate_button(text_btn='Add item', width_btn=9, bg_btn='#DCDCDC', state_btn='disabled',
                    sticky_btn='nw', padx_btn=0,
                    pady_btn=0,
                    ipadx_btn=0, ipady_btn=0, command_btn=add_item)
    generate_button(text_btn='Calculate', width_btn=10, bg_btn='#DCDCDC', state_btn='disabled',
                    command_btn=multi_calculate, padx_btn=91, ipadx_btn=12,
                    sticky_btn='nw')
    generate_button(text_btn='Save', command_btn=save, bg_btn='#DCDCDC', state_btn='disabled')
    generate_button(text_btn=' Load', width_btn=3, bg_btn='#DCDCDC', state_btn='disabled', padx_btn=53, ipadx_btn=10,
                    command_btn=load)
    name_entry.config(state='disabled')
    url_entry.config(state='disabled')
    amount_entry.config(state='disabled')


def calculate_file():
    global name_, result, stop_process
    progress_bar['value'] = 0
    text_process.delete("1.0", "end")
    with open('urls.txt', 'r', encoding='utf-8') as r:
        for line in r:
            if stop_process:
                break
            content = line.strip().replace('\n', '').split(',')
            if len(content) != 3:
                continue
            name_ = content[0]
            url = content[1]
            amount = int(content[2])
            checker = True
            while checker and not stop_process:
                time.sleep(2.5)
                try:
                    check_price(url, amount)
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
