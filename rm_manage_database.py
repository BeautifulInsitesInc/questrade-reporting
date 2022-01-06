########################################################
# Intial database setup and managment using tkinter    #
# Official version 2.0                                 #
########################################################

from rm_questrade_api import *
from tkinter import *
from tkinter import ttk, filedialog, simpledialog
import sqlite3
import pandas as pd
import numpy as np # to use np.nan
from datetime import date
from IPython.display import display
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
# --- Imports for backup:
import os 
from datetime import date, datetime
import time
# --- SQLALCHEMY
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, Table, select, delete
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import null
import logging
#from pdb import set_trace; set_trace() # see what is happening hen it runs
import rm_tables
from rm_tables import *
#from rm_remove_duplicates_df import clean_df_db_dups, to_sql_newrows #For cleaning duplicat rows from DF comparied to Table
# CONNECT TO HEROKU POSTGRES
import os
import re
import psycopg2
from pandasgui import show
# loggin
#import logging
#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# ==== OPEN DATABASE CONNECTION ==========
#user:password@host/database
local ="postgresql+psycopg2://postgres:Cracker70!@localhost/postgres"
aws = "postgresql+psycopg2://riskmit:Cracker70@usefulanalytics-instance.cjepocpyhpgj.us-east-2.rds.amazonaws.com/riskmit"

engine = create_engine(aws, echo=False)
#engine = create_engine(local)
#engine = create_engine('sqlite:///D:\\Dropbox\\code\\riskmit_questrade\\riskmit.db', echo=True)

Session = sessionmaker(bind=engine) # create a configured "Session" class
session = Session() # create a Session
metadata = MetaData()
Base = declarative_base()
rm_tables.Base.metadata.create_all(engine) # Creates tables if they don't exist

# ======== BACKUP PATH ===================
#backup_folder ='D:/Dropbox/Test folder/backups
backup_folder = 'D:\Dropbox/- INVESTINU/= RISMIT BACKUP EXPORTS'
import_folder = 'D:\Dropbox/- INVESTINU/= QUESTRADE EXPORTS'
datetime = time.strftime('%Y%m%d-%H%M%S')
filename = datetime+'rismit_backup.xlsx'
full_backup_path = backup_folder + '/' + filename

#========================================================================================|
#============= DATABASE MANAGEMENT WINDOW ===============================================|
#========================================================================================|

# ===== MAIN WINDOW LOOP =====================
root = Tk()
#root.state('zoomed')
root.geometry('1200x700')
root.title('DATABASE MANAGMENT')

# =====  CREATE WINDOW FRAMES  ===============
# FRAME DIMENTIONS 
root.update()
window_height = root.winfo_height()
window_width = root.winfo_width()
label_width = 30
button_width = 15
button_height = 1
button_color1 = 'light grey'
button_text_color1 = 'black'
space=5
tb_x, tb_y, tb_h, tb_w = space, space, window_height*.08, window_width-(space*2)# toolbar
users_x, users_y, users_h, users_w = space, space*2+tb_h, window_height-space*3-tb_h, (window_width-space*4)/4
ma_x, ma_y, ma_h, ma_w = users_x+users_w+space, users_y, users_h, users_w
accounts_x, accounts_y, accounts_h, accounts_w = ma_x+ma_w+space,ma_y,ma_h,ma_w*2
# CREATE TOOL BAR FRAME 
frame_tb = LabelFrame(root, text ='CONTROL PANEL')
frame_tb.place(x=tb_x, y=tb_y, height=tb_h, width=tb_w)
# CREATE USERS FRAME
frame_users = LabelFrame(root, text ='USERS')
frame_users.place(x=users_x, y=users_y, height=int(users_h*.50), width=users_w)
frame_user_buttons = LabelFrame(root, text = 'USER CONTROLS')
frame_user_buttons.place(x=users_x, y=users_y+int(users_h*.50), height=int(users_h*.50), width=users_w)
tree_users = ttk.Treeview(frame_users)
tree_users.pack(fill='x')
# CREATE MASTER ACCOUNT FRAME
frame_ma = LabelFrame(root, text ='MASTER ACCOUNT')
frame_ma.place(x=ma_x, y=ma_y, height=ma_h*.50, width=ma_w)
frame_ma_buttons = LabelFrame(root, text = 'MA CONTROLS')
frame_ma_buttons.place(x=ma_x, y=ma_y+int(ma_h*.50), height=int(ma_h*.50), width=ma_w)
tree_ma = ttk.Treeview(frame_ma)
tree_ma.pack(fill='x')
# CREATE ACCOUNTS FRAME
frame_accounts = LabelFrame(root, text ='ACCOUNTS')
frame_accounts.place(x=accounts_x, y=accounts_y, height=int(accounts_h*.50), width=accounts_w)
frame_account_buttons = LabelFrame(root, text = 'MA CONTROLS')
frame_account_buttons.place(x=accounts_x, y=accounts_y+int(accounts_h*.50), height=int(ma_h*.50), width=accounts_w)
tree_accounts = ttk.Treeview(frame_accounts, height = 500)
tree_accounts.pack(fill='both')

