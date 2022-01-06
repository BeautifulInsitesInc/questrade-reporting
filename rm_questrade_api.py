# https://pypi.org/project/questrade-api/
import os
import json
import time
from urllib import request
from datetime import datetime, timedelta
import configparser
import urllib
import pandas as pd
from pytz import timezone
import sys
from IPython.display import display
from tkinter import ttk, filedialog, simpledialog

# ---------------- SET TOKEN PATH ------------------
# SET GLOBAL TOKEN_PATH BASED ON MASTER ACCOUNT
def token_path_set(account):
    global TOKEN_PATH
    token_file_path ='D:\Dropbox\Test folder'
    TOKEN_PATH = token_file_path+'/'+account+'-questrade.json'
    print('Token Path Set : ',TOKEN_PATH)
    return TOKEN_PATH

#def get_new_token(): # For first time, or if failed
#   access_token = simpledialog.askstring(title="ACCESS TOKEN", prompt='New Token : ')
#    print('access_token set in questrade_api = ',access_token)
#   return access_token

# ================================================================
# ==============  QUESTRADE API WRAPPER ==========================
# ================================================================

CONFIG_PATH = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'questrade.cfg')

class Questrade:
    def __init__(self, **kwargs):
        if 'config' in kwargs:
            self.config = self.__read_config(kwargs['config'])
        else:
            self.config = self.__read_config(CONFIG_PATH)

        auth_kwargs = {x: y for x, y in kwargs.items() if x in
                       ['token_path', 'refresh_token']}
        ########################### Here is were the JASON is decoded
        print('***auth_kwargs : ',auth_kwargs)

        self.auth = Auth(**auth_kwargs, config=self.config)

    def __read_config(self, fpath):
        config = configparser.ConfigParser()
        with open(os.path.expanduser(fpath)) as f:
            config.read_file(f)
        return config

    @property
    def __base_url(self):
        return self.auth.token['api_server'] + self.config['Settings']['Version']

    def __build_get_req(self, url, params):
        if params:
            url = self.__base_url + url + '?' + urllib.parse.urlencode(params)
            return urllib.request.Request(url)
        else:
            return urllib.request.Request(self.__base_url + url)

    def __get(self, url, params=None):
        req = self.__build_get_req(url, params)
        req.add_header(
            'Authorization',
            self.auth.token['token_type'] + ' ' +
            self.auth.token['access_token']
        )
        try:
            r = urllib.request.urlopen(req)
            return json.loads(r.read().decode('utf-8'))  # loading from json file - replace with database
        except urllib.error.HTTPError as e:
            return json.loads(e.read().decode('utf-8'))

