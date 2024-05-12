from pysnmp.hlapi import *
import time
from datetime import datetime
import pandas as pd

def snmp_function(cstring_value, ip_value, port_value, mib_choice, object_choice, index_value, amount, interval):
    response = []
    i = 0
    for i in range(amount):
        
        iterator = getCmd(SnmpEngine(),
            CommunityData(cstring_value),
            UdpTransportTarget((ip_value, port_value)), 
            ContextData(),
            ObjectType(ObjectIdentity(mib_choice, object_choice, index_value)))
                
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        if errorIndication:
            print(f"Error: {errorIndication}")
        elif errorStatus:
            print(f"Error: {errorStatus} at {errorIndex}")
        else:
            for varBind in varBinds:     
                response.append(varBind.prettyPrint())

        i =i+1
        time.sleep(interval)
    return response

def time_stamps(amount, interval):
    year, month, day, hour, minute, second, time_stamp = [], [], [], [], [], [], []
    i = 0
    for i in range(amount):
        timestamp = datetime.now()
        time_stamp.append(timestamp)
        year.append(timestamp.year)
        month.append(timestamp.month)
        day.append(timestamp.day)
        hour.append(timestamp.hour)
        minute.append(timestamp.minute)
        second.append(timestamp.second)
        i=i+1
        time.sleep(interval)
    
    return year, month, day, hour, minute, second, time_stamp

def snmp_call(cstring_value, ip_value, port_value, mib_choice, object_choice, index_value):
    iterator = getCmd(SnmpEngine(),
        CommunityData(cstring_value),
        UdpTransportTarget((ip_value, port_value)), 
        ContextData(),
        ObjectType(ObjectIdentity(mib_choice, object_choice, index_value)))

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    if errorIndication:
        print(f"Error: {errorIndication}")
    elif errorStatus:
        print(f"Error: {errorStatus} at {errorIndex}")
    else:
        for varBind in varBinds:
            time_stamp = datetime.now()
            varBind = str(varBind)
            split = varBind.split("=")
            split = [i.strip() for i in split]
            mib_desc = split[0]
            obj_value = split[1] 
            new_res = {
                'mib_desc': mib_desc,
                'obj_value': obj_value,
                'time_stamp': time_stamp
            }
    return new_res