# ============================================================================
# ====== BACKUP FUNCTIONS ===================================================
#=============================================================================
def backup_database():
	# CREATE DF FROM TABLES 
	df_users = pd.read_sql_table('users', engine)
	df_master_accounts = pd.read_sql_table('master_accounts', engine)
	df_accounts = pd.read_sql_table('accounts', engine)
	df_positions = pd.read_sql_table('positions', engine)
	df_orders = pd.read_sql_table('orders', engine)
	df_executions = pd.read_sql_table('executions', engine)
	df_activities = pd.read_sql_table('activities', engine)
	display(df_users)
	display(df_master_accounts)
	display(df_accounts)
	display(orders)
	try:
		os.mkdir(backup_folder)
	except:
		print('Directory already exists :',backup_folder)
	# WRITE DF TO EXCEL
	wb= Workbook()
	wb.save(full_backup_path)
	with pd.ExcelWriter(full_backup_path, mode='a') as writer:
		df_users.to_excel(writer, sheet_name='users', index=False)
		df_master_accounts.to_excel(writer, sheet_name='master_accounts', index=False)
		df_accounts.to_excel(writer, sheet_name='accounts', index=False)
		df_positions.to_excel(writer, sheet_name='positions', index=False)
		df_orders.to_excel(writer, sheet_name='orders', index=False)
		df_executions.to_excel(writer, sheet_name='executions', index=False)
		df_activities.to_excel(writer, sheet_name='activities', index=False)
def drop_tables():
	print("dropping tables")
	check = simpledialog.Dialog(root,title='Just double chekcing!')
	with engine.begin() as conn:
		df_users.to_sql(con=conn,name='users',if_exists='append', index=False)
	rm_tables.Base.metadata.drop_all
	session.commit()
	print("DROPPED!")
def restore_database():	
	excel_file_full_path = filedialog.askopenfilename(initialdir=backup_folder, title="Select Excel Workbook", filetypes=(("xlsx Fiel", ".xlsx"),("All Files","*.*")))
	print('Restore file : ',excel_file_full_path)
	df_users = pd.read_excel(excel_file_full_path,sheet_name = 'users')
	df_users.to_sql("users", engine, if_exists='replace')
	df_master_accounts = pd.read_excel(excel_file_full_path,sheet_name = 'master_accounts')
	df_master_accounts.to_sql("master_accounts", engine, if_exists='replace')
	query_names()
	query_ma()
def list_ma_names():
	#CREATE LIST OF MA NAMES :s
	census = Table('users', metadata, autoload=True, autoload_with=engine)
	ma_names = session.execute(select(Master_accounts.account_name))
	ma_list=[] # List of master account names
	for row in ma_names: # Creats the list of master account names to iriterat through
		ma_list.append(''.join(row))
	return ma_list
def list_accounts_by_ma(ma):
	result = session.query(Accounts).filter(Accounts.master_account_id == ma)
	account_list = []
	for row in result:
			#print("Row item :",row.number)
			account_list.append(''.join(row.number))
	return account_list
def populate_accounts():
	ma_list = list_ma_names()
	print('ma list : ',ma_list)
	# CYCLE THROUGH EACH MA NAME 
	for ma in ma_list: 
		print(' RUNNING CYCLE FOR MA = ',ma)
		q = allinone_token_set(ma)# GET THE TOKEN SET FOR CHOOSEN MA
		print(' q has been set in for ma in ma_list loop ', q)
		accounts_data = accounts(q) # contains 2 objects, the ma acocunt number and the list of accounts
		print()
		#print('accounts_data has been set :',accounts_data)
		print()
		df_accounts = accounts_data[0] # assigns the accounts df
		df_accounts.reset_index(drop=True, inplace=True) # Remove the index from df
		df_accounts['master_account_id']=ma # Add ma account field
		#display(df_accounts)
		df_accounts = df_accounts.drop(['isPrimary','isBilling'], axis=1) # drop uncessary columns
		account_number = accounts_data[1] # Account number of the master account
		print()
		print('MASTER ACCOUNT NUMBER :',account_number)
		x = session.query(Master_accounts).get(ma) #
		x.account_number = account_number # ASSIGNS THE MASTER ACCOUNT TO ALL SUBACCOUNTS
		session.commit()
		print("here is the latest df_accounts: ")
		display(df_accounts)
		print()
		for row in df_accounts.itertuples(index = False, name='temp'):
			stmt = Accounts(type=row[0], number=row[1], status=row[2], clientAccountType=row[3], master_account_id=row[4], user_id="", include=False)
			try:
				session.add(stmt)
				session.commit()
				print("Success	!")
			except Exception:
				session.rollback()
				session.commit()
				print("Entry is not unique")
		query_ma()
		query_accounts()
	print("Done ma Loop")