# ******************** Here is were it may be sending to json file
    def __build_post_req(self, url, params):
        url = self.__base_url + url
        print('***** __buld_post_ret url, params : ',url, params)# trying to see what it does
        return urllib.request.Request(url, data=json.dumps(params).encode('utf8'))


    def __post(self, url, params):
        req = self.__build_post_req(url, params)
        req.add_header(
            'Authorization',
            self.auth.token['token_type'] + ' ' +
            self.auth.token['access_token']
        )
    # Here is were it is loading the json file I think
        try:
            r = urllib.request.urlopen(req)
            return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return json.loads(e.read().decode('utf-8'))

    @property
    def __now(self):
        return datetime.now().astimezone().isoformat('T')

    def __days_ago(self, d):
        now = datetime.now().astimezone()
        return (now - timedelta(days=d)).isoformat('T')

    @property
    def time(self):
        return self.__get(self.config['API']['time'])

    @property
    def accounts(self):
        return self.__get(self.config['API']['Accounts'])

    def account_positions(self, id):
        return self.__get(self.config['API']['AccountPositions'].format(id))

    def account_balances(self, id):
        return self.__get(self.config['API']['AccountBalances'].format(id))

    def account_executions(self, id, **kwargs):
        return self.__get(self.config['API']['AccountExecutions'].format(id), kwargs)

    def account_orders(self, id, **kwargs):
        if 'ids' in kwargs:
            kwargs['ids'] = kwargs['ids'].replace(' ', '')
        return self.__get(self.config['API']['AccountOrders'].format(id), kwargs)

    def account_order(self, id, order_id):
        return self.__get(self.config['API']['AccountOrder'].format(id, order_id))

    def account_activities(self, id, **kwargs):
        if 'startTime' not in kwargs:
            kwargs['startTime'] = self.__days_ago(1)
        if 'endTime' not in kwargs:
            kwargs['endTime'] = self.__now
        return self.__get(self.config['API']['AccountActivities'].format(id), kwargs)

    def symbol(self, id):
        return self.__get(self.config['API']['Symbol'].format(id))

    def symbols(self, **kwargs):
        if 'ids' in kwargs:
            kwargs['ids'] = kwargs['ids'].replace(' ', '')
        return self.__get(self.config['API']['Symbols'].format(id), kwargs)

    def symbols_search(self, **kwargs):
        return self.__get(self.config['API']['SymbolsSearch'].format(id), kwargs)

    def symbol_options(self, id):
        return self.__get(self.config['API']['SymbolOptions'].format(id))

    @property
    def markets(self):
        return self.__get(self.config['API']['Markets'])

    def markets_quote(self, id):
        return self.__get(self.config['API']['MarketsQuote'].format(id))

    def markets_quotes(self, **kwargs):
        if 'ids' in kwargs:
            kwargs['ids'] = kwargs['ids'].replace(' ', '')
        return self.__get(self.config['API']['MarketsQuotes'], kwargs)

    def markets_options(self, **kwargs):
        return self.__post(self.config['API']['MarketsOptions'], kwargs)

    def markets_strategies(self, **kwargs):
        return self.__post(self.config['API']['MarketsStrategies'], kwargs)

    def markets_candles(self, id, **kwargs):
        if 'startTime' not in kwargs:
            kwargs['startTime'] = self.__days_ago(1)
        if 'endTime' not in kwargs:
            kwargs['endTime'] = self.__now
        return self.__get(self.config['API']['MarketsCandles'].format(id), kwargs)

# ========================================================================
# ================ AUTH CLASS ============================================
# ========================================================================

# Needs TOKEN_PATH Global set

class Auth:
    def __init__(self, **kwargs):
        if 'config' in kwargs:
            self.config = kwargs['config']
        else:
            raise Exception('No config supplied')
        if 'token_path' in kwargs:
            self.token_path = kwargs['token_path']
        else:
            self.token_path = TOKEN_PATH
        if 'refresh_token' in kwargs:
            self.__refresh_token(kwargs['refresh_token'])

# readong the json file lets print out and see what its doing
    def __read_token(self):
        try:
            with open(self.token_path) as f:
                str = f.read()
                print(' __read_token str :', str, 'json.loads(str) :', json.loads(str))
                return json.loads(str)
        except IOError:
            raise('No token provided and none found at {}'.format(TOKEN_PATH))

    def __write_token(self, token):
        with open(self.token_path, 'w') as f:
            json.dump(token, f)
        os.chmod(self.token_path, 0o600)

# more json 
    def __refresh_token(self, token):
        req_time = int(time.time())
        r = request.urlopen(self.config['Auth']['RefreshURL'].format(token))
        if r.getcode() == 200:
            token = json.loads(r.read().decode('utf-8'))
            token['expires_at'] = str(req_time + token['expires_in'])
            self.__write_token(token)

    def __get_valid_token(self):
        try:
            self.token_data
        except AttributeError:
            self.token_data = self.__read_token()
        finally:
            if time.time() + 60 < int(self.token_data['expires_at']):
                return self.token_data
            else:
                self.__refresh_token(self.token_data['refresh_token'])
                self.token_data = self.__read_token()
                return self.token_data

    @property
    def token(self):
        return self.__get_valid_token()

# =============== SET INITIAL ACCESS TOKEN =======================
def token_registration_set(access_token,account):
    token_path_set(account)
    q = Questrade(refresh_token=access_token)
    print('Token registered: ',q)
    return q

# ========== AFTET TOKEN IS REGISTERED USE THIS =================
#def refresh_token_set(account):
#	token_path_set(account)
#	q = Questrade()
#	print('Refresh token retrieved om refresh_token_set(): ',q)
#	return q

