# AUTH.PY IMPORTS ==========
from rm_questrade_api import *
from tkinter import *
from tkinter import messagebox # even though everything was imported messagebox still needs to be implicidly imported
from tkinter import ttk, filedialog, simpledialog
import sqlite3
import pandas as pd
from pytz import timezone
import sys
from IPython.display import display
from pandastable import Table
from pandasgui import show

database = 'riskmit.db'

label_width = 30
button_width = 15
button_height = 10
button_color1 = 'grey'
button_text_color1 = 'black'

#========================================================================================
#----------- REVIEW WINDOW --------------------------------------------------------------
#========================================================================================
def accounts_window(database):
    print('accounts_window started')
    w1 = Tk()
    w1.state('zoomed')
    #w1.geometry('1500x780')
    w1.title('ACCOUNTS')
    style=ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",#Confirgure treeview colors
        background="#D3D3D3",
        foreground='black',
        rowheight=25,
        fieldbackground='#D3D3D3'
        )
    style.map('Treeview',# CHANGE SELECTED COLOR
        background=[('selected', '#347083')]
        )
    
# FRAME DIMENTIONS --------------
    w1.update()
    window_height = w1.winfo_height()
    window_width = w1.winfo_width()
    label_width = 30
    button_width = 15
    button_height = 1
    button_color1 = 'light grey'
    button_text_color1 = 'black'
    space=5
    tb_x, tb_y, tb_h, tb_w = space, space, window_height*.08, window_width-(space*2)# toolbar
    ma_x, ma_y, ma_h, ma_w = tb_x, tb_y+tb_h, window_height*0.2, window_width*.2# master account
    a_x, a_y, a_h, a_w = ma_x, ma_y+ma_h+space, window_height*0.25, ma_w# accounts
    p_x, p_y, p_h, p_w = ma_x, a_y+a_h+space, window_height*0.44, (window_width*.5)-(space*2)#postions
    o_x, o_y, o_h, o_w = ma_x+p_w+space, p_y, p_h, p_w# orders
    b_x, b_y, b_h, b_w = ma_x+ma_w+space, ma_y, window_height*0.13, (window_width-(4*space)-ma_w)/2#balances
    t_x, t_y, t_h, t_w = b_x, b_y+b_h+space, b_h, b_w#totals
    act_x, act_y, act_h, act_w = b_x, t_y+t_h+space, ma_h+a_h-b_h-t_h-space,b_w #activities
    e_x, e_y, e_h, e_w = b_x+b_w+space, b_y, act_h+b_h+t_h+space+space, b_w#executions

# TOOL BAR FRAME
    frame_tb = LabelFrame(w1, text ='CONTROL PANEL')
    frame_tb.place(x=tb_x, y=tb_y, height=tb_h, width=tb_w)
# USERS-----------------------------------------------------
    button_users = Button(frame_tb, text="USERS", command = lambda: users_window(),height=button_height, width=button_width, bg=button_color1, fg=button_text_color1)
    button_users.grid(column=0,row=0)
# MASTER ACCOUNT FRAME -----------------------------------------------------
    frame_ma = LabelFrame(w1, text="MASTER ACCOUNT")
    frame_ma.place(x=ma_x,y=ma_y, height=ma_h, width=ma_w) # set the height and width
    #button_ma = Button(frame_tb, text="MASTER ACCOUNTS", command = lambda: ma_detail_window(),height=button_height, width=button_width, bg=button_color1, fg=button_text_color1)
    button_ma = Button(frame_tb, text="MASTER ACCOUNTS", command = lambda: ma_detail_window(),height=button_height, width=button_width, bg=button_color1, fg=button_text_color1)
    button_ma.grid(column=1,row=0)
    scroll_ma = Scrollbar(frame_ma) # add scroll bar
    scroll_ma.pack(side=RIGHT, fill=Y)
    tree_ma = ttk.Treeview(frame_ma, yscrollcommand=scroll_ma.set, selectmode="extended")
    tree_ma.pack()
    scroll_ma.config(command=tree_ma.yview)
