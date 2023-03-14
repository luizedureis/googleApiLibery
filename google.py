from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from googleapiclient.http import MediaFileUpload
from datetime import datetime
import time



def upload_to_drive(chromedriver,folder_id,folder_id_backup,name):
    '''
        chromedriver -> API do google\n
        folder_id -> id da pasta principal\n
        folder_id_backup -> id da pasta de backup
        name -> nome do arquivo
    '''
    # Keys para capturar pastas drive
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    CLIENT_SECRET_FILE = chromedriver
    API_NAME = 'drive'
    API_VERSION = 'V3'

    # Jogando arquivos novos para a pasta drive target
    folder_id_backup = '19tH-tJgDHUeaAkvuL7Li3XDOXVeAocmh'
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    query = f"parents = '{folder_id}'"
    response = service.files().list(q=query).execute()
    files = response.get('files')
    next_page_token = response.get('nextPageToken')
    while next_page_token:
        response = service.files().list(q=query, pageToken = next_page_token).execute()
        files.extend(response.get('files'))
        next_page_token = response.get("nextPageToken")

    for f in files:
        if f['mimeType'] != 'application/vnd.google-apps.folder':
            service.files().update(
                fileId=f.get('id'),
                addParents=folder_id_backup,
                removeParents=folder_id
            ).execute()

    print(name)
    file_metadata = {
        'name': name,
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }
    media = MediaFileUpload(name, mimetype='application/vnd.google-apps.spreadsheet')
    idfile = service.files().create(body=file_metadata, media_body=media, fields='id').execute()



import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt