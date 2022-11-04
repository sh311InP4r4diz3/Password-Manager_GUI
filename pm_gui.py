from tkinter import *
import tkinter.messagebox as MessageBox
import pymysql
from cryptography.fernet import Fernet
import pyperclip as pc


def main_sql_connect():
    host = hostname.get()
    u = username.get()
    p = password.get()
    d = dbname.get()
    return pymysql.connect(host=host, user=u, password=p, database=d)

def sql_config():
    host = hostname.get()
    u = username.get()
    p = password.get()
    d = dbname.get()

    if (host == "" or u == "" or p == "" or d == ""):
        MessageBox.showinfo("Insert status", "All fields are required")
    else:
        try:
            mydb = pymysql.connect(host=host,user=u,password=p)
            mycursor = mydb.cursor()
            mycursor.execute("SHOW DATABASES")
            results = [db[0] for db in mycursor.fetchall()]
            if d not in results:
                #print("Create new DB")
                mycursor = mydb.cursor()
                query = (f"CREATE DATABASE {d}")
                mycursor.execute(query)
                #print("New DB Created and connected to DB, Use this DB for future logins")
                mydb.close()
                MessageBox.showinfo("Login", "New DB Created and connected to DB, Use this DB for future logins")
                root.withdraw()
                after_login()
                return main_sql_connect()
            else:
                Label(root, text= "Connected to DB", fg="green", font=("calibri", 11)).pack()
                root.withdraw()
                after_login()
                return main_sql_connect()
        except (pymysql.err.ProgrammingError, pymysql.err.OperationalError):
            err = "Connection refused, Try restarting MYSQL server!"
            #print(err)
            MessageBox.showinfo("Error", err)
def log_in(k):
    conn = main_sql_connect()
    #k = maskpass.askpass(prompt="Enter your masterkey: ")
    if check_passwords(k):
        #print("LoggingIn.....\n")
        return True
    if check_passwords(k) == None or check_passwords(k) == False:
        MessageBox.showinfo("ERROR", "Incorrect key")
def create_newtable():
    conn = main_sql_connect()
    try:
        mycursor = conn.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS credentials(master_key TEXT NOT NULL)")
        mycursor.execute("CREATE TABLE IF NOT EXISTS web_creds(website TEXT NOT NULL, password TEXT NOT NULL)")
        return True
    except pymysql.err.ProgrammingError as e:
        e= "There is an error while executing query."
        #print(e)
        return False
def generateKey():
    if check_for_existing_keys() == None:
        key = Fernet.generate_key()
        key_decoded = key.decode()
        store_keys_to_db(key_decoded)
        pc.copy(key_decoded)
        return key_decoded
    else:
        insert1 = Button(after_login, text='Generate Key', font=("bold", 8), bg='green', command=generateKey, state=DISABLED)
        insert1.place(x=40, y=40)
        insert2 = Button(after_login, text='Store Credentials to DB', font=("bold", 8), bg='green', command=login1, state=NORMAL)
        insert2.place(x=40, y=70)

        insert3 = Button(after_login, text='Retrieve Data', font=("bold", 8), bg='green', command=login2, state=NORMAL)
        insert3.place(x=40, y=100)

        insert4 = Button(after_login, text='Delete DB', font=("bold", 8), bg='green', command=login3, state=NORMAL)
        insert4.place(x=40, y=130)
        #MessageBox.showinfo("ERROR", "keys exists in DB, Use Previously generated key to login (or) Delete database")

def store_keys_to_db(key):
    conn = main_sql_connect()
    if create_newtable():
        mycursor = conn.cursor()
        query = "INSERT INTO credentials (master_key) VALUES (%s)"
        mycursor.execute(query, (key))
        conn.commit()
        #print('[+]Inserted')
        MessageBox.showinfo("Info", "Key is generated and copied to clipboard, Use this key for future logins")
        conn.close()
    else:
        return False
def check_passwords(k):
    conn = main_sql_connect()
    try:
        mycursor = conn.cursor()
        query = f"SELECT DISTINCT master_key FROM credentials WHERE master_key='{k}'"
        mycursor.execute(query)
        results = mycursor.fetchone()
        #print(results)
        if results != None:
            for row in results:
                insert1 = Button(after_login, text='Generate Key', font=("bold", 8), bg='green', command=generateKey, state=DISABLED)
                insert1.place(x=40, y=40)

                if row == k:
                    return True
                else:
                    return False
        if results == None:
            return None
            MessageBox.showinfo("ERROR", "Data not exists")
    except pymysql.err.ProgrammingError as e:
        e ="Incorrect key"
        MessageBox.showinfo("ERROR", e)
def check_for_existing_keys():
    conn = main_sql_connect()
    try:
        mycursor = conn.cursor()
        query = f"SELECT * FROM credentials"
        mycursor.execute(query)
        results = mycursor.fetchall()
        #print(results)
        if results == None:
            return None

        else:
            return True
    except pymysql.err.ProgrammingError as e:
        e= "Data not exists"
        #print("Data not exists")