# ACCOUNTS FRAME ------------------------------------------------------------
    frame_accounts = LabelFrame(w1, text="ACCOUNTS")
    frame_accounts.place(x=a_x, y=a_y, height=a_h, width=a_w) # set the height and width of Jake is a Bad Dog
    button_accounts = Button(frame_tb, text="ACCOUNTS", command = lambda: account_detail_window(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
    button_accounts.grid(column=2,row=0)
    scroll_accounts = Scrollbar(frame_accounts) # add scroll bar
    scroll_accounts.pack(side=RIGHT, fill=Y)
    tree_accounts = ttk.Treeview(frame_accounts, yscrollcommand=scroll_accounts.set, selectmode="extended")
    tree_accounts.pack()
    scroll_accounts.config(command=tree_accounts.yview)
# BALANCE FRAME ------------------------------------------------------------------
    frame_balance = LabelFrame(w1, text="BALANCES")
    frame_balance.place(x=b_x, y=b_y, height=b_h, width=b_w)
    tree_balances = ttk.Treeview(frame_balance, selectmode="extended")
    tree_balances.pack(fill='x')
# TOTAL FRAME ------------------------------------------------------------------
    frame_totals = LabelFrame(w1, text="TOTALS")
    frame_totals.place(x=t_x, y=t_y, height=t_h, width=t_w)
    tree_totals = ttk.Treeview(frame_totals, selectmode="extended")
    tree_totals.pack(fill='x')
# POSITIONS FRAME
    frame_positions = LabelFrame(w1, text="POSITIONS")
    frame_positions.place(x=p_x, y=p_y, height=p_h, width=p_w)
    button_positions = Button(frame_tb, text="POSITIONS", command = lambda: position_detail_window(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
    button_positions.grid(column=3,row=0)
    scroll_postions_y = Scrollbar(frame_positions) # add scroll bar
    scroll_postions_y.pack(side=RIGHT, fill=Y)
    scroll_postions_x = Scrollbar(frame_positions, orient='horizontal')
    scroll_postions_x.pack(side=BOTTOM, fill=X)
    #print('p_h = ',p_h)
    tree_positions = ttk.Treeview(frame_positions, height=500, yscrollcommand=scroll_postions_y.set, selectmode="extended")
    tree_positions.pack(fill='x')
    scroll_postions_y.config(command=tree_positions.yview)
    scroll_postions_x.config(command=tree_positions.xview)
# ORDERS FRAME
    frame_orders = LabelFrame(w1, text="ORDERS")
    frame_orders.place(x=o_x, y=o_y, height=o_h, width=o_w)
    button_orders = Button(frame_tb, text="ORDERS", command = lambda: order_detail_window(), width=button_width, height=button_height,bg=button_color1, fg=button_text_color1)
    button_orders.grid(column=4,row=0)
    scroll_orders_y = Scrollbar(frame_orders) # add scroll bar
    scroll_orders_y.pack(side=RIGHT, fill=Y)
    scroll_orders_x = Scrollbar(frame_orders, orient='horizontal')
    scroll_orders_x.pack(side=BOTTOM, fill=X)
    tree_orders = ttk.Treeview(frame_orders, height= 500, yscrollcommand=scroll_orders_y.set, selectmode="extended")
    tree_orders.pack(fill='both')
    scroll_orders_y.config(command=tree_orders.yview)
    scroll_orders_x.config(command=tree_orders.xview)
# EXECUTIONS FRAME
    frame_executions = LabelFrame(w1, text="EXECUTIONS")
    frame_executions.place(x=e_x, y=e_y, height=e_h, width=e_w)
    button_executions = Button(frame_tb, text="EXECUTIONS", command = lambda: executions_detail_window(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
    button_executions.grid(column=5,row=0)
    scroll_executions_y = Scrollbar(frame_executions) # add scroll bar
    scroll_executions_y.pack(side=RIGHT, fill=Y)
    scroll_executions_x = Scrollbar(frame_executions, orient='horizontal')
    scroll_executions_x.pack(side=BOTTOM, fill=X)
    tree_executions = ttk.Treeview(frame_executions,height=500,yscrollcommand=scroll_executions_y.set, selectmode="extended")
    tree_executions.pack()
    scroll_executions_y.config(command=tree_executions.yview)
    scroll_executions_x.config(command=tree_executions.xview)
# ACCTIVITIES FRAME
    frame_activities = LabelFrame(w1, text="ACTIVITIES")
    frame_activities.place(x=act_x, y=act_y, height=act_h, width=act_w)
    button_activities = Button(frame_tb, text="ACTIVITIES", command = lambda: activities_detail_window(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
    button_activities.grid(column=6,row=0)
    scroll_activities = Scrollbar(frame_activities) # add scroll bar
    scroll_activities.pack(side=RIGHT, fill=Y)
    tree_activities = ttk.Treeview(frame_activities, height=500, yscrollcommand=scroll_activities.set, selectmode="extended")
    tree_activities.pack(fill = 'both')
    scroll_activities.config(command=tree_activities.yview)

# PANDAS GUI BUTTON
    button_pandasgui = Button(frame_tb, text="PANDASGUI", command = lambda: pandasgui_display(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
    button_pandasgui.grid(column=7,row=0)

# CLOSE BUTTON
    close_button = Button(frame_tb, text='CLOSE',width=button_width, height=button_height, bg=button_color1, fg=button_text_color1, command=w1.destroy)
    close_button.grid(column=10,row=0)

    #w1.bind('<Configure>',resize_app)
    #=================================================================================================
    # ============= USERS WINDOW =====================================================================
    # ================================================================================================
    def users_window():

        def clear_name():
            user_name.delete(0,END)
            first_name.delete(0,END)
            last_name.delete(0,END)

        def submit_name():
            conn = sqlite3.connect(database)
            c = conn.cursor()
            c.execute("INSERT INTO users VALUES (:user_name, :first_name, :last_name)",
                    {'user_name' : user_name.get(),'first_name': first_name.get(),'last_name' : last_name.get()})
            conn.commit()
            c.close()
            conn.close()
            clear_name()
            query_names()

        def get_user_selected(*args):
            selected = tree_users.focus() # Gab record number
            values = tree_users.item(selected, 'values') # Grap tuple of row values
            print('User record clicked :',values)
            return values

        def user_record_clicked(*args):
            selected_user = get_user_selected('e')
            print('Selected User :', selected_user)
            clear_name()
            user_name.insert(0,selected_user[0])
            first_name.insert(0,selected_user[1])
            last_name.insert(0,selected_user[2])
            return selected_user

        def update_user():
            print('Running update user')
            user_id = get_user_selected('e')[3]
            print('user_id :',user_id)
            conn = sqlite3.connect(database)
            c = conn.cursor()
            c.execute("""UPDATE users SET
                user_name = :user_name,
                first_name = :first_name,
                last_name = :last_name

                WHERE oid = :oid""",
                {
                'user_name': user_name.get(),
                'first_name': first_name.get(),
                'last_name': last_name.get(),
                'oid': user_id
                })

            conn.commit() # Commit and Close
            c.close()
            conn.close()
            clear_name()
            query_names()

        def query_names():
            conn = sqlite3.connect(database)
            c = conn.cursor()
            c.execute("SELECT *, oid FROM users") # get all fields plus the primary keyu
            records = c.fetchall()
            headers = [i[0] for i in c.description]
            # COLUMN HEADINGS
            tree_users.delete(*tree_users.get_children())
            tree_users['columns'] = headers
            tree_users['show']= 'headings'
            for column in tree_users['columns']:
                tree_users.heading(column, text=column, anchor=W)
                tree_users.column(column, width=100)
            # PRINT ROWS
            for row in records:
                tree_users.insert("", "end", values=row)
            # BINDING
            tree_users.bind('<ButtonRelease-1>', user_record_clicked)
            conn.commit()
            c.close()
            conn.close()

        def delete_name():
            key_to_delete = get_user_selected('e')[3]
            print("about to delete user id :", key_to_delete) 
            conn = sqlite3.connect(database)
            c = conn.cursor()
            c.execute("DELETE from users WHERE oid= "+ key_to_delete)
            conn.commit() # Commit and Close
            c.close()
            conn.close()
            query_names()
        # ------  START OF MAIN USER WINDOW ----------------------
        w_users = Toplevel(w1)
        w_users.geometry('810x600')
        w_users.title('USERS')

        # Frames and tree
        frame_users = LabelFrame(w_users, text = "USERS")
        frame_users.place(x=5, y=5, width=800, height=400)
        frame_buttons = LabelFrame(w_users, text = "CONTROLS")
        frame_buttons.place(x=5, y=405, width=800, height=160)
        tree_users = ttk.Treeview(frame_users,)
        tree_users.pack(fill='x')

        # Input boxes
        user_name_label = Label(frame_buttons, text='User Name')
        user_name_label.grid(row = 0, column = 0)
        user_name = Entry(frame_buttons, width=30)
        user_name.grid(row=0, column=1, padx=20)
        first_name_label = Label(frame_buttons, text='First Name')
        first_name_label.grid(row = 1, column = 0)
        first_name = Entry(frame_buttons, width=30)
        first_name.grid(row=1, column=1, padx=20)
        last_name_label = Label(frame_buttons, text='Last Name')
        last_name_label.grid(row = 2, column = 0)
        last_name = Entry(frame_buttons, width=30)
        last_name.grid(row=2, column=1, padx=20)
        submit_button = Button(frame_buttons, text = "Add User", command=submit_name)
        submit_button.grid(row = 3, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        clear_button = Button(frame_buttons, text = "Clear", command=clear_name)
        clear_button.grid(row = 4, column=0, columnspan=2, pady=0, padx=10, ipadx=110)
        query_button = Button(frame_buttons, text = "Query Database", command=query_names)
        query_button.grid(row =3, column=3, columnspan=1, pady=0, padx=10, ipadx=70)
        delete_button = Button(frame_buttons, text = "Delete User", command=delete_name)
        delete_button.grid(row =4, column=3, columnspan=1, pady=0, padx=10,ipadx=80)
        update_button = Button(frame_buttons, text = "Update User", command=update_user)
        update_button.grid(row =3, column=4, columnspan=1, pady=0, padx=10, ipadx=70)

        frame_users.update()

        query_names()
    #============================================================================
    # ============= MASTER ACCOUNT FRAME ========================================
    # ====================================================================
    def draw_ma():
        tree_ma.delete(*tree_positions.get_children()) # clear any previous tree
        w1.update()
        print('running draw_ma')
        # OPEN DATABASE
        conn = sqlite3.connect('riskmit.db') 
        c = conn.cursor()
        c.execute("SELECT account_number, account_name FROM master_accounts")
        records = c.fetchall() # geta all rows in table
        headers = [i[0] for i in c.description] # gets all column names
        # COLUMN HEADINGS
        tree_ma['columns'] = headers
        tree_ma['show']= 'headings'
        for column in tree_ma['columns']:
            tree_ma.heading(column, text=column)
            if column =='account_name':
                tree_ma.column(column, width=100)
            elif column =='account_number':
                tree_ma.column(column, width=70)
            else:
                tree_ma.column(column, width=20)
        # PRINT ROWS
        for row in records:
            tree_ma.insert("", "end", values=row)
        # BINDING
        tree_ma.bind('<ButtonRelease-1>', master_account_change)
        conn.commit()
        c.close()
        conn.close()

    # MASTER ACCOUNT DETAIL PAGE --------------------
    def ma_detail_window():
            print('running ma_detail_window')
            w7 = Toplevel(w1)
            w7.geometry('1450x600')
            w7.title('MASTER ACCOUNTS')
            frame_ma_all = LabelFrame(w7, text="MASTER ACCOUNTS")
            #frame_ma_all = Frame(w7)
            frame_ma_all.pack(fill='both', expand=True)

        # LOAD DATABASE TABLE INTO DF
            conn = sqlite3.connect(database) 
            c = conn.cursor()
            df_ma = pd.read_squl_querry("SELECT * FROM cralwed",c)
            print("Here is the converted ma df : ",df_ma)
            conn.commit()
            c.close()
            conn.close()

        # PANDASTABLE
            pt = Table(frame_ma_all, dataframe=df_ma)
            pt.show()
            #w7.bind('<Configure>',frame_orders.update())
            w7.mainloop()

    # GRAB THE MASTER ACCOUNT CHOOSEN AND UPDATE ACCOUNT LIST
    def master_account_change(e):
            global q
            global ma_name
            # CLEAR OTHER TREES
            tree_positions.delete(*tree_positions.get_children()) # clear any previous tree
            tree_accounts.delete(*tree_accounts.get_children()) # clear any previous tree  
            tree_orders.delete(*tree_orders.get_children()) # clear any previous tree
            tree_executions.delete(*tree_executions.get_children()) # clear any previous tree
            tree_activities.delete(*tree_activities.get_children()) # clear any previous tree
            w1.update() #refresh window
            # GET THE MA NAME CHOOSEN
            selected = tree_ma.focus() # Gab record number
            values = tree_ma.item(selected, 'values') # Grap tuple of row values
            ma_name = values[1] # Assign selected Account Number
            q = allinone_token_set(ma_name)# GET THE TOKEN SET FOR CHOOSEN MA
            print('Master Account set, q = ',q)
            draw_accounts(q) 

# ===============================================================================
# ============== ACCOUNT LIST FRAME =============================================
# ==============================================================================
    def draw_accounts(q): # List accounts, get master account id
        global account_number
        accounts_data = accounts(q)
        account_df = accounts_data[0]
        account_number = accounts_data[1]
        frame_ma.configure(text = 'MASTER ACCOUNT :'+str(account_number))
        df_summary = account_df
        df_summary = df_summary.drop(['status','isPrimary','isBilling'], axis=1)
        # ------------------------ COLUMN HEADINGS ------------------------------------
        tree_accounts['columns'] = list(df_summary.columns)
        tree_accounts['show']= 'headings'
        for column in tree_accounts['columns']:
            tree_accounts.heading(column, text=column)
            tree_accounts.column(column, width=70)
        # --------------------------- PRINT ROWS -----------------------------------
        df_rows = df_summary.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows:
            tree_accounts.insert("", "end", values=row)
        # --------------- BINDING ---------------------------------------------------
        tree_accounts.bind('<ButtonRelease-1>', account_clicked)
        # ----------  SET ACCOUNT ID IN DB MASTER ACCOUNT TABLE IF NOT SET YET -----------
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("UPDATE master_accounts SET account_number=? WHERE account_name=?",(account_number, ma_name))
        conn.commit() # Commit changes
        c.close()
        conn.close() # close data base
        tree_ma.delete(*tree_ma.get_children()) # clear any previous tree
        w1.update()
        draw_ma()

    # ACCOUNT DETAIL WINDOW -------------------------------
    def account_detail_window(): 
            w2 = Toplevel(w1)
            w2.geometry('1400x600')
            w2.title('ACCOUNTS')
            frame_accounts_all = LabelFrame(w2, text="ACCOUNTS")
            frame_accounts_all.place(x=5, y=5, height=500, width=1390) # set the height and width of Jake is a Bad Dog
            close_button = Button(w2, text='CLOSE', command=w2.destroy) 
            close_button.pack()
        # PANDAS TABLE TEST
            df_accounts_all = accounts(q)[0]
            print('running accounts detail window :',df_accounts_all)
            pt = Table(frame_accounts_all, dataframe=df_accounts_all)
            #pt = Table(frame_positions_all, showtoolbar=True)
            pt.show()

    # ACCOUNT HAS BEEN CLICKED - POPULATE THE FRAMES ===================
    def account_clicked(e):
            global account_number
            #------ GRAB ACCOUNT THAT WAS CLICKED -----------
            selected = tree_accounts.focus() # Gab record number
            values = tree_accounts.item(selected, 'values') # Grap tuple of row values
            account_number = values[1] # Assign selected Account Number
            # --------- CLEAR TREES -------------------------
            tree_positions.delete(*tree_positions.get_children()) # clear any previous tree
            tree_orders.delete(*tree_orders.get_children())
            tree_balances.delete(*tree_balances.get_children())
            tree_totals.delete(*tree_totals.get_children())
            tree_executions.delete(*tree_executions.get_children())
            tree_activities.delete(*tree_activities.get_children())
            w1.update() #refesh window
            # ----------- REPOPULATE THE OTHER TREES
            draw_positions(e) 
            draw_orders(e)
            draw_balances(e)
            draw_executions(e)
            draw_activities(e)

# =================================================================================
# ============== BALANCES FRAME ===================================================
# ==================================================================================
    def draw_balances(e):
        global account_number
        frame_balance.update()
        frame_width = frame_balance.winfo_width()
        df_balance_set = balances(q,account_number)
        df_balances = df_balance_set[0] # balances df
        df_totals = df_balance_set[1] # totals
        print('loaded df_totals in draw_balances :',df_totals)
        # BALANCE HEADINGS
        #frame_balance.update()
        tree_balances['columns'] = list(df_balances.columns)
        tree_balances['show']= 'headings'
        for column in tree_balances['columns']:
            tree_balances.heading(column, text=column,anchor=W)
            tree_balances.column(column, width=100)
        #frame_balance.update()
        # BALANCE ROWS
        df_rows = df_balances.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows:
            tree_balances.insert("", "end", values=row)

        # TOTAL HEADINGS
        frame_totals.update()
        tree_totals['columns'] = list(df_totals.columns)
        tree_totals['show']= 'headings'
        for column in tree_balances['columns']:
            tree_totals.heading(column, text=column,anchor=W)
            tree_totals.column(column, width=100)
        frame_balance.update()
        # TOTAL ROWS
        df_rows = df_totals.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows:
            tree_totals.insert("", "end", values=row)
    
# =================================================================================
# ============== POSITION FRAME ===================================================
# ==================================================================================
    def draw_positions(e):
        global account_number
        frame_positions.update()
        frame_width = frame_positions.winfo_width()
        df_positions = positions(q,account_number)
        df_positions_all = df_positions
        df_positions_all = df_positions_all.drop(['symbolId','closedQuantity','dayPnl','closedPnl','isRealTime','isUnderReorg'], axis=1)
        # COLUMN HEADINGS
        tree_positions['columns'] = list(df_positions_all.columns)
        tree_positions['show']= 'headings'
        for column in tree_positions['columns']:
            tree_positions.heading(column, text=column,anchor=W)
            tree_positions.column(column, width=int(frame_width/7))#, width=60
        # PRINT ROWS
        df_rows = df_positions_all.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows:
            tree_positions.insert("", "end", values=row)

    # --------- POSITION DETAILS WINDOW ---------
    def position_detail_window():
            w3 = Toplevel(w1)
            w3.geometry('1400x600')
            w3.title('POSITIONS')
            frame_positions_all = LabelFrame(w3, text="CURRENT POSITIONS")
            frame_positions_all.place(x=5, y=5, height=500, width=1390) # set the height and width of Jake is a Bad Dog
            close_button = Button(w3, text='CLOSE', command=w3.destroy) 
            close_button.pack()
            # PANDAS TABLE TEST
            df_positions_all = positions(q,account_number)
            print('running position detail window :',df_positions_all)
            pt = Table(frame_positions_all, dataframe=df_positions_all)
            #pt = Table(frame_positions_all, showtoolbar=True)
            pt.show()

            w3.mainloop()

# =================================================================================
# ============== ORDERS FRAME ===================================================
# ==================================================================================
    def create_orders_df(q,account_number):
        df_orders = orders(q,account_number)
        df_orders_filter1 = df_orders
        df_orders_filter1 = df_orders.drop(['id','symbolId','isAnonymous','icebergQuantity','minQuantity','source','primaryRoute','secondaryRoute','orderRoute','venueHoldingOrder','exchangeOrderId','isSignificantShareHolder','isInsider','isLimitOffsetInDollar','legs', 'strategyType','isCrossZero'], axis=1)
        df_orders_filter2 = df_orders_filter1
        df_orders_filter2 = df_orders_filter2.drop(['canceledQuantity','isAllOrNone', 'avgExecPrice', 'notes', 'userId', 'placementCommission'], axis=1)
        df_orders_filter3 = df_orders_filter2
        df_orders_filter3 = df_orders_filter2.drop(['openQuantity','filledQuantity','lastExecPrice','rejectionReason','comissionCharged','chainId', 'creationTime', 'updateTime', 'orderGroupId', 'timeInForce'], axis=1)
        df_orders_filter3 = df_orders_filter3[df_orders_filter3['state'].str.contains('Activated')]
        return(df_orders, df_orders_filter1, df_orders_filter2, df_orders_filter3)

    def draw_orders(e):
        global account_number
        frame_orders.update()
        frame_width = frame_orders.winfo_width()
        print('frame width = ',frame_width)
        df_orders = create_orders_df(q,account_number)[3]
        # COLUMN HEADINGS
        tree_orders['columns'] = list(df_orders.columns)
        tree_orders['show']= 'headings'
        for column in tree_orders['columns']:
            tree_orders.heading(column, text=column,anchor=W)
            tree_orders.column(column, width=int(frame_width/10))
        # PRINT ROWS
        df_rows = df_orders.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows:
            tree_orders.insert("", "end", values=row)
    
    # ------ ORDERS DETAIL WINDOW -----------------
    def order_detail_window():
            global account_number
            w4 = Toplevel(w1)
            w4.geometry('1450x600')
            w4.title('ORDERS')
            frame_orders_all = Frame(w4)
            frame_orders_all.pack(fill='both', expand=True)

        # PANDASTABLE
            #df_orders_all = create_orders_df(q,account_number)[0]
            df_orders_all = orders(q,account_number)
            print('Running orders detail df : ',df_orders_all)
            pt = Table(frame_orders_all, dataframe=df_orders_all)
            pt.show()
            #w4.bind('<Configure>',frame_orders.update())
            w4.mainloop()
    
# =================================================================================
# ============== EXECUTIONS FRAME ===================================================
# ==================================================================================
    def create_executions_df(q,account_number):
        df_executions = executions(q,account_number)
        df_executions_filter1 = df_executions
        df_executions_filter1 = df_executions_filter1.drop(['symbolId','id','orderId','orderChainId','exchangeExecId','notes','venue','legId','canadianExecutionFee','parentId'], axis=1)
        return(df_executions, df_executions_filter1)

    def draw_executions(e):
        global account_number
        frame_executions.update()
        frame_width = frame_executions.winfo_width()
        print('frame width = ',frame_width)
        df_executions = create_executions_df(q,account_number)[1]
        # COLUMN HEADINGS
        tree_executions['columns'] = list(df_executions.columns)
        tree_executions['show']= 'headings'
        for column in tree_executions['columns']:
            tree_executions.heading(column, text=column,anchor=W)
            tree_executions.column(column, width=int(frame_width/10))
        # PRINT ROWS
        df_rows = df_executions.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows:
            tree_executions.insert("", "end", values=row)
        tree_executions.bind('<ButtonRelease-1>', executions_detail_window)

    # ------ EXECUTION DETAIL WINDOW -----------------
    
    def executions_detail_window():
            global account_number
            w5 = Toplevel(w1)
            w5.geometry('1450x600')
            w5.title('EXECUTIONS')
            frame_executions_all = LabelFrame(w5, text="EXECUTIONS")
            frame_executions_all = Frame(w5)
            frame_executions_all.pack(fill='both', expand=True)

            # PANDASTABLE
            df_executions_all = create_executions_df(q,account_number)[0]
            print('Running execution detail df : ',df_executions_all)
            pt = Table(w5, dataframe=df_executions_all, showtoolbar=0, showstatusbar=True)
            pt.show()
            w5.mainloop()
    
# =================================================================================
# ============== ACTIVITES FRAME ===================================================
# ==================================================================================
    def create_activities_df(q,account_number):
        df_activities = activities(q,account_number)
        #df_orders_filter1 = df_orders
        #df_orders_filter1 = df_orders.drop(['id','symbolId','isAnonymous','icebergQuantity','minQuantity','source','primaryRoute','secondaryRoute','orderRoute','venueHoldingOrder','exchangeOrderId','isSignificantShareHolder','isInsider','isLimitOffsetInDollar','legs', 'strategyType','isCrossZero'], axis=1)
        #df_orders_filter3 = df_orders_filter3[df_orders_filter3['state'].str.contains('Activated')]
        return(df_activities)

    def draw_activities(e):
        global account_number
        frame_activities.update()
        frame_width = frame_activities.winfo_width()
        print('activities frame width = ',frame_width)
        df_activities = create_activities_df(q,account_number)
        print('df_activites from draw activites fucntion ',df_activities)
        # COLUMN HEADINGS
        tree_activities['columns'] = list(df_activities.columns)
        tree_activities['show']= 'headings'
        for column in tree_activities['columns']:
            tree_activities.heading(column, text=column,anchor=W)
            tree_activities.column(column, width=int(frame_width/14))
        # PRINT ROWS
        df_rows = df_activities.to_numpy().tolist() #turns dataframe into list of lists
        for row in df_rows:
            tree_activities.insert("", "end", values=row)


        tree_activities.bind('<ButtonRelease-1>', lambda: activities_detail_window())

    # ------ ACTIVITIES DETAIL WINDOW -----------------
    
    def activities_detail_window(*args,**kwargs):
            global account_number
            w6 = Toplevel(w1)
            w6.geometry('1450x600')
            w6.title('ACTIVITES')
            frame_activities_all = LabelFrame(w6, text="EXECUTIONS")
            frame_activities_all = Frame(w6)
            frame_activities_all.pack(fill='both', expand=True)

            # PANDASTABLE
            df_activities_all = create_activities_df(q,account_number)
            print('Running activities detail df : ',df_activities_all)
            pt = Table(frame_activities_all, dataframe=df_activities_all)
            pt.show()
            w6.mainloop()
    draw_ma()

    # =================================================================================
    # ============== PANDAS GUI ===================================================
    # ==================================================================================
    def pandasgui_display():
        conn = sqlite3.connect('riskmit.db') 
        c = conn.cursor()
        df_ma = pd.read_sql_query("SELECT * FROM master_accounts", conn)
        df_users = pd.read_sql_query("SELECT * FROM users", conn)
        print('here is the df read from database :',df_ma)
        c.close()
        conn.close()

        accounts_data = accounts(q)
        df_accounts = accounts_data[0]

        df_balance_set = balances(q,account_number)
        df_balances = df_balance_set[0] # balances df
        df_totals = df_balance_set[1] # totals
        
        df_positions = positions(q,account_number)
        df_orders = orders(q,account_number)
        df_executions = executions(q,account_number)
        df_activities = activities(q,account_number)
        
        show(df_ma, df_users, df_accounts,df_balances, df_totals,df_positions, df_orders, df_executions,df_activities)



   
    w1.mainloop()

# ================== END GUI ======================

