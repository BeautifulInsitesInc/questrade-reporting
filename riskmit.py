#################################################
#  VERY FIRST ATTEMPT WITH QUESTRADE API        #
#  OFFICIAL VERSION 1.0                         #
#################################################


#import questrade_api as qt
from rm_questrade_api import *
from rm_riskmit_live_review import *
#from rm_database_update import*
#pipfrom rm_manage_database import *
from datetime import datetime, timedelta
import configparser
import urllib
from tkinter import *
from tkinter import messagebox # even though everything was imported messagebox still needs to be implicidly imported
from tkinter import ttk, filedialog, simpledialog
import sqlite3
import pandas as pd
from pytz import timezone
import os, sys
from IPython.display import display
from contextlib import contextmanager # for database manager
#import pyodbc  # for database manager
import subprocess # for running windows applications and launching other .py files


button_width = 19
button_padding = 2
button_color1 = 'black'
button_color2 = 'blue'
button_color3 = 'grey'
button_text_color1 = 'white'
label_width = 30

database ='riskmit.db'

#print('Drivers :',pyodbc.drivers())

# =============================================================   
# =================== MAIN WINDOW =============================
# =============================================================
root = Tk()
#root.protocol("WM_DELETE_WINDOW", close_window)
root.title("InvestInU Reporting")
#root.geometry("500x600")
root.iconbitmap('assets/favicon.ico')
#root.columnconfigure(0, weight=1)
#root.columnconfigure(1, weight=3)

# ------ TEST PRINT VARIABLES ---------------------
def test_print():
    token_path = token_path_set(master_account_combo.get())
    print('token_path_set() was run: ',token_path)

test_button = Button(root, text='TEST VARIABLES', command=lambda: test_print(), width=button_width, bg='white', fg='black')
test_button.grid(row=10, column=0, sticky="W", pady=(button_padding,10))

#============== SERVER TIME ========================
def server_time():
    st=q.time
    server_time = st.get('time')
    #print('Server Time : ', server_time)
    server_time_label.config(text = server_time)
    return(server_time)

def time_name():
    timename = server_time().replace(':','-')
    print('server time afer replace :',timename)
    time_name_label.config(text = timename)
    return(timename)

def start_date(days_back):
    date_part = server_time()[:10]
    rest_of_it = server_time()[10:]
    date_format = "%Y-%m-%d"
    date_object = datetime.strptime(date_part, date_format)
    tdelta = timedelta(days=days_back)
    last_month_date_obj = date_object - tdelta
    last_month = last_month_date_obj.strftime(date_format)
    start = last_month + rest_of_it
    print('start date : ',start)
    start_date_label.config(text = start)
    return(start)

server_time_button = Button(root, text="SERVER TIME", command = server_time, width=button_width, bg=button_color2, fg=button_text_color1)
server_time_button.grid(row=22, column=0, sticky="W")
server_time_label = Label(root, text=' ', relief = "flat")
server_time_label.grid(row=22, column=1, sticky="W",pady=(button_padding,0))

time_name_button = Button(root, text="TIME NAME", command = time_name, width=button_width, bg=button_color2, fg=button_text_color1)
time_name_button.grid(row=23, column=0, sticky="W")
time_name_label = Label(root, text=' ', relief = "flat")
time_name_label.grid(row=23, column=1, sticky="W",pady=(button_padding,0))

start_date_button = Button(root, text="START DATE", command = lambda: start_date(30), width=button_width, bg=button_color2, fg=button_text_color1)
start_date_button.grid(row=24, column=0, sticky="W")
start_date_label = Label(root, text=' ', relief = "flat")
start_date_label.grid(row=24, column=1, sticky="W",pady=(10,0))

# ================================================================================
# ============================== SELECT MASTER ACCOUNT ===========================
def master_account_set(account, *args):
    global q
    print("Starting master_account_set. account : ",account)
    q = allinone_token_set(account)
    master_account_label.config(text=account)
    print('Master account set, q = ',q)
    return q

options = ["corporate1", "corporate2", "personal"]

master_account_label = Label(root, text=options[0], relief = "flat", width=label_width, anchor=W)
master_account_label.grid(row=0, column=1, sticky="W")
master_account_combo = ttk.Combobox(root, value=options, width=20)
master_account_combo.current(0)
master_account_combo.grid(row=0, column=0, sticky="W")
master_account_combo.bind('<<ComboboxSelected>>', lambda x: master_account_set(master_account_combo.get()))

#master_account_set(master_account_combo.get())

#=================================================================================
# ================================ ACCOUNTS ======================================
def accounts():
    dict_accounts = q.accounts
    ma_name = master_account_combo.get()
    user_id = q.accounts['userId']
    df = pd.DataFrame.from_dict(q.accounts['accounts']) #de-nest the accounts dict and make df
    print('running accounts : ',df)
    print('user_id = ',user_id)
    
    # Set database accountID to ma name in master_accounts table
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("UPDATE master_accounts SET account_id=? WHERE account_name=?",(user_id, ma_name))
    conn.commit() # Commit changes
    c.close()
    conn.close() # close data base
    return (df, user_id)


accounts_button = Button(root, text="ACCOUNTS", command = accounts, width=button_width, bg=button_color2, fg=button_text_color1)
accounts_button.grid(row=29, column=0, sticky="W")
accounts_label = Label(root, text=' ', relief = "flat")
accounts_label.grid(row=29, column=1, sticky="W",pady=(button_padding,0))



# ------ ADD USERS TO MASTER ACCOUNT LIST -------
def add_ma_users():
    global options
    conn = sqlite3.connect('riskmit.db')
    c = conn.cursor()
    for name in options:
        try:
            c.execute('''INSERT INTO master_accounts (account_id, account_name) VALUES (? ,?)''',(666, name))
            print('Master Account Added')
        except:
            print('WARRNING: MASTER ACCOUNT ALREADY EXISTS')
    
    conn.commit()
    #querry database
    c.execute("SELECT * FROM users")
    records = c.fetchall()
    print(records)

     # Commit changes
    conn.close()
# =============== END DATABASE ========================================

def browes_database():
    subprocess.Popen('"C:\\Program Files (x86)\\DB Software Laboratory\\Database Browser\\DatabaseBrowser.exe"')

account_window_button = Button(root, text="ACCOUNT WINDOW", command = lambda: accounts_window(database),width=button_width, bg='green', fg=button_text_color1)
account_window_button.grid(row=50, column=0, sticky="W", pady=(button_padding,0))
database_update_button = Button(root, text="DATABASE UPDATE", command = lambda: database_update(database),width=button_width, bg='green', fg=button_text_color1)
database_update_button.grid(row=55, column=0, sticky="W", pady=(button_padding,0))
database_manage_button = Button(root, text="MANAGE DATABASE", command = lambda: subprocess.Popen("python rm_manage_database.py", shell=True),width=button_width, bg='green', fg=button_text_color1)
database_manage_button.grid(row=55, column=0, sticky="W", pady=(button_padding,0))
viewer_button = Button(root, text="BROWES DATABASE", command = lambda: browes_database(),width=button_width, bg='green', fg=button_text_color1)
viewer_button.grid(row=57, column=0, sticky="W", pady=(button_padding,0))

#create_database()
#add_ma_users()
#manage_database(database)
#accounts_window(database) # OPEN LIVE ACCOUNT WINDOW









print('This is the last line in the code')
root.mainloop()
# ================== END GUI ==================