def store_data():
    w = website.get()
    p = pword.get()
    m = mkey.get()
    if (w == "" or p =="" or m ==""):
        MessageBox.showinfo("Store data", "All fields are required")
    else:
        if create_newtable():
            try:
                conn = main_sql_connect()
                if check_passwords(m):
                    password_encode = p.encode()
                    encrypted_key = m.encode()
                    f = Fernet(encrypted_key)
                    encrypted_password = f.encrypt(password_encode)
                    decoded_password = encrypted_password.decode()
                    mycursor = conn.cursor()
                    query = f"INSERT INTO web_creds(website, password) VALUES ('{w}', '{decoded_password}')"
                    mycursor.execute(query)
                    conn.commit()
                    MessageBox.showinfo("Info", "Data Stored to DB")
                    web.delete(0, END)
                    pd.delete(0, END)
                    mk.delete(0, END)
                    conn.close()
                else:
                    MessageBox.showinfo("Store data", ":Create account to store passwords")
            except (pymysql.err.ProgrammingError, pymysql.err.OperationalError):
                e = "Incorrect Key"
                MessageBox.showinfo("Info", e)
def decrypt_password(p, m):
    try:
        #retype_mk = maskpass.askpass("Re-Type master key: ")
        encoded01 = p.encode()
        encoded02 = m.encode()
        key01 = Fernet(encoded02)
        d_pasword = key01.decrypt(encoded01)
        decoded_form = d_pasword.decode()
        pc.copy(decoded_form)
        MessageBox.showinfo("Info", "Copied to clipboard")
    except:
        MessageBox.showinfo("Error", "Incorrect key")
def retrieve_data():
    to_retrieve_data = rdata.get()
    mk = mskey.get()
    if (to_retrieve_data == "" or mk == ""):
        MessageBox.showinfo("ERROR", "All fields are required")
    else:
        conn = main_sql_connect()
        try:
            if log_in(mk):
                mycursor = conn.cursor()
                query=f"SELECT DISTINCT website, password FROM web_creds WHERE website='{to_retrieve_data}'"
                mycursor.execute(query)
                query1 = [item[0:] for item in mycursor.fetchall()]
                if query1 == []:
                    MessageBox.showinfo("ERROR", "Data not exists")
                    w_entry.delete(0, END)
                    m_entry.delete(0, END)
                if query1 != []:    
                    for i in query1:
                        for row in i:
                            if len(row) > 15:
                                decrypt_password(row, mk)
                                w_entry.delete(0, END)
                                m_entry.delete(0, END)
                       
        except (pymysql.ProgrammingError, pymysql.err.OperationalError):
            e ="Connection refused"
            MessageBox.showinfo("ERROR", e)
def delete_data():
    msk2 = mskey1.get()
    db_1 = d_db.get()
    if (msk2 == "" or db_1 == ""):
        MessageBox.showinfo("ERROR", "All fields are required.")
    else:
        try:
            if log_in(msk2):
                conn = main_sql_connect()
                #db_name = input("Enter DB name to DELETE: ")
                mycursor=conn.cursor()
                mycursor.execute(f"DROP DATABASE {db_1}")
                MessageBox.showinfo("delete data", "Data erased!")
                d_db_entry.delete(0, END)
                mskey_entry.delete(0, END)
                mycursor.execute(f"SHOW DATABASES")
                results = [items[0] for items in mycursor.fetchall()]
                if len(results) == 4:
                    insert1 = Button(after_login, text='Generate Key', font=("bold", 8), bg='green', command=generateKey, state=DISABLED)
                    insert1.place(x=40, y=40)
                    insert1 = Button(after_login, text='Generate Key', font=("bold", 8), bg='green', command=generateKey, state=DISABLED)
                    insert1.place(x=40, y=40)
                    insert2 = Button(after_login, text='Store Credentials to DB', font=("bold", 8), bg='green', command=login1, state=DISABLED)
                    insert2.place(x=40, y=70)
                    insert3 = Button(after_login, text='Retrieve Data', font=("bold", 8), bg='green', command=login2, state=DISABLED)
                    insert3.place(x=40, y=100)
                    insert4 = Button(after_login, text='Delete DB', font=("bold", 8), bg='green', command=login3, state=DISABLED)
                    insert4.place(x=40, y=130)
                else:
                    return None
            
        except pymysql.err.OperationalError as e:
            e="Unknown Database"
            MessageBox.showinfo("ERROR", e)
