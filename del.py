HOST = 'https://ithingspro.cloud'

SEND_DATA = True

machine_obj = {}

ob_db = DBHelper("EM_data")

prev_sensor_data_sent = time.time()

ACCESS_TOKEN = 'Nmz6IGFsFEjhmFhDjThD'

HEADERS = {'content-type': 'application/json'}

HOST_SENSOR = 'https://api.infinite-uptime.com/api/3.0/idap-api'
print(HOST_SENSOR)

ACCESS_TOKEN_SENSOR = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIyY0NxRnpxRXJrNU5GS1RjTi1YSk1IdE9NS2tWVTZXS1hIdHZFMF8xZE5ZIn0.eyJleHAiOjE3MTAyNjI1NTIsImlhdCI6MTcxMDIxOTM1MiwianRpIjoiZTcxZWMyNzItNDNkZC00MzI3LTgwNzYtZWVhYmU1Zjc5NjFkIiwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS5pbmZpbml0ZS11cHRpbWUuY29tL3JlYWxtcy9pZGFwIiwic3ViIjoiZjo2MGNhNzY4Yy1iMTA0LTQ0OTktYjU4Yy05MzliOTdlNzAzM2Q6OTg3NCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImlkYXAiLCJzZXNzaW9uX3N0YXRlIjoiNGE2MzM3MzItYzQxZC00ZjEyLWJlMTYtZDAwMTEzZTgzZWNlIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwic2lkIjoiNGE2MzM3MzItYzQxZC00ZjEyLWJlMTYtZDAwMTEzZTgzZWNlIiwiaXNfYWRtaW4iOiJmYWxzZSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6IlNoaXZhbSBNYXVyeWEiLCJpZGFwX3JvbGUiOiJST0xFX1VTRVIiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzaGl2YW1tYXVyeWEwMjQ4QGdtYWlsLmNvbSIsImdpdmVuX25hbWUiOiJTaGl2YW0iLCJsb2NhbGUiOiJlbiIsImZhbWlseV9uYW1lIjoiTWF1cnlhIiwiZW1haWwiOiJzaGl2YW1tYXVyeWEwMjQ4QGdtYWlsLmNvbSJ9.mUBIzeh5Vny593evB7MHU0oe4SGCPv8wNcup-pDrBG9ug_vLoa72nq9Z2sw87e_4QHlPUxhTL-LcnLYBjTfgHxNlyTbkCeL6YfZA3bQH2e-jmkSBatBOu1d4u27xTSOR-QCmAbAAniz61wLzvfIvz8kyzHzXdSn_9frrIQsoMCVDo0anWaiasaP7HHy5Tj1KLVIRfPMsfsvQX92XkkIPx_HMD4X2ge7nQWEiutp499kpoEuOz2beriHNQrr2eYvcmUJk1rQuw3bNNq9g2c1F7Rbl6R5KZgKSDpN3QyS3p6masP5SAwBisDbBDJ9VrX4_-f5pCJk2NtoFao7Eklk1Gg'

PASSWORD = "'RTRzeVA0JCR3MHJk'"
USERNAME = "'c2hpdmFtbWF1cnlhMDI0OEBnbWFpbC5jb20='"

HEADERS_SENSOR = {'content-type': 'application/json',
                  'Authorization': f"Bearer {ACCESS_TOKEN_SENSOR}"}