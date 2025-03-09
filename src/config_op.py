import os
import sys
import platform
import subprocess
import yaml
from save_log import logging

def get_config_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, "config", "config.yaml")


def load_config():
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            
            # Получаем переменные из конфига
            api_domain = config['api_url']
            default_is_active = config['default_is_active']
            colorized_icon = config['colorized_icon']
            api_url = f"https://{api_domain}"

            return api_url, default_is_active, colorized_icon
        
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return "", False, False


def open_config():  
    try:  
        if platform.system() == "Darwin":  # macOS  
            subprocess.run(["open", config_path])  
        elif platform.system() == "Windows":  
            os.startfile(config_path)  
        else:  # Linux  
            subprocess.run(["xdg-open", config_path])  
    except Exception as e:  
        logging.error(f"Ошибка: {e}")



config_path = get_config_path()

# Загружаем конфиг
api_url, default_is_active, colorized_icon = load_config()

rpc_api_server_url = api_url

