import datetime
import schedule
import requests
import os
import sys
import time
import base64
import logging
import logging.handlers
from database import DBHelper
from logging.handlers import TimedRotatingFileHandler
import os
import struct

log_level = logging.INFO
from dotenv import load_dotenv

load_dotenv()

FORMAT = ('%(asctime)-15s %(levelname)-8s %(name)s %(module)-15s:%(lineno)-8s %(message)s')

logFormatter = logging.Formatter(FORMAT)
log = logging.getLogger("HIS_LOGS")

# checking and creating logs directory here

if getattr(sys, 'frozen', False):
    dirname = os.path.dirname(sys.executable)
else:
    dirname = os.path.dirname(os.path.abspath(__file__))

logdir = f"{dirname}/logs"
print(f"log directory name is {logdir}")
if not os.path.isdir(logdir):
    log.info("[-] logs directory doesn't exists")
    try:
        os.mkdir(logdir)
        log.info("[+] Created logs dir successfully")
    except Exception as e:
        log.error(f"[-] Can't create dir logs Error: {e}")

fileHandler = TimedRotatingFileHandler(f'{logdir}/app_log',
                                       when='midnight', interval=1)
fileHandler.setFormatter(logFormatter)
fileHandler.suffix = "%Y-%m-%d.log"
log.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)

log.setLevel(log_level)

# endregion
SENSOR_DATA_INTERVAL = 5
SAMPLE_RATE = 1
HOST = 'https://ithingspro.cloud'

SEND_DATA = True

machine_obj = {}

ob_db = DBHelper("EM_data")

prev_sensor_data_sent = time.time()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN_EM_IU')

HEADERS = {'content-type': 'application/json'}

HOST_SENSOR = os.getenv('HOST_SENSOR')
print(HOST_SENSOR)

ACCESS_TOKEN_SENSOR = os.getenv('ACCESS_TOKEN_SENSOR')
PASSWORD = os.getenv('PASSWORD')
USERNAME = os.getenv('USERNAME1')

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
        log.error(f"Error while converting {hex_str} to float: {e}")
        decimal_value_big_endian = 0.0

    return round(decimal_value_big_endian, 5)


def post_sensors_data(payload):
    try:
        if payload:
            host_tb = f'{HOST}/api/v1/{ACCESS_TOKEN}/telemetry/'
            log.info(f"Sending {payload} to {host_tb}")
            try:
                req_post = requests.post(host_tb, json=payload, headers=HEADERS, timeout=2)
                log.info(req_post.status_code)
                log.info(req_post.text)
                req_post.raise_for_status()
            except Exception as e:
                log.error(f"[-] Error While sending data to server {e}")
        else:
            log.info("got empty payload")
    except Exception as e:
        log.error(f"Error while sending data {e}")



def get_steam_data(sensor_json, parameter_key, parameter_output):
    try:
        req = requests.post(f'{HOST_SENSOR}/advance-query?organizationId=763', json=sensor_json, headers=HEADERS_SENSOR, timeout=2)
        log.info(req.status_code)
        log.info(req.text)
        if req.status_code in [401, 403]:
            pass
            refresh_jwt_token()
        raw_data = req.json()
        payload = {}
        log.info(raw_data)
        id_list = []
        if raw_data is not None:
            max_id = max([m_data['id'] for m_data in raw_data])
            latest_data = {}
            for m_data in raw_data:
                if m_data['id'] == max_id:
                    latest_data = m_data
                    break
            if latest_data:
                hex_value = latest_data[parameter_key]
                float_value = struct.unpack('!f', bytes.fromhex(hex_value))[0]
                payload = {
                    parameter_output: float_value,
                }
                post_sensors_data(payload)
        return payload
    except Exception as e:
        log.error(f"Error while sending the {parameter_key} data {e}")
        return []
steam_data = {
    "STEAM_TEMP": STEAM_TEMP,
    "SPEED": SPEED,
    "PAPER_GSM": PAPER_GSM,
    "STEAM_PRGP_1": STEAM_PRGP_1,
    "STEAM_PRGP_2": STEAM_PRGP_2,
    "STEAM_PRGP_3": STEAM_PRGP_3,
    "STEAM_PRGP_4": STEAM_PRGP_4,
    "STEAM_PRGP_5": STEAM_PRGP_5,
    "STEAM_PRGP_6": STEAM_PRGP_6,
    "STEAM_PRGP_7": STEAM_PRGP_7,
    "STEAM_PRGP_8": STEAM_PRGP_8,
    "STEAM_PRGP_9": STEAM_PRGP_9,
}

