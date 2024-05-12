import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def clean_data(snmp_response, time_response):
    
    ifHCInOctets, ifHCOutOctets, ifInErrors, ifOutErrors, ifHCInUcastPkts, ifHCOutUcastPkts, ifSpeed, ipInDiscards, ipOutDiscards, ifMtu, ifAdminStatus, ifOperStatus  = snmp_response
    
    year, month, day, hour, minute, second, time_stamp = time_response
    time_response = time_response[-6]
    
    ifHCInOctets = [(item.split(" = ")[0], item.split(" = ")[1]) for item in ifHCInOctets] 
    ifHCOutOctets = [(item.split(" = ")[0], item.split(" = ")[1]) for item in ifHCOutOctets]
    ifInErrors = [(item.split(" = ")[0], item.split(" = ")[1]) for item in ifInErrors]
    ifOutErrors = [(item.split(" = ")[0], item.split(" = ")[1]) for item in ifOutErrors]
    ifHCInUcastPkts = [(item.split(" = ")[0], item.split(" = ")[1]) for item in ifHCInUcastPkts]
    ifHCOutUcastPkts = [(item.split(" = ")[0], item.split(" = ")[1]) for item in ifHCOutUcastPkts]
    ifSpeed = [(item.split(" = ")[0], item.split(" = ")[1]) for item in ifSpeed]
    ipInDiscards = [(item.split(" = ")[0], item.split(" = ")[1]) for item in ipInDiscards]
    ipOutDiscards = [(item.split(" = ")[0], item.split(" = ")[1]) for item in ipOutDiscards]
    ifMtu = [(item.split(" = ")[0], item.split(" = ")[1]) for item in ifMtu]
    ifAdminStatus = [(item.split(" = ")[0], item.split(" = ")[1]) for item in ifAdminStatus]
    ifOperStatus = [(item.split(" = ")[0], item.split(" = ")[1]) for item in ifOperStatus]

    ifHCInOctets = [item[1] for item in ifHCInOctets]
    ifHCOutOctets = [item[1] for item in ifHCOutOctets]
    ifInErrors = [item[1] for item in ifInErrors] 
    ifOutErrors = [item[1] for item in ifOutErrors]
    ifHCInUcastPkts = [item[1] for item in ifHCInUcastPkts]
    ifHCOutUcastPkts = [item[1] for item in ifHCOutUcastPkts]  
    ifSpeed = [item[1] for item in ifSpeed]
    ipInDiscards = [item[1] for item in ipInDiscards]
    ipOutDiscards = [item[1] for item in ipOutDiscards]
    ifMtu = [item[1] for item in ifMtu]
    ifAdminStatus = [item[1] for item in ifAdminStatus]
    ifOperStatus = [item[1] for item in ifOperStatus]
    ifHCInOctets = list(map(int, ifHCInOctets))
    ifHCOutOctets = list(map(int, ifHCOutOctets))
    ifInErrors = list(map(int, ifInErrors))
    ifOutErrors = list(map(int, ifOutErrors))
    ifHCInUcastPkts = list(map(int, ifHCInUcastPkts))
    ifHCOutUcastPkts = list(map(int, ifHCOutUcastPkts))
    ifSpeed = list(map(int, ifSpeed))
    ipInDiscards = list(map(int, ipInDiscards))
    ipOutDiscards = list(map(int, ipOutDiscards))
    ifMtu = list(map(int, ifMtu))
    ifAdminStatus = list(map(str, ifAdminStatus))
    ifOperStatus = list(map(str, ifOperStatus))
    


    return ifHCInOctets, ifHCOutOctets, ifInErrors, ifOutErrors, ifHCInUcastPkts, ifHCOutUcastPkts, ifSpeed, ipInDiscards, ipOutDiscards, ifMtu, ifOperStatus, ifAdminStatus, year, month, day, hour, minute, second
    
