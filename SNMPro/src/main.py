import customtkinter
from snmp import *
from database import *
import multiprocessing
from data import *
from ml import ML
import pandas as pd
import tkinter as tk
from tkinter import ttk
import ast

class App(customtkinter.CTk):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.signup_window()
        self.ml = ML()
        self.db = DB()

    def signup_window(self):
        self.geometry(f"{360}x{350}")
        self.title("Create Account Page")
        self.current_page = "signup"
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        
        self.title_logo = customtkinter.CTkLabel(self, text="Sign Up Page", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_logo.grid(row=0, column=2, columnspan=2)
        
        self.first_name_entry = customtkinter.CTkEntry(self, placeholder_text="First Name")
        self.first_name_entry.grid(row=1, column=2, padx=(65, 0), pady=10, sticky="w")

        self.last_name_entry = customtkinter.CTkEntry(self, placeholder_text="Last Name")
        self.last_name_entry.grid(row=2, column=2, padx=(65, 0), pady=10, sticky="w")

        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.username_entry.grid(row=4, column=2, padx=(65, 0), pady=10, sticky="w")

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Password")
        self.password_entry.grid(row=5, column=2, padx=(65, 0), pady=10, sticky="w")

        self.signup_button = customtkinter.CTkButton(self, text="Create Account", command=self.signup_button_press, width=80)
        self.signup_button.grid(row=6, column=2, padx=(33, 0), pady=10, sticky="nsew")

        self.login_button = customtkinter.CTkButton(self, text="Login Page", command=self.login_button_press)
        self.login_button.grid(row=7, column=2, padx=(33, 0), pady=10, sticky="nsew")

    def login_window(self):
        self.geometry(f"{400}x{200}")
        self.title("Login Page")
        self.current_page = "login"
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.username_label_login = customtkinter.CTkLabel(self, text="Username: ")
        self.username_label_login.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        self.username_entry_login = customtkinter.CTkEntry(self)
        self.username_entry_login.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.password_label_login = customtkinter.CTkLabel(self, text="Password:  ")
        self.password_label_login.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.password_entry_login = customtkinter.CTkEntry(self)
        self.password_entry_login.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        self.try_again_label_login = customtkinter.CTkLabel(self, text="")
        self.try_again_label_login.grid(row=7, column=1)

        
    
    
    def signup_button_press(self):
        if self.current_page == "signup":
            
            first_name_val = self.first_name_entry.get()
            last_name_val = self.last_name_entry.get()
            username_val = self.username_entry.get()
            password_val = self.password_entry.get()
            
            data = {
                'firstname': [first_name_val],
                'lastname': [last_name_val],
                'username': [username_val],
                'password': [password_val]
            }

            self.data = pd.DataFrame(data)

            self.db.insert_signup_data(self.data)
            self.login_button_press()
            
        else:
            self.username_label_login.grid_forget()
            self.password_entry_login.grid_forget()
            self.username_entry_login.grid_forget()
            self.password_label_login.grid_forget()
            self.signup_window()
    
    
    def login_button_press(self):
        if self.current_page == "login":
            self.username = self.username_entry_login.get()
            self.password = self.password_entry_login.get()
            print(self.username)
            print(self.password)

            check = self.db.check_user_exists(self.username, self.password)
            if check == False:
                self.try_again_label_login.configure(text="Username or Password Incorrect Please Try Again")
            else:
                self.signup_button.grid_forget()
                self.login_button.grid_forget()
                self.username_entry_login.grid_forget()
                self.password_entry_login.grid_forget()
                self.username_label_login.grid_forget()
                self.password_label_login.grid_forget()
                self.logged_in_window()

        else:

            self.first_name_entry.grid_forget()
            self.last_name_entry.grid_forget()
            self.username_entry.grid_forget()
            self.password_entry.grid_forget()
            self.title_logo.grid_forget()
            self.signup_button.configure(text="Create Account Page")
            self.login_button.grid_forget()
            self.signup_button.grid_forget()
            self.login_button = customtkinter.CTkButton(self, text="Login", command=self.login_button_press, width=80)
            self.login_button.grid(row=7, column=2, padx=(0, 15), pady=10, sticky="nsew")
            self.signup_button = customtkinter.CTkButton(self, text="Create Account", command=self.signup_button_press, width=80)
            self.signup_button.grid(row=6, column=2, padx=(0, 15), pady=10, sticky="nsew")
            self.login_window()

    def logged_in_window(self):
        self.title("SNMPro") 
        self.geometry(f"{1180}x{500}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 4, 5, 6, 7, 8, 9, 10), weight=1)
        
        self.left_frame = customtkinter.CTkFrame(self, width=150, corner_radius=0)
        self.left_frame.grid(row=0, column=0, rowspan=11, sticky="nsew")
        self.left_frame.grid_rowconfigure(11, weight=1)
        self.title_logo = customtkinter.CTkLabel(self.left_frame, text="SNMPro", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_logo.grid(row=0, column=0, padx=60, pady=(5, 30))
        self.single_fetch = customtkinter.CTkButton(self.left_frame, text="Fetch SNMP Object", command=self.show_single_page)
        self.single_fetch.grid(column=0, row=1, pady=6)
        self.data_collection = customtkinter.CTkButton(self.left_frame, text="Fetch Periodic Data", command=self.show_periodic_page)
        self.data_collection.grid(column=0, row=2, pady=6)
        self.machine_learning = customtkinter.CTkButton(self.left_frame, text="Machine Learning", command=self.show_ml_page)
        self.machine_learning.grid(column=0, row=3, pady=6)
        self.calc_predictions = customtkinter.CTkButton(self.left_frame, text="Generate Predictions", command=self.predictions_page)
        self.calc_predictions.grid(column=0, row=4, pady=6)
        switch = customtkinter.CTkSwitch(master=self.left_frame, text="Dark Mode")
        switch.grid(row=18, column=0, padx=10, pady=(0, 20))
        self.fetch_page()
        pd.set_option('future.no_silent_downcasting', True)

  
    def fetch_page(self):
        try:
            self.periodic_frame.grid_forget()
            self.periodic2_frame.grid_forget()
            self.ml_frame.grid_forget()
            self.ml_frame2.grid_forget()
            self.prediction_frame.grid_forget()
            self.prediction_frame2.grid_forget()
        except:
            pass
        self.fetch_frame = customtkinter.CTkFrame(self)
        self.fetch_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew", columnspan=3)
        self.ip_entry1 = customtkinter.CTkEntry(master=self.fetch_frame, placeholder_text="IP Address")
        self.ip_entry1.grid(row=1, column=0, pady=10, padx=(300, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self.fetch_frame, text="Destination IP", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, pady=10)
        self.port_entry1 = customtkinter.CTkEntry(master=self.fetch_frame, placeholder_text="Port")
        self.port_entry1.grid(row=2, column=0, pady=10, padx=(300, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self.fetch_frame, text="Destination Port", anchor="w")
        self.appearance_mode_label.grid(row=2, column=0, pady=10)
        self.cstring_entry1 = customtkinter.CTkEntry(master=self.fetch_frame, placeholder_text="Community String")
        self.cstring_entry1.grid(row=3, column=0, pady=10, padx=(300, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self.fetch_frame, text="Community String", anchor="w")
        self.appearance_mode_label.grid(row=3, column=0, pady=10)
        self.option_menu1 = customtkinter.CTkOptionMenu(master=self.fetch_frame, values=["SNMPv2-MIB", "RFC1213-MIB", 'IF-MIB', 'TCP-MIB', 'UDP-MIB'], command=self.option_menu_func1)
        self.option_menu1.grid(row=1, column=1, pady=10, padx=(300, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self.fetch_frame, text="MIB Type", anchor="w")
        self.appearance_mode_label.grid(row=1, column=1, pady=10)
        self.option_menu2_1 = customtkinter.CTkOptionMenu(master=self.fetch_frame, command=self.option_menu_func2)
        self.option_menu2_1.grid(row=2, column=1, pady=10, padx=(300, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self.fetch_frame, text="Object Type", anchor="w")
        self.appearance_mode_label.grid(row=2, column=1, pady=10)
        self.option_menu2_1.set("sysDescr")
        self.index_entry1 = customtkinter.CTkEntry(master=self.fetch_frame, placeholder_text="Index")
        self.index_entry1.grid(row=3, column=1, pady=10, padx=(300, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self.fetch_frame, text="MIB Index", anchor="w")
        self.appearance_mode_label.grid(row=3, column=1, pady=10)
        button = customtkinter.CTkButton(master=self.fetch_frame, text="Fetch SNMP Object", command=self.button_click1, width=745)
        button.grid(column=(0), columnspan=2, row=7, padx=(163, 10), pady=5)
        
        self.fetch_frame2 = customtkinter.CTkFrame(master=self)
        self.fetch_frame2.grid(row=1, rowspan=9, column=1, columnspan=3, padx=15, pady=(0,15), sticky="nsew")
        columns = ('mib_desc', 'obj_value', 'time_stamp')
        self.recurrent = ttk.Treeview(self.fetch_frame2, columns=columns, show="headings")
        for col in columns:
            self.recurrent.heading(col, text=col)
        data = {
            'mib_desc': [],
            'obj_value': [],
            'time_stamp': []
        }

        for sr, ov, ts in zip(data['mib_desc'], data['obj_value'], data['time_stamp']):
            self.recurrent.insert("", tk.END, values=(sr, ov, ts))
        style = ttk.Style()
        style.configure("Custom.Treeview", background="black", foreground="white", fieldbackground="black", rowheight=25)
        self.recurrent.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
        button2 = customtkinter.CTkButton(master=self.fetch_frame2, text="Save Data", command=self.save_fetch_to_db_button_click, width=223)
        button2.grid(column=1, columnspan=1, row=1, pady=0)
        button2 = customtkinter.CTkButton(master=self.fetch_frame2, text="View Database", command=self.save_fetch_to_db_button_click, width=223)
        button2.grid(column=1, columnspan=1, row=1, pady=(120, 50))

    def option_menu_func1(self, choice):
        self.mib_choice = choice
        print(self.mib_choice)
        if self.mib_choice == "SNMPv2-MIB":
            self.option_menu2_1.configure(values=[
        "sysDescr",
        "sysObjectID",
        "sysUpTime",
        "sysContact",
        "sysName",
        "sysLocation",
        "sysServices",
        "snmpInPkts",
        "snmpOutPkts",
        "snmpInBadVersions",
        "snmpInBadCommunityNames",
        "snmpInBadCommunityUses",
        "snmpInASNParseErrs",
        "snmpSilentDrops",
        "snmpProxyDrops"
    ])
        elif self.mib_choice == "IF-MIB":
            self.option_menu2_1.configure(values= [
        "ifIndex",
        "ifAdminStatus", 
        "ifAlias", 
        "ifDescr", 
        "ifHCInOctets", 
        "ifHCOutOctets",
        "ifHCInUcastPkts", 
        "ifHCOutUcastPkts", 
        "ifInDiscards", 
        "ifInErrors",
        "ifInMulticastPkts", 
        "ifInOctets", 
        "ifInUcastPkts", 
        "ifInUnknownProtos",
        "ifLastChange", 
        "ifMtu", 
        "ifOperStatus", 
        "ifOutDiscards", 
        "ifOutErrors",
        "ifOutMulticastPkts", 
        "ifOutOctets"
    ])
        elif self.mib_choice == 'RFC1213-MIB':
            self.option_menu2_1.configure(values= [
        'ipForwarding', 
        'ipDefaultTTL', 
        'ipInReceives', 
        'ipInHdrErrors', 
        'ipInAddrErrors',
        'ipForwDatagrams', 
        'ipInUnknownProtos', 
        'ipInDiscards', 
        'ipInDelivers', 
        'ipOutRequests',
        'ipOutDiscards', 
        'ipOutNoRoutes', 
        'ipReasmTimeout', 
        'ipReasmReqds', 
        'ipReasmOKs',
        'ipReasmFails', 
        'ipFragOKs', 
        'ipFragFails', 
        'ipFragCreates',
    ])
        elif self.mib_choice == 'TCP-MIB':
            self.option_menu2_1.configure(values= [
        'tcpRtoAlgorithm', 
        'tcpRtoMin', 
        'tcpRtoMax', 
        'tcpMaxConn', 
        'tcpActiveOpens',
        'tcpPassiveOpens', 
        'tcpAttemptFails', 
        'tcpEstabResets', 
        'tcpCurrEstab', 
        'tcpInSegs',
        'tcpOutSegs', 
        'tcpRetransSegs', 
        'tcpInErrs', 
        'tcpOutRsts'
    ])
        elif self.mib_choice == 'UDP-MIB':
            self.option_menu2_1.configure(values= [
            'udpInDatagrams', 
            'udpNoPorts', 
            'udpInErrors', 
            'udpOutDatagrams'
    ])


    def option_menu_func2(self, choice2):
        self.object_choice = choice2
        print(self.object_choice)         

    def periodic_page(self):
        try:
            self.fetch_frame.grid_forget()
            self.fetch_frame2.grid_forget()
            self.ml_frame.grid_forget()
            self.ml_frame2.grid_forget()
            self.prediction_frame.grid_forget()
            self.prediction_frame2.grid_forget()
        except:
            pass
        self.periodic_frame = customtkinter.CTkFrame(master=self)
        self.periodic_frame.grid(row=0, column=1, columnspan=3, padx=15, pady=15, sticky="nsew")
        self.appearance_mode_label = customtkinter.CTkLabel(self.periodic_frame, text="Destination IP", anchor="w")
        self.appearance_mode_label.grid(row=1, column=1, pady=10, padx=10)
        self.ip_address_entry = customtkinter.CTkEntry(master=self.periodic_frame, width=200, placeholder_text="Enter IP")
        self.ip_address_entry.grid(row=1, column=2, pady=10, padx=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.periodic_frame, text="Destination Port", anchor="w")
        self.appearance_mode_label.grid(row=2, column=1, pady=10, padx=10)
        self.port_entry = customtkinter.CTkEntry(master=self.periodic_frame, width=200, placeholder_text="Enter Port")
        self.port_entry.grid(row=2, column=2, pady=10, padx=10)
        appearance_mode_label = customtkinter.CTkLabel(self.periodic_frame, text="Community String", anchor="w")
        appearance_mode_label.grid(row=3, column=1, pady=10, padx=10)
        cstring_entry = customtkinter.CTkEntry(master=self.periodic_frame, width=200, placeholder_text="Enter Community String")
        cstring_entry.grid(row=3, column=2, pady=10, padx=10)
        appearance_mode_label = customtkinter.CTkLabel(self.periodic_frame, text="MIB Index", anchor="w")
        appearance_mode_label.grid(row=1, column=3, pady=10, padx=10)
        index_entry = customtkinter.CTkEntry(master=self.periodic_frame, width=200, placeholder_text="Enter Index")
        index_entry.grid(row=1, column=4, pady=10, padx=10)
        button = customtkinter.CTkButton(master=self.periodic_frame, text="Fetch Periodic Data", command=self.button_click2, width=745)
        button.grid(column=1, columnspan=4, row=5, pady=10, padx=120)
        interval_label = customtkinter.CTkLabel(self.periodic_frame, text="Polls Interval", anchor="w")
        interval_label.grid(row=2, column=3, pady=10, padx=10)
        self.interval_entry = customtkinter.CTkEntry(master=self.periodic_frame, width=200, placeholder_text='Enter Seconds')
        self.interval_entry.grid(column=4, row=2, pady=10, padx=10)
        amount_label = customtkinter.CTkLabel(self.periodic_frame, text="Number of Polls", anchor="w")
        amount_label.grid(row=3, column=3, pady=10, padx=10)
        self.amount_entry = customtkinter.CTkEntry(master=self.periodic_frame, width=200, placeholder_text='Enter Number')
        self.amount_entry.grid(column=4, row=3, pady=10, padx=10)



        self.periodic2_frame = customtkinter.CTkFrame(master=self)
        self.periodic2_frame.grid(row=1, rowspan=9, column=1, columnspan=10, padx=15, pady=15, sticky="nsew")
        columns = ("Overall Utilization", "Total Variation", "Average Errors", "Total Discards", "Timestamp")
        self.recurrent = ttk.Treeview(self.periodic2_frame, columns=columns, show="headings")
        self.recurrent.column(columns[0], width=150)
        self.recurrent.column(columns[1], width=150)
        self.recurrent.column(columns[2], width=150)
        self.recurrent.column(columns[3], width=150)
        self.recurrent.column(columns[4], width=150)
        for col in columns:
            self.recurrent.heading(col, text=col)
        data = {
            'Overall Utilization': [],
            'Total Variation': [],
            'Average Errors': [],
            'Total Discards': [],
            'Timestamp': []
        }

        for ou, av, ae, ad, ts in zip(data['Overall Utilization'], data['Total Variation'], data['Average Errors'], data['Total Discards'], data['Timestamp']):
            self.recurrent.insert("", tk.END, values=(ou, av, ae, ad, ts))
        style = ttk.Style()
        style.configure("Custom.Treeview", background="black", foreground="white", fieldbackground="black", rowheight=25)
        self.recurrent.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
        button2 = customtkinter.CTkButton(master=self.periodic2_frame, text="Save Data", command=self.save_data_to_db_button_click, width=120)
        button2.grid(column=1, columnspan=1, row=1, pady=0)
        button3 = customtkinter.CTkButton(master=self.periodic2_frame, text="View Database", command=self.save_fetch_to_db_button_click, width=120)
        button3.grid(column=1, columnspan=1, row=1, pady=(120, 50))

    def ml_page(self, table_no):
        try:
            self.fetch_frame.grid_forget()
            self.fetch_frame2.grid_forget()
            self.periodic_frame.grid_forget()
            self.periodic2_frame.grid_forget()
            self.prediction_frame.grid_forget()
            self.prediction_frame2.grid_forget()
        except:
            pass 
        self.ml_frame = customtkinter.CTkFrame(self)
        self.ml_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew", columnspan=3)
        self.db_fetch = customtkinter.CTkEntry(master=self.ml_frame, placeholder_text="Enter Batch ID", width=300)
        self.db_fetch.grid(row=1, columnspan=2, column=0, pady=10, padx=(0, 0))
        self.button = customtkinter.CTkButton(master=self.ml_frame, text="Retrieve Batch", command=self.button_click3, width=140)
        self.button.grid(column=(0), columnspan=1, row=2, padx=(10, 10), pady=5)
        self.option_menu_ml = customtkinter.CTkOptionMenu(master=self.ml_frame, values=["Linear Regression", "Random Forest", "SVM"])
        self.option_menu_ml.grid(column=(1), columnspan=1, row=2, padx=(10, 10), pady=5)
        self.ml_button = customtkinter.CTkButton(master=self.ml_frame, text="Start", command=self.start_button_press, width=140)
        self.ml_button.grid(column=(1), columnspan=1, row=3, padx=(10, 10), pady=5)
        self.save_model_button = customtkinter.CTkButton(master=self.ml_frame, text="Save Model", command=self.save_model_press, width=140)
        self.save_model_button.grid(column=(10), columnspan=1, row=3, padx=(10, 10), pady=5)
        self.display_switches()


        self.ml_frame2 = customtkinter.CTkFrame(master=self)
        self.ml_frame2.grid(row=1, rowspan=9, column=1, columnspan=3, padx=15, pady=(0,15), sticky="nsew")
        columns = ["Batch ID", "Utilization", "Var", "In Var", "Out Var", "Error", "In Err", "Out Err", "Disc", "In Disc", "Out Disc"]
        self.tree = ttk.Treeview(self.ml_frame2, columns=columns)
        self.tree.grid(row=1, column=0, padx=15, pady=(15,0), sticky="nsew")
        widths = [60, 80, 60, 60, 60, 60, 60, 60, 60, 60, 60]
        
        data = self.db.fetch_periodic_data(self.username)
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
       
        for x in data:
            self.tree.insert("", "end", values=x)


    def predictions_page(self):
        self.models = self.db.fetch_models(self.username)
        try:
            self.fetch_frame.grid_forget()
            self.fetch_frame2.grid_forget()
            self.periodic_frame.grid_forget()
            self.periodic2_frame.grid_forget()
            self.ml_frame.grid_forget()
            self.ml_frame2.grid_forget()
        except:
            pass

        self.prediction_frame = customtkinter.CTkFrame(self)
        self.prediction_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew", columnspan=10)
        self.enter_date_label = customtkinter.CTkLabel(self.prediction_frame, text="Minute")
        self.enter_date_label.grid(row=1, column=3, columnspan=1, padx=(10, 10), pady=(15,0))  
        self.enter_date_label = customtkinter.CTkLabel(self.prediction_frame, text="Hour")
        self.enter_date_label.grid(row=1, column=4, columnspan=1, padx=(10, 10), pady=(15,0))  
        self.enter_date_label = customtkinter.CTkLabel(self.prediction_frame, text="Day")
        self.enter_date_label.grid(row=1, column=5, columnspan=1, padx=(10, 10), pady=(15,0))
        self.enter_date_label = customtkinter.CTkLabel(self.prediction_frame, text="Month")
        self.enter_date_label.grid(row=1, column=6, columnspan=1, padx=(10, 10), pady=(15,0))
        self.enter_date_label = customtkinter.CTkLabel(self.prediction_frame, text="Year")
        self.enter_date_label.grid(row=1, column=7, columnspan=1, padx=(10, 10), pady=(15,0)) 
        self.enter_date_label = customtkinter.CTkLabel(self.prediction_frame, text="Enter Prediction Date:", anchor="w", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.enter_date_label.grid(row=2, column=2, columnspan=1, padx=(10, 10))     
        self.year_option = customtkinter.CTkOptionMenu(self.prediction_frame, values=['2024', '2025', '2026'], width=100)   
        self.year_option.grid(row=2, column=7, columnspan=1, padx=(10, 10))
        self.month_option = customtkinter.CTkOptionMenu(self.prediction_frame, values=['1', '2', '3', '4', '5', '6','7', '8', '9', '10', '11','12'], width=100)   
        self.month_option.grid(row=2, column=6, columnspan=1, padx=(10, 10))
        self.day_entry = customtkinter.CTkEntry(self.prediction_frame, placeholder_text='1-31', width=100)
        self.day_entry.grid(row=2, column=5, columnspan=1, padx=(10,10))
        self.hour_option = customtkinter.CTkOptionMenu(self.prediction_frame, values=['0', '1', '2', '3', '4', '5', '6','7', '8', '9', '10', '11','12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'], width=100)   
        self.hour_option.grid(row=2, column=4, columnspan=1, padx=(10, 10))
        self.minute_entry = customtkinter.CTkEntry(self.prediction_frame, placeholder_text='0-59', width=100)
        self.minute_entry.grid(row=2, column=3, columnspan=1, padx=(10,10))
        self.enter_date_label = customtkinter.CTkLabel(self.prediction_frame, text="Enter Variables:", anchor="w", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.enter_date_label.grid(row=4, column=2, columnspan=1, padx=(10, 10), pady=(15,0))  
        self.enter_date_label = customtkinter.CTkLabel(self.prediction_frame, text="Interface Speed", anchor="w")
        self.enter_date_label.grid(row=3, column=3, columnspan=1, padx=(10, 10), pady=(15,0))  
        self.enter_date_label = customtkinter.CTkLabel(self.prediction_frame, text="Maximum Transmission Unit")
        self.enter_date_label.grid(row=3, column=4, columnspan=1, padx=(10, 10), pady=(15,0))
        self.enter_date_label = customtkinter.CTkLabel(self.prediction_frame, text="Operational Status")
        self.enter_date_label.grid(row=3, column=5, columnspan=1, padx=(10, 10), pady=(15,0))
        self.enter_date_label = customtkinter.CTkLabel(self.prediction_frame, text="Admin Status")
        self.enter_date_label.grid(row=3, column=6, columnspan=1, padx=(10, 10), pady=(15,0)) 
        self.oper_option = customtkinter.CTkOptionMenu(self.prediction_frame, values=['Up (1)', 'Down (2)', 'Testing (3)', 'Unknown (4)', 'Dormant (5)', 'Not Present (6)','Lower Layer Down (7)'], width=100)   
        self.oper_option.grid(row=4, column=5, columnspan=1, padx=(10, 10))
        self.admin_option = customtkinter.CTkOptionMenu(self.prediction_frame, values=['Up (1)', 'Down (2)', 'Testing (3)', 'Unknown (4)'], width=100)
        self.admin_option.grid(row=4, column=6, columnspan=1, padx=(10, 10))
        self.mtu_entry = customtkinter.CTkEntry(self.prediction_frame, placeholder_text='Bytes', width=100)
        self.mtu_entry.grid(row=4, column=4, columnspan=1, padx=(10, 10))
        self.ifspeed_entry = customtkinter.CTkEntry(self.prediction_frame, placeholder_text='Bits', width=100)
        self.ifspeed_entry.grid(row=4, column=3, columnspan=1, padx=(10, 10))


        self.prediction_frame2 = customtkinter.CTkFrame(self)
        self.prediction_frame2.grid(row=1, rowspan=9, column=1, columnspan=10, padx=15, pady=(0, 15), sticky="nsew")
        self.model_id_entry = customtkinter.CTkEntry(self.prediction_frame2, placeholder_text="Enter Model ID")
        self.model_id_entry.grid(row=1, column=2, padx=15, pady=(15, 100))
        self.load_model_but = customtkinter.CTkButton(self.prediction_frame2, text="Load Model", command=self.load_model_press)
        self.load_model_but.grid(row=1, column=2, padx=15, pady=(15, 0))
        self.load_model_but = customtkinter.CTkButton(self.prediction_frame2, text="Make Predictions", command=self.make_predictions_press)
        self.load_model_but.grid(row=1, column=2, padx=15, pady=(100, 15))
        columns = ["Model ID", "Model Type"]
        self.tree2 = ttk.Treeview(self.prediction_frame2, columns=columns)
        self.tree2.grid(row=1, column=0, padx=15, pady=(15,0), sticky="nsew")
        widths = [200, 200]
        
        for col, width in zip(columns, widths):
            self.tree2.heading(col, text=col)
            self.tree2.column(col, width=width)
       
        for model in self.models:
            self.tree2.insert("", "end", values=model)


    def load_model_press(self):
        model_id = self.model_id_entry.get()
        serialized_model = self.db.fetch_model(model_id)
        self.model = pickle.loads(serialized_model)
        self.target_variables = self.db.fetch_list_data(model_id)
        print(self.target_variables)
    
        
    def make_predictions_press(self):
        year = self.year_option.get()
        month = self.month_option.get()
        day = self.day_entry.get()
        hour = self.hour_option.get()
        minute = self.minute_entry.get()
        second = 0
        
        admin = self.admin_option.get()
        if admin == "Up (1)":
            admin = 1
        elif admin == "Down (2)":
            admin = 2
        elif admin == "Testing (3)":
            admin = 3
        else:
            admin = 4
        
        op = self.oper_option.get()
        if op == "Up (1)":
            op = 1
        elif op == "Down (2)":
            op = 2
        elif op == "Testing (3)":
            op = 3
        elif op == "Unknown (4)":
            op = 4
        elif op == "Dormant (5)":
            op = 5
        elif op == "Not Present (6)":
            op = 6
        else:
            op = 7

        mtu = self.mtu_entry.get()
        ifspeed = self.ifspeed_entry.get()
        year, month, day, hour, minute, second, admin, op, mtu, ifspeed = map(int, (year, month, day, hour, minute, second, admin, op, mtu, ifspeed))
        data = np.array([[ifspeed, mtu, op, admin, year, month, day, hour, minute, second]])
        predictions = self.model.predict(data)
        predictions = predictions.flatten()
        
        target_variables_list = ast.literal_eval(self.target_variables)

        results = list(zip(target_variables_list, predictions))
        print(results)
        for variable_name, prediction in results:
            print(f"Predicted value for '{variable_name}': {prediction}")

        self.tree2.grid_forget()

        columns = ["Target Variable", "Prediction"]
        new_tree = ttk.Treeview(self.prediction_frame2, columns=columns)

        new_tree.grid(row=1, column=0, padx=15, pady=(15,0), sticky="nsew")

        widths = [200, 200]
        for col, width in zip(columns, widths):
            new_tree.heading(col, text=col)
            new_tree.column(col, width=width)

        for variable_name, prediction in results:
            new_tree.insert("", "end", values=(variable_name, prediction))







    def var_switch_press(self):
        var_switch_val = self.var_switch.get()
        self.var_switch.configure(text=var_switch_val)

    def error_switch_press(self):
        error_switch_val = self.error_switch.get()
        self.error_switch.configure(text=error_switch_val)

    def discard_switch_press(self):
        discard_switch_val = self.discard_switch.get()
        self.discard_switch.configure(text=discard_switch_val)

    def standardization_switch_press(self):
        standardization_val = self.standardization_switch.get()
        self.standardization_switch.configure(text=standardization_val)

    def normalization_switch_press(self):
        normalization_val = self.normalization_switch.get()
        self.normalization_switch.configure(text=normalization_val)
         
    def display_switches(self):
        self.var_err_disc_title_label = customtkinter.CTkLabel(master=self.ml_frame, text='Columns to Include', fg_color='transparent', anchor='w')
        self.var_err_disc_title_label.grid(column=8, columnspan=2, row=1, padx=(10, 10))
        self.roll_stand_norm_title_label = customtkinter.CTkLabel(master=self.ml_frame, text='Preprocessing Techniques', fg_color='transparent', anchor='w')
        self.roll_stand_norm_title_label.grid(column=3, columnspan=2, row=1, padx=(10, 10))
        self.var_switch = customtkinter.CTkSwitch(master=self.ml_frame, text='Total', command=self.var_switch_press, onvalue='In/Out', offvalue='Total')
        self.var_switch.grid(column=(9), row=2, padx=(10, 10), pady=5)
        self.var_label = customtkinter.CTkLabel(master=self.ml_frame, text="Packet Variation", fg_color="transparent", anchor="w")
        self.var_label.grid(column=(8), row=2)  
        self.error_switch = customtkinter.CTkSwitch(master=self.ml_frame, text='Average', command=self.error_switch_press, onvalue='In/Out', offvalue='Average')
        self.error_switch.grid(column=(9), row=3, padx=(10, 10), pady=5)
        self.error_label = customtkinter.CTkLabel(master=self.ml_frame, text="Error Percent", fg_color="transparent", anchor="w")
        self.error_label.grid(column=(8), row=3)
        self.discard_switch = customtkinter.CTkSwitch(master=self.ml_frame, text='Total', command=self.discard_switch_press, onvalue='In/Out', offvalue='Total')
        self.discard_switch.grid(column=(9), row=4, padx=(10, 10), pady=5)
        self.discard_label = customtkinter.CTkLabel(master=self.ml_frame, text="Discards", fg_color="transparent", anchor="w")
        self.discard_label.grid(column=(8), row=4)
        self.standardization_switch = customtkinter.CTkSwitch(master=self.ml_frame, text='Off', command=self.standardization_switch_press, onvalue='On', offvalue='Off')
        self.standardization_switch.grid(column=(4), row=3, padx=(10, 10), pady=5)
        self.standardization_switch_label = customtkinter.CTkLabel(master=self.ml_frame, text='Standardization', fg_color='transparent', anchor='w')
        self.standardization_switch_label.grid(column=(3), row=3)
        self.normalization_switch = customtkinter.CTkSwitch(master=self.ml_frame, text='Off', command=self.normalization_switch_press, onvalue='On', offvalue='Off')
        self.normalization_switch.grid(column=(4), row=2, padx=(10, 10), pady=5)
        self.normalization_switch_label = customtkinter.CTkLabel(master=self.ml_frame, text='Normalization', fg_color='transparent', anchor='w')
        self.normalization_switch_label.grid(column=(3), row=2)


    
    def start_button_press(self):
        self.var = self.var_switch.get()
        self.err = self.error_switch.get()
        self.disc = self.discard_switch.get()
        self.std = self.standardization_switch.get()
        self.norm = self.normalization_switch.get()
        self.ml_choice = self.option_menu_ml.get()
        self.df = replace_na_values(self.df)
        self.df = self.df.drop(columns=['batch_id'])
        self.df = self.df.drop(index=self.df.index[0])
        print(self.df)

        if self.norm == "On":
            self.df = normalize_dataframe(self.df)
        else:
            pass
        
        if self.std == 'On':
            self.df = standardize_dataframe(self.df)
        else:  
            pass
       
        if self.var == "Total":
            self.df = self.df.drop(columns=["Input Packet Variation"])
            self.df = self.df.drop(columns=["Output Packet Variation"])
        else:
            self.df = self.df.drop(columns=["Total Packet Variation"])
        
        if self.err == "Average":
            self.df = self.df.drop(columns=["Input Error Percentage"])
            self.df = self.df.drop(columns=["Output Error Percentage"])
        else:
            self.df = self.df.drop(columns=["Average Error Percentage"])
        
        if self.disc == "Total":
            self.df = self.df.drop(columns=["Input Discards"])
            self.df = self.df.drop(columns=["Output Discards"])
        else:
            self.df = self.df.drop(columns=["Total Discards"])
        
        self.model, self.rmse, self.mae = self.ml.start_ml(self.ml_choice, self.df)


    def save_model_press(self):
        model = self.ml.get_model()
        model_type = self.option_menu_ml.get()
        username = self.username
        target_var_list = self.ml.get_target_var()
        self.db.save_model(model_type, model, username, target_var_list)



    def update_res(self, res):
            mib_desc = res['mib_desc']
            obj_value = res['obj_value']
            time_stamp = res['time_stamp']
            self.recurrent.insert("", tk.END, value=(mib_desc, obj_value, time_stamp))
         
    
    def update_data(self, new_data, ts):
         for x in self.recurrent.get_children():
              self.recurrent.delete(x)
         for ou, av, ae, ad, ts in zip(new_data['Overall Utilization'], new_data['Total Packet Variation'], new_data['Average Error Percentage'], new_data['Total Discards'], ts):
              self.recurrent.insert("", tk.END, value=(ou, av, ae, ad, ts))

    def update_retrieval(self, df):
        for i in self.recurrent.get_children():
            self.recurrent.delete(i)
        try:
            df['timestamp'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']], errors='coerce')
        
        except Exception as e:
            print("Error occurred during datetime conversion:", e)
        
        for ou, opv, oiv, oov, oep, iep, oep, td, id, od, timestamp in zip(
            df["Overall Utilization"], 
            df["Total Packet Variation"], 
            df["Input Packet Variation"], 
            df['Output Packet Variation'], 
            df["Average Error Percentage"], 
            df["Input Error Percentage"], 
            df["Output Error Percentage"], 
            df["Total Discards"], 
            df["Input Discards"], 
            df["Output Discards"], 
            df["timestamp"]
        ):
            self.recurrent.insert("", tk.END, value=(ou, opv, oiv, oov, oep, iep, oep, td, id, od, timestamp))
         

    def update_norm_data(self, df):
        self.df = df
        table_no = 1
        self.ml_page(table_no)
       
        for i in self.recurrent.get_children():
            self.recurrent.delete(i)
        
        for ou, opv, oiv, oov, oep, iep, oep, td, id, od in zip(
            df["Overall Utilization"], 
            df["Total Packet Variation"], 
            df["Input Packet Variation"], 
            df['Output Packet Variation'], 
            df["Average Error Percentage"], 
            df["Input Error Percentage"], 
            df["Output Error Percentage"], 
            df["Total Discards"], 
            df["Input Discards"], 
            df["Output Discards"]):
            self.recurrent.insert("", tk.END, value=(ou, opv, oiv, oov, oep, iep, oep, td, id, od))

        return self.df
   
    def show_single_page(self):
        self.fetch_page()

    def show_periodic_page(self):
        self.periodic_page()
      
    def show_ml_page(self):
        table_no = 0
        self.ml_page(table_no)


    def button_click1(self):
        ip_value = self.ip_entry1.get()
        port_value = self.port_entry1.get()
        cstring_value = self.cstring_entry1.get()
        index_value = self.index_entry1.get()
        self.new_res = snmp_call(cstring_value, ip_value, port_value, self.mib_choice, self.object_choice, index_value,)
        print(self.new_res)
        self.update_res(self.new_res)
        self.df2 = create_dataframe2(self.new_res)
        return self.new_res, self.df2
    
    def button_click2(self):
        self.amount = self.amount_entry.get()
        self.interval = self.interval_entry.get()
        self.amount = int(self.amount)
        self.amount = self.amount + 1
        self.interval = int(self.interval)
        

        function_args = [
            ('public', '192.168.1.158', '161', "IF-MIB", "ifHCInOctets", '2', self.amount, self.interval),
            ('public', '192.168.1.158', '161', "IF-MIB", "ifHCOutOctets", '2',self.amount, self.interval),
            ('public', '192.168.1.158', '161', "IF-MIB", "ifInErrors", '2',self.amount, self.interval),
            ('public', '192.168.1.158', '161', "IF-MIB", "ifOutErrors", '2',self.amount, self.interval),
            ('public', '192.168.1.158', '161', "IF-MIB", "ifHCInUcastPkts", '2',self.amount, self.interval),
            ('public', '192.168.1.158', '161', "IF-MIB", "ifHCOutUcastPkts", '2',self.amount, self.interval),
            ('public', '192.168.1.158', '161', "IF-MIB", "ifSpeed", '2',self.amount, self.interval),
            ('public', '192.168.1.158', '161', "IF-MIB", "ifInDiscards", '2',self.amount, self.interval),
            ('public', '192.168.1.158', '161', "IF-MIB", "ifOutDiscards", '2',self.amount, self.interval),
            ('public', '192.168.1.158', '161', 'IF-MIB', 'ifMtu', '2',self.amount, self.interval),
            ('public', '192.168.1.158', '161', 'IF-MIB', 'ifAdminStatus', '2',self.amount, self.interval),
            ('public', '192.168.1.158', '161', 'IF-MIB', 'ifOperStatus', '2',self.amount, self.interval),
            ]
        function_args2 = (self.amount, self.interval)
        
        with multiprocessing.Pool(processes=18) as pool: 

            self.snmp_result = pool.starmap_async(snmp_function, function_args)
            self.time_result = pool.apply_async(time_stamps, function_args2)
            self.snmp_response = self.snmp_result.get() 
            self.time_response = self.time_result.get()
            self.time_stamp = self.time_response[6]
            self.ifHCInOctets, self.ifHCOutOctets, self.ifInErrors, self.ifOutErrors, self.ifHCInUcastPkts, self.ifHCOutUcastPkts, self.ifSpeed, self.ipInDiscards, self.ipOutDiscards, ifMtu, ifOperStatus, ifAdminStatus, self.year, self.month, self.day, self.hour, self.minute, self.second = clean_data(self.snmp_response, self.time_response)
            ifOperStatus = convert_oper_status(ifOperStatus)
            ifAdminStatus = convert_admin_status(ifAdminStatus)
            print(ifOperStatus)
            print(ifAdminStatus)
            self.total_discards, self.in_discard_variation, self.out_discard_variation = calculate_total_discards(self.ipInDiscards, self.ipOutDiscards) 
            self.packet_variation, self.in_packet_variation, self.out_packet_variation = calculate_packet_variation(self.ifHCInUcastPkts, self.ifHCOutUcastPkts)
            self.overall_error_percentage, self.input_error_percentage, self.output_error_percentage = calculate_error_percentages(self.ifOutErrors, self.ifHCOutUcastPkts, self.ifInErrors, self.ifHCInUcastPkts)
            self.overall_utilization = calculate_utilization(self.ifHCInOctets, self.ifSpeed, self.ifHCOutOctets, self.interval)
            self.df = create_dataframe(self.year, self.month,self.day, self.hour, self.minute, self.second, self.total_discards, self.packet_variation, self.input_error_percentage, self.output_error_percentage, self.overall_error_percentage, self.in_packet_variation, self.out_packet_variation, self.in_discard_variation, self.out_discard_variation, self.overall_utilization, self.ifSpeed, ifMtu, ifOperStatus, ifAdminStatus)         
            self.update_data(self.df, self.time_stamp)
        return self.df
    
    def button_click3(self):
        batch_id = self.db_fetch.get()
        self.ml_frame2 = customtkinter.CTkFrame(master=self)
        self.ml_frame2.grid(row=1, rowspan=9, column=1, columnspan=3, padx=15, pady=(0,15), sticky="nsew")

        columns = ("Overall Util ", "Total Pack Var", "In Pack Var", "Out Pack Var", "Avg Err Per", "In Err Per", "Out Err Per", "Total Disc", "In Disc", "Out Disc")
        self.recurrent = ttk.Treeview(self.ml_frame2, columns=columns, show="headings")
        self.recurrent.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
        self.recurrent.column(columns[0], width=95)
        self.recurrent.column(columns[1], width=95)
        self.recurrent.column(columns[2], width=95)
        self.recurrent.column(columns[3], width=95)
        self.recurrent.column(columns[4], width=95)
        self.recurrent.column(columns[5], width=95)
        self.recurrent.column(columns[6], width=95)
        self.recurrent.column(columns[7], width=90)
        self.recurrent.column(columns[8], width=80)
        self.recurrent.column(columns[9], width=80)
        for col in columns:
            self.recurrent.heading(col, text=col)

        self.retrieve_fetch_from_db(batch_id)


    def save_data_to_db_button_click(self):
        self.db.insert_to_snmp_data_table(self.df, self.username)
         
    def save_fetch_to_db_button_click(self):
        self.db.insert_to_snmp_fetch_table(self.df2)

    def retrieve_fetch_from_db(self, batch_id):
        batch_id = [batch_id]
        self.df = self.db.retrive_data_from_db(batch_id)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        print(self.df)
        self.update_retrieval(self.df)
        return self.df
    
              
if __name__ == "__main__":
    app = App()
    app.mainloop()