parameter_keys = {
    "STEAM_TEMP": "process_parameter_001_a",
    "SPEED": "process_parameter_001_b",
    "PAPER_GSM": "process_parameter_001_c",
    "STEAM_PRGP_1": "process_parameter_001_d",
    "STEAM_PRGP_2": "process_parameter_001_e",
    "STEAM_PRGP_3": "process_parameter_001_f",
    "STEAM_PRGP_4": "process_parameter_001_g",
    "STEAM_PRGP_5": "process_parameter_001_h",
    "STEAM_PRGP_6": "process_parameter_001_i",
    "STEAM_PRGP_7": "process_parameter_001_j",
    "STEAM_PRGP_8": "process_parameter_001_k",
    "STEAM_PRGP_9": "process_parameter_001_l",
}

parameter_output = {'STEAM_TEMP':'INF_UPTM_PR_MAIN_TEMP_DEG_CELCIUS',
                    'SPEED':'INF_UPTM_MAL_SPEED_MPM',
                    'PAPER_GSM':'INF_UPTM_GSM_GSM',
                    'STEAM_PRGP_1':'INF_UPTM_STEAM_PR_GP1_BAR',
                    'STEAM_PRGP_2':'INF_UPTM_STEAM_PR_GP2_BAR',
                    'STEAM_PRGP_3':'INF_UPTM_STEAM_PR_GP3_BAR',
                    'STEAM_PRGP_4':'INF_UPTM_STEAM_PR_GP4_BAR',
                    'STEAM_PRGP_5':'INF_UPTM_STEAM_PR_GP5_BAR',
                    'STEAM_PRGP_6':'INF_UPTM_STEAM_PR_GP6_BAR',
                    'STEAM_PRGP_7':'INF_UPTM_STEAM_PR_GP7_BAR',
                    'STEAM_PRGP_8':'INF_UPTM_STEAM_PR_GP8_BAR',
                    'STEAM_PRGP_9':'INF_UPTM_STEAM_PR_GP9_BAR',
                    }


for key, value in steam_data.items():
    get_steam_data(value, parameter_keys[key], parameter_output[key])
    schedule.every(SENSOR_DATA_INTERVAL).seconds.do(get_steam_data)

def refresh_jwt_token():
    try:
        global ACCESS_TOKEN_SENSOR, HEADERS_SENSOR, USERNAME, PASSWORD
        ob_db.add_access_data(ACCESS_TOKEN_SENSOR)
        refresh_url = f"{HOST_SENSOR}/login"
        a_payload = {'username': base64.b64decode(USERNAME).decode('ascii'),
                     'password': base64.b64decode(PASSWORD).decode('ascii')}

        req = requests.post(refresh_url, json=a_payload, headers=HEADERS, timeout=2)
        log.info(req.status_code)
        log.info(req.text)

        raw_data = req.json()
        if raw_data:
            access_token = raw_data['data']['accessToken']
            if access_token:
                ob_db.add_access_data(access_token)

        at = ob_db.get_access_data()
        if at:
            ACCESS_TOKEN_SENSOR = at
            HEADERS_SENSOR = {'content-type': 'application/json',
                              'Authorization': f"Bearer {ACCESS_TOKEN_SENSOR}"}
    except Exception as e:
        log.error(f"Error while Refreshing JWT TOKEN: {e}")


if __name__ == "__main__":
    try:
        access_token = ob_db.get_access_data()
        if access_token is None:
            log.info("[+] Error No Access Token is Found Refreshing...")
        refresh_jwt_token()

        at = ob_db.get_access_data()
        ACCESS_TOKEN_SENSOR = at
        HEADERS_SENSOR['Authorization'] = f'Bearer {ACCESS_TOKEN_SENSOR}'
        while True:
            schedule.run_pending()
            time.sleep(2)
    except Exception as e:
        log.error(f"Error Running Program {e}")