def calculate_utilization(ifHCInOctets, ifSpeed, ifHCOutOctets, poll_interval):
    #Input Utilization = (ifInOctet2 - ifInOctet1) * 8 / delta_time) / ifSpeed * 100
    in_util = []
    out_util = []
    print("ifHCInOctets: " + str(ifHCInOctets))
    print("ifSpeed: " + str(ifSpeed))
    print("ifHCOutOctets: " + str(ifHCOutOctets))
    for i in range(len(ifHCInOctets)):
        if i > 0:
            in_util.append(ifHCInOctets[i] - ifHCInOctets[i-1])
        else:
            in_util.append('N/A')

    input_utilization = []
    for i in in_util:
        if i != "N/A":
            input_utilization.append((i*8/poll_interval)/ifSpeed[0]*100)
        else:
            input_utilization.append('N/A')
   
    #Output Utilization = ((OutHCOctet2 - OutHCOctet1) * 8 / delta_time) / ifSpeed * 100
    out_util = []
    for i in range(len(ifHCOutOctets)):
        if i > 0:
           out_util.append(ifHCOutOctets[i] - ifHCOutOctets[i-1])
        else:
           out_util.append('N/A')

    output_utilization = []
    for i in out_util:
        if i != "N/A":
            output_utilization.append((i*8/poll_interval)/ifSpeed[0]*100)
        else:
            output_utilization.append('N/A')
    
    overall_utilization = [a + b for a, b in zip(input_utilization, output_utilization)]
    return overall_utilization
    
def calculate_error_percentages(ifOutErrors, ifHCOutUcastPkts, ifInErrors, ifHCInUcastPkts): 
    #Output Error Percentage = (ifOutErrors / ifHCOutUcastPkts) * 100
    change_in_out_errors = []
    for i in range(len(ifOutErrors)):
        if i > 0:
            change_in_out_errors.append(ifOutErrors[i] - ifOutErrors[i-1])
        else:
            change_in_out_errors.append(0)

    change_in_out_Ucast_Pkts = []
    for i in range(len(ifHCOutUcastPkts)):
        if i > 0:
            change_in_out_Ucast_Pkts.append(ifHCOutUcastPkts[i] - ifHCOutUcastPkts[i-1])
        else:
            change_in_out_Ucast_Pkts.append(0)

    output_error_percentage = []
    for x, y in zip(change_in_out_errors, change_in_out_Ucast_Pkts):
        if y > 0:
            output_error_percentage.append((x / y)*100)
        else:
            output_error_percentage.append(0)
    
    #Input Error Percentage = (ifInErrors / ifHCInUcastPkts) * 100
    change_in_input_errors = []
    for i in range(len(ifInErrors)):
        if i > 0:
            change_in_input_errors.append(ifInErrors[i] - ifInErrors[i-1])
        else:
            change_in_input_errors.append(0)

    change_in_input_Ucast_Pkts = []
    for i in range(len(ifHCInUcastPkts)):
        if i > 0:
            change_in_input_Ucast_Pkts.append(ifHCInUcastPkts[i] - ifHCInUcastPkts[i-1])
        else:
            change_in_input_Ucast_Pkts.append(0)
    
    input_error_percentage = []
    for x, y in zip(change_in_input_errors, change_in_input_Ucast_Pkts):
        if y > 0:
            input_error_percentage.append((x / y)*100)
        else:
            input_error_percentage.append(0)
    
    overall_error_percentage = [(x + y) / 2 for x, y in zip(input_error_percentage, output_error_percentage)]
    return overall_error_percentage, input_error_percentage, output_error_percentage
    

def calculate_packet_variation(ifHCInUcastPkts, ifHCOutUcastPkts): 
    in_packet_variation = []
    out_packet_variation = []
    for i in range(len(ifHCInUcastPkts)):
        diff_in = ifHCInUcastPkts[i] - ifHCInUcastPkts[i-1]
        print("diff:" + str(diff_in))
        diff_out = ifHCOutUcastPkts[i] - ifHCOutUcastPkts[i-1]
        in_packet_variation.append(diff_in)
        out_packet_variation.append(diff_out)
    packet_variation = [a + b for a, b in zip(in_packet_variation, out_packet_variation)]

    return packet_variation, in_packet_variation, out_packet_variation

def calculate_total_discards(ipInDiscards, ipOutDiscards):
    in_discard_variation = []
    out_discard_variation = []
    in_discard_variation.append(0)
    out_discard_variation.append(0)
    for i in range(1, len(ipOutDiscards)):
        in_discard_variation.append(ipInDiscards[i] - ipInDiscards[i-1])
        out_discard_variation.append(ipOutDiscards[i] - ipOutDiscards[i-1])
    total_discards = [a + b for a, b in zip(in_discard_variation, out_discard_variation)]
    
    return total_discards, in_discard_variation, out_discard_variation