#============== SERVER TIME ========================
def server_time(q):
    st=q.time
    server_time = st.get('time')
    #print('Server Time fuction succesful : ', server_time)
    return(server_time)

def time_name(q):
    timename = server_time(q).replace(':','-')
    print('server time afer replace :',timename)
    return(timename)

def start_date(q,days_back):
    date_part = server_time(q)[:10]
    rest_of_it = server_time(q)[10:]
    date_format = "%Y-%m-%d"
    date_object = datetime.strptime(date_part, date_format)
    tdelta = timedelta(days=days_back)
    last_month_date_obj = date_object - tdelta
    last_month = last_month_date_obj.strftime(date_format)
    start = last_month + rest_of_it
    #print('start date : ',start)
    return start

# ================== ALL IN ONE TOKEN REFRESH ================
def allinone_token_set(account):
    try:
        print("trying q=Questrade(): account=",account)
        token_path_set(account)
        #q = refresh_token_set(account)
        q = Questrade()
        print('Refresh token retrieved in allinone_token_set : ',q)
        st = server_time(q)
        print('successful! server_time =',st)
    except Exception:
        print('There is an issue with the token ')
        #aio_token_label.config(text = "Huston, We Have A Problem! - Token needs to be reset")
        #access_token = get_new_token()
        access_token = simpledialog.askstring(title="ACCESS TOKEN", prompt='New Token : ')
        q =token_registration_set(access_token,account)
        print('Refresh token retrieved : ',q)
        try:
            server_time()
            print('successful!')
            aio_token_label.config(text = "NEW REGISTRATION SUCCCESFUL! - "+master_account)
        except Exception:
            print('WE HAVE A BIGGER PROBLEM')

    print('allinone_token_set ran and break q=',q,'account = ',account)

    return q

# =============================== ACCOUNTS ======================================
def accounts(q):
    dict_accounts = q.accounts
    user_id = q.accounts['userId']
    #print('user_id = ', user_id)
    df = pd.DataFrame.from_dict(q.accounts['accounts']) #de-nest the accounts dict and make df
    #print('running accounts : ',df)
    return (df, user_id)

# ===================== BALANCES ==========================================
def balances(q,id):
    dict_balances = q.account_balances(id)
    df_combined_balances3 = pd.DataFrame.from_dict(dict_balances['sodPerCurrencyBalances'])# sod per Currency balances : The MOST ACCURATE to what is shown in account.
    df_combined_balances3 = df_combined_balances3.drop(['isRealTime'], axis=1)
    df_combined_balances4 = pd.DataFrame.from_dict(dict_balances['sodCombinedBalances'])# sod combined balances : Combined totals of sod per currency for use in 3rd row
    df_combined_balances4 = df_combined_balances4.drop(['isRealTime'], axis=1)
    #display(df_combined_balances3)
    #display(df_combined_balances4)
    return (df_combined_balances3, df_combined_balances4)

# ===================  POSITIONS ==========================================
def positions(q,id):
    dict_positions = q.account_positions(id)
    position_list = dict_positions['positions']
    df_positions = pd.DataFrame.from_dict(position_list)
    return df_positions

# ====================== ORDERS =============
def orders(q,id):
    dict_orders = q.account_orders(id, startTime=start_date(q,28))
    df_orders = pd.DataFrame.from_dict(dict_orders['orders'])
    #display(df_orders)
    return df_orders

# ================  EXECUTIONS ============================================
def executions(q,id):
    start_datex = start_date(q,200)
    dict_executions = q.account_executions(id, startTime=start_date(q,200))
    print('getting exececutions, start_date :',start_datex)
    df_executions = pd.DataFrame.from_dict(dict_executions['executions'])
    display(df_executions)
    return df_executions

# ================   ACCOUNT ACTIVITIES ===================================
# Only gets 30 days max
def activities(q,id):
    dict_activities = q.account_activities(id, startTime=start_date(q,30))
    df_activities = pd.DataFrame.from_dict(dict_activities['activities'])
    display(df_activities)
    return df_activities
