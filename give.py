import schedule
import requests
import time
from database import DBHelper
import struct


# endregion
SENSOR_DATA_INTERVAL = 5
SAMPLE_RATE = 1
HOST = ''

SEND_DATA = True

machine_obj = {}

ob_db = DBHelper("EM_data")

prev_sensor_data_sent = time.time()

ACCESS_TOKEN = ''

HEADERS = {'content-type': 'application/json'}

HOST_SENSOR = 'https://api.infinite-uptime.com/api/3.0/idap-api'
print(HOST_SENSOR)

ACCESS_TOKEN_SENSOR = ''
PASSWORD = "''"
USERNAME = "'='"

HEADERS_SENSOR = {'content-type': 'application/json',
                  'Authorization': f"Bearer {ACCESS_TOKEN_SENSOR}"}

sensors = {
    "STEAM_TEMP": {
        "tableName": "external_device_data_ald_steam_001_a_763"
    },
    "SPEED": {
        "tableName": "external_device_data_ald_speed_001_b_763"
    },
    "PAPER_GSM": {
        "tableName": "external_device_data_ald_gsm_001_c_763"
    },
    "STEAM_PRGP_1": {
        "tableName": "external_device_data_ald_gp1_001_d_763"
    },
    "STEAM_PRGP_2": {
        "tableName": "external_device_data_ald_gp2_001_e_763"
    },
    "STEAM_PRGP_3": {
        "tableName": "external_device_data_ald_gp3_001_f_763"
    },
    "STEAM_PRGP_4": {
        "tableName": "external_device_data_ald_gp4_001_g_763"
    },
    "STEAM_PRGP_5": {
        "tableName": "external_device_data_ald_gp5_001_h_763"
    },
    "STEAM_PRGP_6": {
        "tableName": "external_device_data_ald_gp6_001_i_763"
    },
    "STEAM_PRGP_7": {
        "tableName": "external_device_data_ald_gp7_001_j_763"
    },
    "STEAM_PRGP_8": {
        "tableName": "external_device_data_ald_gp8_001_k_763"
    },
    "STEAM_PRGP_9": {
        "tableName": "external_device_data_ald_gp9_001_l_763"
    }
}


def generate_sensor_config(sensor_name):
    config = {
        "filters": [
            {
                "fields": [],
                "nextCondition": "string",
                "fieldsCondition": "string"
            }
        ],
        "tableName": sensors[sensor_name]["tableName"],  # Access tableName dynamically
        "sortField": [{"field": "id", "dir": "desc"}],
        "groupBy": [],
        "functions": [],
        "page": 1,
        "pageSize": 200,
        "selectedFields": []
    }
    return config


STEAM_TEMP = generate_sensor_config("STEAM_TEMP")
SPEED = generate_sensor_config("SPEED")
PAPER_GSM = generate_sensor_config("PAPER_GSM")
STEAM_PRGP_1 = generate_sensor_config("STEAM_PRGP_1")
STEAM_PRGP_2 = generate_sensor_config("STEAM_PRGP_2")
STEAM_PRGP_3 = generate_sensor_config("STEAM_PRGP_3")
STEAM_PRGP_4 = generate_sensor_config("STEAM_PRGP_4")
STEAM_PRGP_5 = generate_sensor_config("STEAM_PRGP_5")
STEAM_PRGP_6 = generate_sensor_config("STEAM_PRGP_6")
STEAM_PRGP_7 = generate_sensor_config("STEAM_PRGP_7")
STEAM_PRGP_8 = generate_sensor_config("STEAM_PRGP_8")
STEAM_PRGP_9 = generate_sensor_config("STEAM_PRGP_9")


def convert_hex_to_ieee754(hex_str):
    try:
        # currently converting to big endian
        decimal_value_big_endian = struct.unpack('>f', bytes.fromhex(hex_str))[0]
    except Exception as e:
        print(f"Error while converting {hex_str} to float: {e}")
        decimal_value_big_endian = 0.0

    return round(decimal_value_big_endian, 5)


def post_sensors_data(payload):
    try:
        if payload:
            host_tb = f'{HOST}/api/v1/{ACCESS_TOKEN}/telemetry/'
            print(f"Sending {payload} to {host_tb}")
            try:
                req_post = requests.post(host_tb, json=payload, headers=HEADERS, timeout=2)
                print(req_post.status_code)
                print(req_post.text)
                req_post.raise_for_status()
            except Exception as e:
                print(f"[-] Error While sending data to server {e}")
        else:
            print("got empty payload")
    except Exception as e:
        print(f"Error while sending data {e}")


def get_steam_data():
    try:
        req = requests.post(f'{HOST_SENSOR}/advance-query?organizationId=763', json=STEAM_TEMP, headers=HEADERS_SENSOR,
                            timeout=2)
        print(req.status_code)

        raw_data = req.json()
        payload = {}
        id_list = []
        if raw_data is not None:
            max_id = max([m_data['id'] for m_data in raw_data])
            latest_data = {}
            for m_data in raw_data:
                if m_data['id'] == max_id:
                    latest_data = m_data
                    break
            if latest_data:
                payload = {
                    'INF_UPTM_PR_MAIN_TEMP_DEG_CELCIUS': convert_hex_to_ieee754(latest_data['process_parameter_001_a']),
                }
                post_sensors_data(payload)
        return payload
    except Exception as e:
        print(f"Error while sending the Steam data {e}")
        return []



schedule.every(SENSOR_DATA_INTERVAL).seconds.do(get_steam_data)

if __name__ == "__main__":
    try:
        access_token = ACCESS_TOKEN_SENSOR
        if access_token is None:
            print("[+] Error No Access Token is Found Refreshing...")

        HEADERS_SENSOR['Authorization'] = f'Bearer {ACCESS_TOKEN_SENSOR}'
        while True:
            schedule.run_pending()
            time.sleep(2)
    except Exception as e:
        print(f"Error Running Program {e}")
