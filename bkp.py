import datetime
import requests
import json
import sys
import time
import base64
import logging
import logging.handlers
from database import DBHelper
from logging.handlers import TimedRotatingFileHandler
import os
import struct
from datetime import datetime, timedelta
log_level = logging.INFO
from dotenv import load_dotenv

load_dotenv()
FORMAT = '%(asctime)-15s %(levelname)-8s %(name)s %(module)-15s:%(lineno)-8s %(message)s'

logFormatter = logging.Formatter(FORMAT)
log = logging.getLogger("HIS_LOGS")
ob_db = DBHelper("EM_data")
# # checking and creating logs directory here

if getattr(sys, 'frozen', False):
    dirname = os.path.dirname(sys.executable)
else:
    dirname = os.path.dirname(os.path.abspath(__file__))
logdir = f"{dirname}/logs"
log.info(f"log directory name is {logdir}")
if not os.path.isdir(logdir):
    log.info("[-] logs directory doesn't exists")
    try:
        os.mkdir(logdir)
        log.info("[+] Created logs dir successfully")
    except Exception as e:
        log.info(f"[-] Can't create dir logs Error: {e}")

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

# ENV FILE VARIABLES
HOST = os.getenv('HOST')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
USERNAME = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST_SENSOR = os.getenv("HOST_SENSOR")
HOST_SENSOR1 = os.getenv("HOST_SENSOR1")
ACCESS_TOKEN_SENSOR = ob_db.get_access_data()
# END REGION

payload = {}
HEADERS_1 = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic Og==',
    'Cookie': 'JSESSIONID=5BB7E1FA21C8A0A94FAA017C90CA32B1'
}

HEADERS = {
    'Authorization': f'Bearer {ACCESS_TOKEN_SENSOR}'
}


def convert_hex_to_ieee754(hex_str):
    try:
        # currently converting to big endian
        decimal_value_big_endian = struct.unpack('>f', bytes.fromhex(hex_str))[0]
    except Exception as err:
        log.error(f"Error while converting {hex_str} to float: {err}")
        decimal_value_big_endian = 0.0

    return round(decimal_value_big_endian, 5)


