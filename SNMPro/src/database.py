import mysql.connector
import random
import string
import pandas as pd
import pickle
import json


class DB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="database-1.clzinzr5ga32.eu-west-2.rds.amazonaws.com",
            user="root",
            password="root12345",
            database="snmp_data_db"
        )
        
        self.cursor = self.conn.cursor()


    def insert_signup_data(self, data):
        self.data = data
        print(data)
        for _, row in self.data.iterrows():
            insert_query = """
            INSERT INTO snmp_data_db.signup
            (username, password, firstname, lastname)
            VALUES (%s, %s, %s, %s)
            """
            values = (
                row['username'],
                row['password'],
                row['firstname'],
                row['lastname']
            )
            self.cursor.execute(insert_query, values)
        self.conn.commit()

    
    def check_user_exists(self, username, password):
        query = "SELECT * FROM snmp_data_db.signup WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        rows = self.cursor.fetchall()

        if rows: 
            data = []
            for row in rows:
                username_data = {
                    'username': row[0],
                    'password': row[1],
                    'firstname': row[2],
                    'lastname': row[3]
                }
                data.append(username_data)
            self.user_data = pd.DataFrame(data)
            return True
        else:
            print("User not found")
            return False
    

    
    def generate_batch_id(self, length=4):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length ))

    
    def insert_to_snmp_data_table(self, df, username):
        self.df = df
        print(self.df)
        batch_id = self.generate_batch_id()
        for _, row in self.df.iterrows():
            insert_query = """
            INSERT INTO snmp_data_db.snmp_data 
            (batch_id, Overall_Utilization, Overall_Packet_Variation, Input_Packet_Variation, Output_Packet_Variation, Overall_Error_Percentage, Input_Error_Percentage, Output_Error_Percentage, Total_Discards, Input_Discards, Output_Discards, Interface_Speed, Maximum_Transmission_Unit, Operational_Status, Admin_Status, Year, Month, Day, Hour, Minute, Second, username) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                batch_id,
                row['Overall Utilization'],
                row['Total Packet Variation'],
                row['Input Packet Variation'],
                row['Output Packet Variation'],
                row['Average Error Percentage'],
                row['Input Error Percentage'],
                row['Output Error Percentage'],
                row['Total Discards'],
                row['Input Discards'],
                row['Output Discards'],
                row['Interface Speed'], 
                row['Maximum Transmission Unit'], 
                row['Operational Status'], 
                row['Admin Status'], 
                row['Year'],
                row['Month'],
                row['Day'],
                row['Hour'],
                row['Minute'],
                row['Second'],
                username,
            )
            self.cursor.execute(insert_query, values)
        self.conn.commit()

    def insert_to_snmp_fetch_table(self, df):
        self.df = df
        batch_id = self.generate_batch_id()
        for _, row in self.df.iterrows():
            insert_query = """
            INSERT INTO snmp_data_db.snmp_fetch
            (batch_id, mib_desc, obj_value)
            VALUES (%s, %s, %s)
            """
            values = (
                batch_id,
                row['mib_desc'],
                row['obj_value'],
            )
            self.cursor.execute(insert_query, values)
        self.conn.commit()

    def retrive_data_from_db(self, batch_id):
        self.data_df = pd.DataFrame(columns=["Batch ID", "Overall Utilization", "Total Packet Variation", "Input Packet Variation", "Output Packet Variation", "Average Error Percentage", "Input Error Percentage", "Output Error Percentage", "Total Discards", "Input Discards", "Output Discards", 'Interface_Speed', 'Maximum_Transmission_Unit', 'Operational_Status', 'Admin_Status', "Year", "Month", "Day", "Hour", "Minute", "Second"])
        query = "SELECT * FROM snmp_data WHERE batch_id = %s"
        self.cursor.execute(query, (batch_id))
        rows = self.cursor.fetchall()
        data = [{"batch_id": row[0],
                 "Overall Utilization": row[1], 
                 "Total Packet Variation": row[2], 
                 "Input Packet Variation": row[3], 
                 "Output Packet Variation": row[4], 
                 "Average Error Percentage": row[5], 
                 "Input Error Percentage": row[6], 
                 "Output Error Percentage": row[7], 
                 "Total Discards": row[8], 
                 "Input Discards": row[9], 
                 "Output Discards": row[10],
                 'Interface Speed': row[11],
                 'Maximum Transmission Unit': row[12],
                 'Operational Status': row[13],
                 'Admin Status': row[14], 
                 "Year": row[15], 
                 "Month": row[16], 
                 "Day": row[17], 
                 "Hour": row[18], 
                 "Minute": row[19], 
                 "Second": row[20]} for row in rows]
        
        self.data_df = pd.DataFrame(data)  
        print(self.data_df)
        return self.data_df      



    def save_model(self, model_type, model, username, new_list):
      
        serialized_model = pickle.dumps(model)
        model_id = self.generate_batch_id()
        serialized_list_json = json.dumps(new_list)
        insert_query = """
        INSERT INTO snmp_data_db.models
        (model_id, model_type, serialized_model, username, list_data)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (model_id, model_type, serialized_model, username, serialized_list_json)
        self.cursor.execute(insert_query, values)
        self.conn.commit()


    def close_connections(self):
        self.conn.close()

    def fetch_models(self, username):
        query = "SELECT * FROM snmp_data_db.models WHERE username = %s"
        self.cursor.execute(query, (username,))
        model = self.cursor.fetchall()

        return model

    def fetch_model(self, model_id):
        query = "SELECT serialized_model FROM models WHERE model_id = %s"
        self.cursor.execute(query, (model_id,))
        serialized_model = self.cursor.fetchone()[0] 
        
        return serialized_model


    def fetch_list_data(self, model_id):
        query = "SELECT list_data FROM models WHERE model_id = %s"
        self.cursor.execute(query, (model_id,))
        list_data = self.cursor.fetchone()[0] 
        
        return list_data


    def delete_model(self, model_id):
        """
        Delete a model from the database based on its ID.
        """
        delete_query = """
        DELETE FROM snmp_data_db.models
        WHERE model_id = %s
        """
        values = (model_id,)
        self.cursor.execute(delete_query, values)
        self.conn.commit()


    def fetch_periodic_data(self, username):
        query = "SELECT * FROM snmp_data_db.snmp_data WHERE username = %s"
        self.cursor.execute(query, (username,))
        data = self.cursor.fetchall()

        return data