def convert_oper_status(ifOperStatus):
    
    converted_ifOperStatus = []
    
    for i in ifOperStatus:
        if i == 'up':
            converted_ifOperStatus.append(1)
        elif i == 'down':
            converted_ifOperStatus.append(2)
        elif i == 'testing':
            converted_ifOperStatus.append(3)
        elif i == 'unknown':
            converted_ifOperStatus.append(4)
        elif i == 'dormant':
            converted_ifOperStatus.append(5)
        elif i == 'notPresent':
            converted_ifOperStatus.append(6)
        elif i == 'lowerLayerDown':
            converted_ifOperStatus.append(7)
        else:
            converted_ifOperStatus.append(3)
    
    return converted_ifOperStatus

def convert_admin_status(ifAdminStatus):
    
    conveted_ifAdminStatus = []
    
    for i in ifAdminStatus:
        if i == 'up':
            conveted_ifAdminStatus.append(1)
        elif i == 'down':
            conveted_ifAdminStatus.append(2)
        elif i == 'testing':
            conveted_ifAdminStatus.append(3)
        elif i == 'unknown':
            conveted_ifAdminStatus.append(4)
    
    return conveted_ifAdminStatus


def create_dataframe(year, month, day, hour, minute, second, total_discards, packet_variation, input_error_percentage, output_error_percentage, overall_error_percentage, in_packet_variation, out_packet_variation, in_discard_variation, out_discard_variation, overall_utilization, ifSpeed, ifMtu, ifOperStatus, ifAdminStatus,):
    
    data = {
        'Overall Utilization': overall_utilization,     
        'Total Packet Variation': packet_variation,
        'Input Packet Variation': in_packet_variation,
        'Output Packet Variation': out_packet_variation,
        'Average Error Percentage': overall_error_percentage,
        'Input Error Percentage': input_error_percentage,
        'Output Error Percentage': output_error_percentage,  
        'Total Discards': total_discards,
        'Input Discards': in_discard_variation,
        'Output Discards': out_discard_variation,
        'Year': year,
        'Month': month,
        'Day': day,
        'Hour': hour,
        'Minute': minute,
        'Second': second,
        'Interface Speed': ifSpeed,
        'Maximum Transmission Unit': ifMtu,
        'Operational Status': ifOperStatus,
        'Admin Status': ifAdminStatus
    }

    df = pd.DataFrame(data)
    df = df.drop(0)
    print(df)
    return df

def create_dataframe2(new_res):
    for key, value in new_res.items():
        if not isinstance(value, (list, tuple)):
            new_res[key] = [value]
        
        df2 = pd.DataFrame(new_res)
        return df2
    
import pandas as pd

def replace_na_values(df):
    df_filled = df.fillna(method='ffill')
    df_filled = df_filled.fillna(method='bfill')
    return df

def add_rolling_aggregates(df):
    df['timestamp'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']])
    df.set_index('timestamp', inplace=True)

    rolling_aggregates = df['Overall Utilization'].rolling(window='5s').agg(['mean', 'median', 'min', 'max', 'std', 'sum'])
    rolling_aggregates_filled = replace_na_values(rolling_aggregates)
    
    df = pd.merge(df, rolling_aggregates_filled, left_index=True, right_index=True, suffixes=('', '_Rolling'))
    df.reset_index(drop=True, inplace=True)
    return df


def normalize_dataframe(df):
    columns_to_exclude = ['batch_id', 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'timestamp']
    columns_to_normalize = [col for col in df.columns if col not in columns_to_exclude]
    
    scaler = MinMaxScaler()

    df[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])
    
    print(df)
    return df


def standardize_dataframe(df):
    
    columns_to_exclude = ['batch_id', 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'timestamp']
    columns_to_standardize = [col for col in df.columns if col not in columns_to_exclude]

    scaler = StandardScaler()

    df[columns_to_standardize] = scaler.fit_transform(df[columns_to_standardize])

    print('*************************************************************************')
    return df




def denormalize_dataframe(df, original_df):
    
    columns_to_exclude = ['batch_id', 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'timestamp']
    columns_to_denormalize = [col for col in df.columns if col not in columns_to_exclude]

    for col in columns_to_denormalize:
        min_val = original_df[col].min()
        max_val = original_df[col].max()
        df[col] = (df[col] * (max_val - min_val)) + min_val

    return df

def unstandardize_dataframe(df, original_df):
   
    columns_to_exclude = ['batch_id', 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'timestamp']
    columns_to_unstandardize = [col for col in df.columns if col not in columns_to_exclude]

    for col in columns_to_unstandardize:
        mean_val = original_df[col].mean()
        std_val = original_df[col].std()
        df[col] = (df[col] * std_val) + mean_val

    return df