def get_equipment_area_asset():
    try:
        payload1 = {}
        payload = {}
        # Get the current date in the format YYYY-MM-DD
        current_date = datetime.now().strftime('%Y-%m-%d')
        today = datetime.today()
        previous_day = today - timedelta(days=1)
        date = previous_day.strftime("%Y-%m-%d")
        print(date)
        plant_id = [3047, 3048, 3049, 3058, 3059, 3060, 3061, 3062, 3063]
        for pid in plant_id:
            url = f"{HOST_SENSOR1}equipmentId={pid}&start={date}T12%3A13%3A14Z&end={current_date}T12%3A13%3A14Z&page=" \
                  f"1&pageSize=10"
            req1 = requests.request("POST", url, headers=HEADERS, data=payload1)
            # print(req1.json())  # Print the response
            if req1.status_code in [401, 403]:
                pass
                refresh_jwt_token()
            raw_data = req1.json()
            log.info(raw_data)

            if raw_data is not None:

                latest_data = raw_data['data']['area']['machineGropus']['externalTableResponse'][0]['externalTableData']
                latest_data1 = raw_data['data']['externalTableResponse']
                log.info(f'latest data is {latest_data1}')
                if pid == 3047:
                    data = latest_data1[0]['externalTableData']['00:30:11:78:A1:A6:01']
                    max_item = max(data, key=lambda x: x['id'])
                    latest_data_a = max_item['process_parameter_001_a']
                    payload.update({'Steam Temperature': convert_hex_to_ieee754(latest_data_a)})

                    data2 = latest_data1[1]['externalTableData']['00:30:11:78:A1:A6:02']
                    max_item = max(data2, key=lambda x: x['id'])
                    latest_data_b = max_item['process_parameter_001_b']
                    payload.update({'Paper GSM': convert_hex_to_ieee754(latest_data_b)})

                    data3 = latest_data1[2]['externalTableData']['00:30:11:78:A1:A6:03']
                    max_item = max(data3, key=lambda x: x['id'])
                    latest_data_c = max_item['process_parameter_001_c']
                    payload.update({'Machine Speed': convert_hex_to_ieee754(latest_data_c)})

                    data4 = latest_data['00:30:11:78:A1:A6:04']
                    max_item = max(data4, key=lambda x: x['id'])
                    latest_data_d = max_item['process_parameter_001_d']
                    payload.update({'Steam Presure GP1': convert_hex_to_ieee754(latest_data_d)})

                elif pid == 3048:
                    data4 = latest_data['00:30:11:78:A1:A6:05']
                    max_item = max(data4, key=lambda x: x['id'])
                    latest_data_e = max_item['process_parameter_001_e']
                    payload.update({'Steam Presure GP2': convert_hex_to_ieee754(latest_data_e)})
                elif pid == 3049:
                    data4 = latest_data['00:30:11:78:A1:A6:06']
                    max_item = max(data4, key=lambda x: x['id'])
                    latest_data_f = max_item['process_parameter_001_f']
                    payload.update({'Steam Presure GP3': convert_hex_to_ieee754(latest_data_f)})
                elif pid == 3058:
                    data4 = latest_data['00:30:11:78:A1:A6:07']
                    max_item = max(data4, key=lambda x: x['id'])
                    latest_data_g = max_item['process_parameter_001_g']
                    payload.update({"Steam Presure GP4": convert_hex_to_ieee754(latest_data_g)})
                elif pid == 3059:
                    data = latest_data['00:30:11:78:A1:A6:08']
                    max_item = max(data, key=lambda x: x['id'])
                    latest_data_h = max_item['process_parameter_001_h']
                    payload.update({'Steam Presure GP5': convert_hex_to_ieee754(latest_data_h)})
                elif pid == 3060:
                    data = latest_data['00:30:11:78:A1:A6:09']
                    max_item = max(data, key=lambda x: x['id'])
                    latest_data_i = max_item['process_parameter_001_i']
                    payload.update({'Steam Presure GP6': convert_hex_to_ieee754(latest_data_i)})
                elif pid == 3061:
                    data = latest_data['00:30:11:78:A1:A6:10']
                    max_item = max(data, key=lambda x: x['id'])
                    latest_data_j = max_item['process_parameter_001_j']
                    payload.update({'Steam Presure GP7': convert_hex_to_ieee754(latest_data_j)})
                elif pid == 3062:
                    data = latest_data['00:30:11:78:A1:A6:11']
                    max_item = max(data, key=lambda x: x['id'])
                    latest_data_k = max_item['process_parameter_001_k']
                    payload.update({'Steam Presure GP8': convert_hex_to_ieee754(latest_data_k)})
                elif pid == 3063:
                    data = latest_data['00:30:11:78:A1:A6:12']
                    max_item = max(data, key=lambda x: x['id'])
                    latest_data_k = max_item['process_parameter_001_l']
                    payload.update({'Steam Presure GP9': convert_hex_to_ieee754(latest_data_k)})
        # return payload
    except Exception as err:
        log.error(f"Error while getting the API data {err}")
        return []


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
    except Exception as ee:
        log.error(f"Error while sending data {ee}")


def refresh_jwt_token():
    try:
        global ACCESS_TOKEN_SENSOR, HEADERS_1, USERNAME, PASSWORD, HEADERS
        ob_db.add_access_data(ACCESS_TOKEN_SENSOR)
        refresh_url = 'https://api.infinite-uptime.com/api/3.0/idap-api/login'
        # log.info(f"+++++++++++++++++++++++++++++++++++{base64.b64decode(USERNAME).decode('ascii')}")
        # log.info(base64.b64decode(PASSWORD).decode('ascii'))
        a_payload = json.dumps({'username': 'rishavpreet@hisgroup.in',
                                'password': "SdS6ahGbGZ5@#f"})
        req = requests.request("POST", refresh_url, headers=HEADERS_1, data=a_payload)
        log.info(req.status_code)
        raw_data = req.json()
        if raw_data:
            access_token = raw_data['data']['accessToken']
            if access_token:
                ob_db.add_access_data(access_token)
        at = ob_db.get_access_data()
        if at:
            ACCESS_TOKEN_SENSOR = at
            HEADERS = {'Authorization': f"Bearer {ACCESS_TOKEN_SENSOR}"}
    except Exception as e:
        log.error(f"Error while Refreshing JWT TOKEN: {e}")


if __name__ == "__main__":
    try:
        while True:
            access_token = ob_db.get_access_data()
            if access_token is None:
                log.info("[+] Error No Access Token is Found Refreshing...")
                refresh_jwt_token()
            data = get_equipment_area_asset()
            log.info(data)
            at = ob_db.get_access_data()
            ACCESS_TOKEN_SENSOR = at
            HEADERS['Authorization'] = f'Bearer {ACCESS_TOKEN_SENSOR}'
            time.sleep(30)
    except Exception as e:
        log.info(f"Error Running Program {e}")