def update_all():
	ma_list = list_ma_names()
	first = True
	# =====================================================================
	# ================== MASTER ACCOUNT MAIN LOOP  =====================
	# ========================================================================
	for ma in ma_list: 
		q = allinone_token_set(ma)# GET THE TOKEN SET FOR CHOOSEN MA
		print("Current Master Account :",ma)
		account_list = list_accounts_by_ma(ma)
		print("Account list: ",account_list)

		# =====================================================================
		# ==================  ACCOUNTS IN EACH MA LOOP  =====================
		# ================ Make the Dataframes   ============================
		
		for account in account_list:
			#  BUILD EACH TOTAL DATAFRAME :
			# ==============   BALANCES  ===================
			combined_balances = balances(q,account) #contains 2 objects, the first is balances, 2nd is totals
			df_balances = combined_balances[0] # CND and US equity and cash balances
			df_balances['account_id']=account # Add ma account fielddf_totals = combined_balances[1] # total balances in each currency
			df_balances['type']='balances'
			df_totals = combined_balances[1] # Account totals in each currencydf
			df_totals['account_id']=account 
			df_totals['type']='totals'

			# ============ POSITIONS ==============================
			df_positions = positions(q,account)
			if df_positions.empty == False:
				df_positions['account_id']=account # add related username 

			# ============ ORDERS ==============================
			df_orders = orders(q,account)
			if df_orders.empty == False:  # If df is empty for the first one, account Id will be put in postion 1
				df_orders['account_id']=account # add related username
				df_orders = df_orders.drop([
					'isAnonymous',
					'icebergQuantity',
					'minQuantity',
					'source',
					'primaryRoute',
					'secondaryRoute',
					'orderRoute',
					'venueHoldingOrder',
					'exchangeOrderId',
					'isSignificantShareHolder',
					'isInsider',
					'isLimitOffsetInDollar',
					'legs',
					'strategyType',
					'isCrossZero'
					], axis=1)

			# ============ EXECUTIONS =============================		
			df_executions = executions(q,account)
			if df_executions.empty == False:  # If df is empty for the first one, account Id will be put in postion 1
				df_executions['account_id']=account # add related username

			# ============ ACTIVITIES =============================		
			df_activities = activities(q,account)
			if df_activities.empty == False:  # If df is empty for the first one, account Id will be put in postion 1
				df_activities['account_id']=account # add related username

			# ========= COMBINE ALL ACCOUNT DATAFRAMES TOGETHER =====================
			if first == True:
				df_all_balances = df_balances
				df_all_balances = pd.concat([df_totals,df_all_balances],ignore_index=True)
				df_all_positions = df_positions
				df_all_orders = df_orders
				df_all_executions = df_executions
				df_all_activities = df_activities
				first = False
			else:
				df_all_balances = pd.concat([df_balances,df_all_balances],ignore_index=True)
				df_all_balances = pd.concat([df_all_balances,df_totals],ignore_index=True)
				df_all_positions = pd.concat([df_all_positions,df_positions],ignore_index=True)
				df_all_orders = pd.concat([df_all_orders,df_orders],ignore_index=True)
				df_all_executions = pd.concat([df_all_executions,df_executions],ignore_index=True)
				df_all_activities = pd.concat([df_all_activities,df_activities],ignore_index=True)

	# ALL DATAFRAMES ARE CREATED
	#show(df_all_balances, df_all_positions, df_all_orders, df_all_executions, df_all_activities)
	
	# ADD BALANCES TO TABLE - REPLACE
	
	#import_balances(df_all_balances)
	#import_positions(df_all_positions)
	import_orders(df_all_orders)
	import_executions(df_all_executions)
	import_activities(df_all_activities)
	print()
	print("All data has been updated!")
def import_balances(df_balances):
	print('Starting to import balance rows')
	session.query(Balances).delete() # Delete all balances before importing new
	session.commit()
	for row in df_balances.itertuples(index = False, name='Balances'):
		# Create import statment
		stmt = Balances(
			currency=row[0],
			cash=row[1],
			marketValue=row[2],
			totalEquity=row[3],
			buyingPower=row[4],
			maintenanceExcess=row[5],
			account_id=row[6],
			type=row[7]
			)
		print('Adding this row to Balances table :',list(row))
		try:
			session.add(stmt)
			session.commit()
			print("Success!")
		except Exception:
			session.rollback()
			session.commit()
			print("Entry is not unique")
	print('Done importing balance rows')
