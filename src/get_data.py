import os
import sys
import requests
from PIL import Image
from save_log import logging


# Добавляем корневую папку в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Ипортируем config
from config_op import *

try:
    # Добавляем заголовки, чтобы указать на отсутствие кэширования
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate, proxy-revalidate",
        "Pragma": "no-cache",  # Для старых версий HTTP/1.0
        "Expires": "0"  # Устанавливаем время истечения как 0
    }
    
    response = requests.get(f"{rpc_api_server_url}/api/get_program_data", headers=headers)
    response.raise_for_status()
    data = response.json()

    program_name = data.get("program_name", "")
    program_site_url = data.get("program_site_url", "")
    yum_site_url = data.get("yum_site_url", "")

    program_version = data.get("program_version", "")
    yummyanime_tags = data.get("yummyanime_tags", [])
    browsers = data.get("browsers", [])
    RPC_CLIENT_ID = data.get("RPC_CLIENT_ID", "")

except Exception as e:
    logging.error(f"Ошибка: {e}")
    os._exit(0)



def get_all_images():
    try:
        base_path = (
            sys._MEIPASS if getattr(sys, "frozen", False) 
            else os.path.dirname(os.path.abspath(__file__))
        )
        img_dir = os.path.join(base_path, "assets", "img")

        image_names = [
            "logo_rpc_white.png",
            "logo_rpc_green.png",
            "logo_rpc_red.png",
            "logo_rpc_grey.png",
            "logo_rpc_yellow.png",
            "logo_rpc.png"
        ]

        images = [Image.open(os.path.join(img_dir, name)) for name in image_names]
        return images

    except Exception as e:
        logging.error(f"Ошибка загрузки изображений: {e}")
        sys.exit(1)  # Код завершения 1 (ошибка)


def get_rpc_data_from_server(tab: str):
    url = f"{rpc_api_server_url}/api/rpc_data"
    
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Content-Type': 'application/json'
    }
    payload = {
        'tab_name': tab 
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Ошибка: {response.status_code}")
            return {'error': f'Failed to fetch data, status code: {response.status_code}'}
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе: {e}")
        return {'error': f'Error during the request: {str(e)}'}


