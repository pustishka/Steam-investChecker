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

root = Tk()


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


def generate_entry(data_menu, text_: str, width_: int = 6, font_name: str = 'Arial', font_size: int = 14, row_: int = 1,
                   column_: int = 0):
    entry_name = Entry(data_menu, width=width_, text=text_, font=(font_name, font_size))
    entry_name.grid(row=row_, column=column_)
    return entry_name


def count_lines():
    count_line = 0
    with open('urls.txt', 'r', encoding='utf-8') as r:
        for line in r:
            count_line += 1
        return count_line


generate_elements(data_menu, text_='Item')
name_entry = generate_entry(data_menu, text_='name', row_=1)
generate_elements(data_menu, text_='Url', column_=1)
url_entry = generate_entry(data_menu, width_=16, text_='Url', row_=1, column_=1)
generate_elements(data_menu, text_='Amount', column_=2)
amount_entry = generate_entry(data_menu, text_='Amount', row_=1, column_=2)
text_process = scrolledtext.ScrolledText(data_menu, width=38, height=12)
text_process.grid(row=2, column=0, columnspan=3)
style = ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background='#5882FA')
progress_bar = Progressbar(data_menu, length=200, style='black.Horizontal.TProgressbar')
progress_bar['value'] = 0
progress_bar.grid(row=3, column=0, columnspan=3)


def load():
    with open('urls.txt', 'r', encoding='utf-8') as r:
        text_process.delete("1.0", "end")
        for line in r:
            text_process.insert(INSERT, f'{line}''\n')


def add_item():
    if name_entry.get() == '' or url_entry.get == '' or amount_entry.get() == '':
        messagebox.showerror('Error!', 'Fill all fields!')
        return None
    with open('urls.txt', 'a', encoding='utf-8') as f:
        get_data = '\n'f'{name_entry.get() + ", " + url_entry.get() + ", " + amount_entry.get()}'
        f.write(get_data)
    text_process.insert(INSERT, '\n'f'{name_entry.get()}, {url_entry.get()}, {amount_entry.get()}')


result = []


def multi_calculate():
    progress_bar['value'] = 0
    th = Thread(target=calculate_file)
    th.start()


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


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47'
}
cookie = {'steamLoginSecure': '12345'}


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
    Button(text='Calculate', width=12, bg='#58FA58', height=1, command=multi_calculate,
           font=('Arial', 13), state='disabled').grid(row=2, column=0, columnspan=3)
    name_entry.config(state='disabled')
    url_entry.config(state='disabled')
    amount_entry.config(state='disabled')


Button(text='Add item', width=11, bg='#FE9A2E', height=1, command=add_item, font=('Arial', 13)).grid(row=2, column=0,
                                                                                                     columnspan=3,
                                                                                                     sticky='nw')
Button(text='Load file', width=11, bg='#58FA58', height=1, command=load,
       font=('Arial', 13)).grid(row=2, column=0, columnspan=3, sticky='ne')
Button(text='Calculate', width=12, bg='#58FA58', height=1, command=multi_calculate,
       font=('Arial', 13)).grid(row=2, column=0, columnspan=3)


def calculate_file():
    global name_, result
    text_process.delete("1.0", "end")
    with open('urls.txt', 'r', encoding='utf-8') as r:
        for line in r:
            content = line.replace('\n', '').split(',')
            name_ = content[0]
            url = content[1]
            amount = int(content[2])
            checker = True
            while checker:
                time.sleep(2.5)
                try:
                    check_price(url, amount)
                    checker = False
                except Exception:
                    print("Steam triggered!")
    today = str(date.today())
    text_process.insert(INSERT, '\n' + '*' * 20)
    data = str(int(sum(result))) + '$  '
    with open('invest.txt', 'a', encoding='utf-8') as f:
        f.write('\n' + data) + f.write(today)
    text_process.insert(INSERT, '\n'f'{data}  {today}')
    Button(text='Calculate', width=12, bg='#58FA58', height=1, command=multi_calculate,
           font=('Arial', 13), state='normal').grid(row=2, column=0, columnspan=3)
    name_entry.config(state='normal')
    url_entry.config(state='normal')
    amount_entry.config(state='normal')
    result = []


data_menu.mainloop()
root.mainloop()