def import_positions(df_positions):
	print('Starting to import position rows')
	session.query(Positions).delete() # Delete all Positions before importing new
	session.commit()
	for row in df_positions.itertuples(index = False, name='Positions'):
		stmt = Positions(
			symbol=row[0],
			symbolId=row[1],
			openQuantity=row[2],
			closedQuantity=row[3],
			currentMarketValue=row[4],
			currentPrice=row[5],
			averageEntryPrice=row[6],
			dayPnl=row[7],
			closedPnl=row[8],
			openPnl=row[9],
			totalCost=row[10],
			isRealTime=row[11],
			isUnderReorg = row[12],
			account_id=row[13]
			)
		print('Adding this row to Positions table :',list(row))
		try:
			session.add(stmt)
			session.commit()
			print("Success!")
		except Exception:
			session.rollback()
			session.commit()
			print("Entry is not unique")
	print("Done entering positions")
def import_orders(df_orders):
	session.query(Orders).delete() # Delete all Orders before importing new
	session.commit()
	for row in df_orders.itertuples(index = False, name='Orders'):
		stmt = Orders(
			id = row[0],
			symbol = row[1],
			symbolId = row[2],
			totalQuantity = row[3],
			openQuantity = row[4],
			filledQuantity = row[5],
			canceledQuantity = row[6],
			side = row[7],
			orderType = row[8],
			limitPrice = row[9],
			stopPrice = row[10],
			isAllOrNone = row[11],
			avgExecPrice = row[12],
			lastExecPrice = row[13],
			timeInForce = row[14],
			gtdDate = row[15],
			state = row[16],
			rejectionReason = row[17],
			chainId = row[18],
			creationTime = row[19],
			updateTime = row[20],
			notes = row[21],
			commisionCharged = row[22],
			userId = row[23],
			placementCommission = row[24],
			triggerStopPrice = row[25],
			orderGroupID = row[26],
			orderClass = row[27],
			account_id = row[28]
			)
		print('Adding this row to Orders table :',list(row))
		try:
			session.add(stmt)
			session.commit()
			print("Success!")
		except Exception:
			session.rollback()
			session.commit()
			print("Entry is not unique")
	print("Done updating orders")
def import_executions(df_executions):
	print("About to enter Executions")
	for row in df_executions.itertuples(index = False, name='Orders'):
		stmt = Executions(
			symbol = row[0],
			symbolId = row[1],
			quantity = row[2],
			side = row[3],
			price = row[4],
			id = row[5],
			orderId = row[6],
			orderChainId = row[7],
			exchangeExecId = row[8],
			timestamp = row[9],
			notes =row[10],
			venue = row[11],
			totalCost = row[12],
			orderPlacementCommission = row[13],
			commission = row[14],
			executionFee = row[15],
			secFee = row[16],
			legId = row[17],
			canadianExecutionFee =row[18],
			parentId = row[19],
			account_id = row[20]
			)
		print('Adding this row to Executions table :',list(row))
		try:
			session.merge(stmt)
			session.commit()
			print("Success!")
		except Exception:
			session.rollback()
			session.commit()
			print("Entry is not unique")
	print("About to enter Executions")
def import_activities(df_activities):
	df_activities = df_activities.replace(np.nan,"",regex=True)
	for row in df_activities.itertuples(index = False, name='Activities'):
		stmt = Activities(
			tradeDate = row[0],
			transactionDate = row[1],
			settlementDate = row[2],
			action = row[3],
			symbol = row[4],
			symbolId = row[5],
			description = row[6],
			currency = row[7],
			quantity = row[8],
			price = row[9],
			grossAmount = row[10],
			commission = row[11],
			netAmount = row[12],
			type = row[13],
			account_id = row[14]
			)
		print('Adding this row to Activities table :',list(row))
		try:
			session.add(stmt)
			session.commit()
			print("Success!")
		except Exception:
			session.rollback()
			session.commit()
			print("Entry is not unique")
	print("Do entering activities ")
def	load_executions_activities_from_backup():
	excel_file_full_path = filedialog.askopenfilename(initialdir=backup_folder, title="Select Excel Workbook", filetypes=(("xlsx Fiel", ".xlsx"),("All Files","*.*")))
	print('Restore file : ',excel_file_full_path)
	df_executions = pd.read_excel(excel_file_full_path,sheet_name = 'executions')
	df_activities = pd.read_excel(excel_file_full_path,sheet_name = 'activities')
	print()
	print("loaded executions: ")
	display(df_executions)
	print()
	print("Loaded aCtivities : ")
	display(df_activities)
	import_executions(df_executions)
	import_activities(df_activities)