def scratch():
    global root
    root = Tk()
    root.geometry("500x500")
    root.title("Password Manager: Login")

    frame = LabelFrame(root, text="", bd=10, bg='bisque4')
    frame.pack(fill="both", expand="yes", padx=20, pady=20)
    global hostname
    global username
    global password
    global dbname
   
    hostname = StringVar()
    username = StringVar()
    password = StringVar()
    dbname = StringVar()

    Label(frame, text='Enter hostname', font=('Times 12 italic bold')).place(x=40, y=20)
    Label(frame, text='Enter username', font=('Times 12 italic bold')).place(x=40, y=50)
    Label(frame, text='Enter your password', font=('Times 12 italic bold')).place(x=40, y=80)
    Label(frame, text="Enter your DB name", font=('Times 12 italic bold')).place(x=40, y=110)
    u_host = Entry(frame, textvariable= hostname).place(x=195, y=20)
    u_name = Entry(frame, textvariable=username).place(x=195, y=50)
    u_p = Entry(frame,show="*", textvariable=password).place(x=195, y=80)
    u_d = Entry(frame, textvariable=dbname).place(x=195, y=110)
    insert = Button(frame, text='Login', font=("roman", 9), command=sql_config).place(x=115, y=180)
    insert0 = Button(frame, text='Quit', font=("roman", 9), command=root.destroy).place(x=230, y=180)
    root.mainloop()
    return None

def after_login():
    global after_login
    global insert1
    global insert2
    global insert3
    global insert4
    after_login = Toplevel(root)
    after_login.geometry("300x300")
    after_login.title("Password Manager")

    insert1 = Button(after_login, text='Generate Key', font=("bold", 8), bg='green', command=generateKey, state=NORMAL)
    insert1.place(x=40, y=40)

    insert2 = Button(after_login, text='Store Credentials to DB', font=("bold", 8), bg='green', command=login1, state=DISABLED)
    insert2.place(x=40, y=70)

    insert3 = Button(after_login, text='Retrieve Data', font=("bold", 8), bg='green', command=login2, state=DISABLED)
    insert3.place(x=40, y=100)

    insert4 = Button(after_login, text='Delete DB', font=("bold", 8), bg='green', command=login3, state=DISABLED)
    insert4.place(x=40, y=130)

    insert5 = Button(after_login, text='Quit', font=("bold", 8), bg='white', command=root.destroy)
    insert5.place(x=120, y=180)

    return None

def login1():
    global after_login1
    after_login1 = Toplevel(root)
    after_login1.geometry("280x280")
    after_login1.title("Store Credentials")
    global website
    global pword
    global mkey
    global web
    global pd
    global mk
    website = StringVar()
    pword = StringVar()
    mkey = StringVar()

    frame1 = LabelFrame(after_login1, text="", padx=5, pady=10)
    frame1.pack(padx=5, pady=10)
    Label(frame1, text="Enter WebSiteName", padx=5, pady=2).pack()
    web = Entry(frame1, textvariable=website)
    web.pack()
    Label(frame1, text="Enter Password", padx=5, pady=5).pack()
    pd = Entry(frame1, show="*",textvariable=pword)
    pd.pack()
    Label(frame1, text="Enter MasterKey", padx=5, pady=5).pack()
    mk = Entry(frame1, show="*", textvariable=mkey)
    mk.pack()
    Label(frame1, text= "").pack()
    insert6 = Button(frame1, text="Store", font=("bold", 8), command=store_data)
    insert6.pack(side=LEFT)
    #y.place(x=30, y=60)
    insert7 = Button(frame1, text="Back to Menu", font=("bold", 8), command=after_login1.destroy)
    insert7.pack(side=RIGHT)

  
    after_login1.mainloop()

def login2():
    global after_login2
    after_login2 = Toplevel(root)
    after_login2.geometry("200x200")
    after_login2.title("Retrieve Data")
    global mskey
    global rdata
    global w_entry
    global m_entry

    rdata = StringVar()
    mskey = StringVar()

    Label(after_login2, text="Enter your WebSiteName", pady=10).pack()
    w_entry = Entry(after_login2, textvariable=rdata)
    w_entry.pack()
    Label(after_login2, text="Enter your MasterKey", pady=5).pack()
    m_entry = Entry(after_login2, show="*", textvariable=mskey)
    m_entry.pack()
    insert8 = Button(after_login2, text="Retrieve", font=('bold', 8), command=retrieve_data)
    insert8.pack()
    insert9 = Button(after_login2, text="Back to Menu", font=('bold', 8), command=after_login2.destroy)
    insert9.pack()

    after_login2.mainloop()

def login3():
    global after_login3
    after_login3 = Toplevel(root)
    after_login3.geometry("280x180")
    after_login3.title("Delete data")
    global d_db
    global mskey1
    global d_db_entry
    global mskey_entry

    d_db = StringVar()
    mskey1 = StringVar()

    Label(after_login3, text="Enter DB name to Delete", pady=10).pack()
    d_db_entry = Entry(after_login3, textvariable=d_db)
    d_db_entry.pack()
    Label(after_login3, text="Enter your MasterKey", pady=5).pack()
    mskey_entry = Entry(after_login3, show="*", textvariable=mskey1)
    mskey_entry.pack()
    insert10 = Button(after_login3, text="Delete", font=('bold', 8), command=delete_data)
    insert10.pack()
    insert11 = Button(after_login3, text="Back to Menu", font=('bold', 8), command=after_login3.destroy)
    insert11.pack()
    after_login3.mainloop()

scratch()