def questrade_import():
		excel_file_full_path = filedialog.askopenfilename(initialdir=import_folder, title="Select Excel Workbook", filetypes=(("xlsx Fiel", ".xlsx"),("All Files","*.*")))
		print('Restore file : ',excel_file_full_path)
		df_qtactivities = pd.read_excel(excel_file_full_path)
		
		# Shape data to match table
		df_qtactivities.drop('Account Type', axis=1, inplace=True) 
		df_qtactivities.rename(columns={'Transaction Date':'transactionDate','Settlement Date':'settlementDate','Action':'action','Symbol':'symbol','Description':'description','Currency':'currency','Quantity':'quantity','Price':'price','Gross Amount':'grossAmount','Commission':'commission','Net Amount':'netAmount','Account #':'account_id','Activity Type':'type'},inplace=True)
		print('Renamed columns :')

		# Change Column order
		df_qtactivities = df_qtactivities.reindex(columns = ['tradeDate','transactionDate','settlementDate','action','symbol','symbolId','description','currency','quantity','price','grossAmount','commission','netAmount','type','account_id'])
		df_qtactivities['tradeDate']=df_qtactivities['transactionDate']
		print("running import activities")
		import_activities(df_qtactivities)

# ----------------------------------------------------------------------------
# ------- TOOL BAR BUTTONS ---------------------------------------------------
# ----------------------------------------------------------------------------
button_backup = Button(frame_tb, text='BACKUP', command = lambda: backup_database(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
button_backup.grid(column=0, row=0)
button_restore = Button(frame_tb, text='RESTORE', command = lambda: restore_database(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
button_restore.grid(column=5, row=0)
button_create = Button(frame_tb, text='CREATE', command = lambda: rm_tables.Base.metadata.create_all(engine), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
button_create.grid(column=10, row=0)
button_delete = Button(frame_tb, text='DROP TABLES', command = lambda: drop_tables(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
button_delete.grid(column=20, row=0)
button_populate_accounts = Button(frame_tb, text='ACCOUNTS', command = lambda: populate_accounts(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
button_populate_accounts.grid(column=25, row=0)
button_update_all = Button(frame_tb, text='UPDATE ALL', command = lambda: update_all(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
button_update_all.grid(column=30, row=0)
button_import_executions = Button(frame_tb, text='IMPORT EXECUTIONS', command = lambda: load_executions_activities_from_backup(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
button_import_executions.grid(column=35, row=0)
button_import_executions = Button(frame_tb, text='QUESTRADE IMPORT', command = lambda: questrade_import(), width=button_width, height=button_height, bg=button_color1, fg=button_text_color1)
button_import_executions.grid(column=40, row=0)
# ============================================================================
# ========== USERS FRAME FUNCTIONS ===========================================
# ============================================================================
def submit_name():
	new_name = (Users(user_name = entry_user_name.get(),first_name = entry_first_name.get(), last_name = entry_last_name.get()))
	#session.flush()
	session.add(new_name)
	session.commit()
	clear_name()
	query_names()
	#entry_ma_owner.set(query_names())
def clear_name():
	entry_user_name.delete(0,END)
	entry_first_name.delete(0,END)
	entry_last_name.delete(0,END)
def query_names():
	# CLEAR TREE
	tree_users.delete(*tree_users.get_children())
	tree_users.update()
	# CONNECT TO TABLE
	try:
		census = Table('users', metadata, autoload=True, autoload_with=engine)
		records = session.execute(select([census])).fetchall()
		#Create name list for dropdown
		user_name_list = session.execute(select(Users.user_name))
		name_list=[]
		for row in user_name_list:
			name_list.append(''.join(row))
		print("name list:",name_list)
		headers = census.columns.keys()
		# PRINT COLUMN HEADINGS
		tree_users['columns'] = headers
		tree_users['show']= 'headings'
		for column in tree_users['columns']:
			tree_users.heading(column, text=column, anchor=W)
			tree_users.column(column, width=80)
		# PRINT ROWS
		for row in records:
			row = list(row) # convert tup to list
			tree_users.insert("", "end", values=row)
		tree_users.bind('<ButtonRelease-1>', user_record_clicked)
		#return name_list
		return name_list
	except Exception:
		print(Exception)
		print("There is an issue with the user table")
def delete_name():
	key_to_delete = get_user_selected('e')[0]
	print("about to delete user id :", key_to_delete) 
	stmt = session.query(Users).get(key_to_delete)
	session.delete(stmt)
	session.commit()
	clear_name()
	query_names()
def update_user():
	user_id = get_user_selected('e')[0]
	print('user_id :',user_id)
	x = session.query(Users).get(user_id)
	x.user_name = entry_user_name.get()
	x.first_name = entry_first_name.get()
	x.last_name = entry_last_name.get()
	session.commit()
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
	entry_user_name.insert(0,selected_user[0])
	entry_first_name.insert(0,selected_user[1])
	entry_last_name.insert(0,selected_user[2])
	return selected_user
def import_users():	
	excel_file_full_path = filedialog.askopenfilename(initialdir=backup_folder, title="Select Excel Workbook", filetypes=(("xlsx Fiel", ".xlsx"),("All Files","*.*")))
	print('Restore file : ',excel_file_full_path)
	df_users = pd.read_excel(excel_file_full_path,sheet_name = 'users')
	df_master_accounts = pd.read_excel(excel_file_full_path,sheet_name = 'master_accounts')
	display(df_users)
	with engine.begin() as conn:
		df_users.to_sql(con=conn,name='users',if_exists='append', index=False)
		#df_master_accounts.to_sql(con=conn,name='master_accounts',if_exists='append', index=False)
	session.commit()
	query_names()

# ---------------------------------------------------------------------------
# ----- USER BUTTONS --------------------------------------------------------
# ---------------------------------------------------------------------------
label_user_name = Label(frame_user_buttons, text='User Name')
label_user_name.grid(row = 0, column = 0)
entry_user_name = Entry(frame_user_buttons, width=30)
entry_user_name.grid(row=0, column=1, padx=0)
label_first_name = Label(frame_user_buttons, text='First Name')
label_first_name.grid(row = 1, column = 0)
entry_first_name = Entry(frame_user_buttons, width=30)
entry_first_name.grid(row=1, column=1, padx=0)
label_last_name = Label(frame_user_buttons, text='Last Name')
label_last_name.grid(row = 2, column = 0)
entry_last_name = Entry(frame_user_buttons, width=30)
entry_last_name.grid(row=2, column=1, padx=0)
button_user_submit = Button(frame_user_buttons, text = "Add", command=submit_name)
button_user_submit.grid(row = 3, column=0, columnspan=1, pady=0, padx=0, ipadx=20)
button_user_delete = Button(frame_user_buttons, text = "Delete", command=delete_name)
button_user_delete.grid(row =4, column=0, columnspan=1, pady=0, padx=0,ipadx=10)
button_update_user = Button(frame_user_buttons, text = "Update", command=update_user)
button_update_user.grid(row =5, column=0, columnspan=1, pady=0, padx=0, ipadx=10)
button_clear_user = Button(frame_user_buttons, text = "Clear", command=clear_name)
button_clear_user.grid(row = 3, column=1, columnspan=1, pady=0, padx=0, ipadx=10)
button_user_query = Button(frame_user_buttons, text = "Refresh", command=query_names)
button_user_query.grid(row =4, column=1, columnspan=1, pady=0, padx=0, ipadx=10)
button_import_users = Button(frame_user_buttons, text = "Import", command=import_users)
button_import_users.grid(row =5, column=1, columnspan=1, pady=0, padx=0, ipadx=10)

# ========================================================================
# ========== MASTER ACCOUNT FUNCTIONS ====================================
# ========================================================================
def submit_ma():
	if entry_ma_name.get() =="":
		print("Master Account Name Cannot be NILL!")
	else:
		try:
			new_name = (Master_accounts(broker = entry_broker.get(), account_name = entry_ma_name.get(),account_number = null(), owner = entry_ma_owner.get(), include = 0))
			session.add(new_name)
			session.commit()
		except Exception:
			session.rollback()
			session.commit()
		clear_ma()
		query_ma()
def clear_ma():
	entry_ma_name.delete(0,END)
	entry_ma_owner.delete(0,END)
	entry_broker.delete(0,END)
def query_ma():
	# CLEAR TREE
	tree_ma.delete(*tree_ma.get_children())
	tree_ma.update()
	#entry_ma_owner.set(query_names())
	#entry_ma_owner.update()
	#tree_ma.update()
	# CONNECT TO TABLE
	try:
		census = Table('master_accounts', metadata, autoload=True, autoload_with=engine)
		records = session.execute(select([census])).fetchall()
		#print("records:",records)
		headers = census.columns.keys()
		# PRINT COLUMN HEADINGS
		tree_ma['columns'] = headers
		tree_ma['show']= 'headings'
		for column in tree_ma['columns']:
			tree_ma.heading(column, text=column, anchor=W)
			tree_ma.column(column, width=80)
		# PRINT ROWS
		for row in records:
			row = list(row) # convert tup to list
			tree_ma.insert("", "end", values=row)
		tree_ma.bind('<ButtonRelease-1>', ma_record_clicked)
	except Exception:
		print("There is an issue with the user table")
def delete_ma():
	key_to_delete = get_ma_selected('e')[1]
	print("about to delete ma id :", key_to_delete) 
	stmt = session.query(Master_accounts).get(key_to_delete)
	session.delete(stmt)
	session.commit()
	clear_ma()
	query_ma()
def update_ma():
	ma_id = get_ma_selected('e')[0]
	print('ma_id :',ma_id)
	x = session.query(Master_accounts).get(ma_id)
	x.broker = entry_broker.get()
	x.account_name = entry_ma_name.get()
	x.owner = entry_ma_owner.get()
	session.commit()
	clear_ma()
	query_ma()
def get_ma_selected(*args):
	selected = tree_ma.focus() # Gab record number
	values = tree_ma.item(selected, 'values') # Grap tuple of row values
	print('MA record clicked :',values)
	return values
def ma_record_clicked(*args):
	selected_ma = get_ma_selected('e')
	print('Selected MA :', selected_ma)
	clear_ma()
	entry_ma_name.insert(0,selected_ma[0])
	entry_ma_owner.insert(0,selected_ma[2])
	entry_broker.insert(0,selected_ma[3])
	return selected_ma
def import_ma():	
	excel_file_full_path = filedialog.askopenfilename(initialdir=backup_folder, title="Select Excel Workbook", filetypes=(("xlsx Fiel", ".xlsx"),("All Files","*.*")))
	print('Restore file : ',excel_file_full_path)
	df_master_accounts = pd.read_excel(excel_file_full_path,sheet_name = 'master_accounts')
	with engine.begin() as conn:
		df_master_accounts.to_sql(con=conn,name='master_accounts',if_exists='append', index=False)
	session.commit()
	query_ma()

# ---------------------------------------------------------------------------
# ----- MA BUTTONS --------------------------------------------------------
# ---------------------------------------------------------------------------
label_broker = Label(frame_ma_buttons, text='Broker')
label_broker.grid(row = 0, column = 0)
entry_broker = Entry(frame_ma_buttons, width=30)
entry_broker.grid(row=0, column=1, padx=0)
label_ma_name = Label(frame_ma_buttons, text='MA Name')
label_ma_name.grid(row = 1, column = 0)
entry_ma_name = Entry(frame_ma_buttons, width=30)
entry_ma_name.grid(row=1, column=1, padx=0)
label_ma_number = Label(frame_ma_buttons, text='MA Number')
label_ma_number.grid(row = 2, column = 0)
label_ma_owner = Label(frame_ma_buttons, text='MA Owner')
label_ma_owner.grid(row = 3, column = 0)
entry_ma_owner = ttk.Combobox(frame_ma_buttons, value=query_names())
entry_ma_owner.grid(row = 3, column=1)
button_ma_submit = Button(frame_ma_buttons, text = "Add", command=submit_ma)
button_ma_submit.grid(row = 6, column=0, columnspan=1, pady=0, padx=0, ipadx=20)
button_ma_delete = Button(frame_ma_buttons, text = "Delete", command=delete_ma)
button_ma_delete.grid(row =7, column=0, columnspan=1, pady=0, padx=0,ipadx=20)
button_update_ma = Button(frame_ma_buttons, text = "Update", command=update_ma)
button_update_ma.grid(row =8, column=0, columnspan=1, pady=0, padx=0, ipadx=20)
button_clear_ma = Button(frame_ma_buttons, text = "Clear", command=clear_ma)
button_clear_ma.grid(row = 6, column=1, columnspan=1, pady=0, padx=0, ipadx=20)
button_ma_query = Button(frame_ma_buttons, text = "Refresh", command=query_ma)
button_ma_query.grid(row =7, column=1, columnspan=1, pady=0, padx=0, ipadx=20)
button_import_ma = Button(frame_ma_buttons, text = "Import", command=import_ma)
button_import_ma.grid(row =8, column=1, columnspan=1, pady=0, padx=0, ipadx=20)

# ========================================================================
# ========== ACCOUNT FUNCTIONS ====================================
# ========================================================================
def clear_account():
	entry_account_owner.delete(0,END)
	label_account_type.config(text="Type")
	label_account_number.config(text="Account Number")
	label_master_account.config(text="Master Account")
	label_client_type.config(text="Client Type")
	var_include = ""
def query_accounts():
	# CLEAR TREE
	tree_accounts.delete(*tree_accounts.get_children())
	tree_accounts.update()
	# CONNECT TO TABLE
	try:
		census = Table('accounts', metadata, autoload=True, autoload_with=engine)
		records = session.execute(select([census])).fetchall()
		#print("records:",records)
		headers = census.columns.keys()
		# PRINT COLUMN HEADINGS
		tree_accounts['columns'] = headers
		tree_accounts['show']= 'headings'
		for column in tree_accounts['columns']:
			tree_accounts.heading(column, text=column, anchor=W)
			tree_accounts.column(column, width=90)
		# PRINT ROWS
		for row in records:
			row = list(row) # convert tup to list
			tree_accounts.insert("", "end", values=row)
		tree_accounts.bind('<ButtonRelease-1>', account_record_clicked)
	except Exception:
		print("There is an issue with the user table")
def delete_account():
	key_to_delete = get_ma_selected('e')[0]
	print("about to delete ma id :", key_to_delete) 
	stmt = session.query(Master_accounts).get(key_to_delete)
	session.delete(stmt)
	session.commit()
	clear_ma()
	query_ma()
def update_account():
	account_id = get_account_selected('e')[0]
	print('account_id :',account_id)
	x = session.query(Accounts).get(account_id)
	x.user_id = entry_account_owner.get()
	print("check box :",var_include.get())
	x.include = var_include.get()
	#x.include = check_include.get()
	session.commit()
	clear_account()
	query_accounts()
def get_account_selected(*args):
	selected = tree_accounts.focus() # Gab record number
	values = tree_accounts.item(selected, 'values') # Grap tuple of row values
	print('Account record clicked :',values)
	return values
def account_record_clicked(*args):
	clear_account()
	selected_account = get_account_selected('e')
	print('Selected Account :', selected_account)
	label_account_type.config(text=selected_account[0])
	label_account_number.config(text=selected_account[1])
	label_client_type.config(text=selected_account[3])
	label_master_account.config(text=selected_account[4])
	entry_account_owner.insert(0,selected_account[5])
	#entry_ma_owner.insert(0,selected_ma[2])
	return selected_account
def import_accounts():	
	excel_file_full_path = filedialog.askopenfilename(initialdir=backup_folder, title="Select Excel Workbook", filetypes=(("xlsx Fiel", ".xlsx"),("All Files","*.*")))
	print('Restore file : ',excel_file_full_path)
	df_accounts = pd.read_excel(excel_file_full_path,sheet_name = 'accounts')
	with engine.begin() as conn:
		df_accounts.to_sql(con=conn,name='accounts',if_exists='append', index=False)
	session.commit()
	query_accounts()

# ---------------------------------------------------------------------------
# ----- ACCOUNT BUTTONS --------------------------------------------------------
# ---------------------------------------------------------------------------
label_account_type = Label(frame_account_buttons, text='Type')
label_account_type.grid(row = 0, column = 0)
label_account_number = Label(frame_account_buttons, text='Number')
label_account_number.grid(row=1, column=0)
label_client_type = Label(frame_account_buttons, text='Client Type')
label_client_type.grid(row = 2, column = 0)
label_master_account = Label(frame_account_buttons, text='Master Account')
label_master_account.grid(row = 3, column = 0)
label_account_owner = Label(frame_account_buttons, text='Account Owner')
label_account_owner.grid(row = 4, column = 0)
entry_account_owner = ttk.Combobox(frame_account_buttons, value=query_names())
entry_account_owner.grid(row = 4, column = 1)
var_include = IntVar()
check_include = Checkbutton(frame_account_buttons, text='Include', variable=var_include, onvalue=1, offvalue=0)
check_include.grid(row = 5, column = 0)

button_account_delete = Button(frame_account_buttons, text = "Delete", command=delete_account)
button_account_delete.grid(row =7, column=0, columnspan=1, pady=0, padx=0,ipadx=20)
button_update_account = Button(frame_account_buttons, text = "Update", command=update_account)
button_update_account.grid(row =8, column=0, columnspan=1, pady=0, padx=0, ipadx=20)
button_clear_account = Button(frame_account_buttons, text = "Clear", command=clear_account)
button_clear_account.grid(row = 6, column=1, columnspan=1, pady=0, padx=0, ipadx=20)
button_account_query = Button(frame_account_buttons, text = "Refresh", command=query_accounts)
button_account_query.grid(row =7, column=1, columnspan=1, pady=0, padx=0, ipadx=20)
button_import_accounts = Button(frame_account_buttons, text = "Import", command=import_accounts)
button_import_accounts.grid(row =8, column=1, columnspan=1, pady=0, padx=0, ipadx=20)

# =====================================================
# ====== END MAINLOOP =================================
# =====================================================
query_names()
query_ma()
query_accounts()
root.mainloop()
#session.commit()	
session.close()	