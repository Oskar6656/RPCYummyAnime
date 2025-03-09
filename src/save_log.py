import logging
import os  
import subprocess  
import platform  
import sys

def get_log_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # Для PyInstaller
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Поднимаемся на уровень выше

    return os.path.join(base_path, "logs", "logs.txt")

# Используем путь
log_path = get_log_path()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат сообщения
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8")
    ]
)


def open_logs():  
    try: 
        check_logs() 
        if platform.system() == "Darwin":  # macOS  
            subprocess.run(["open", log_path])  
        elif platform.system() == "Windows":  
            os.startfile(log_path)  
        else:  # Linux  
            subprocess.run(["xdg-open", log_path])  
    except Exception as e:  
        logging.error(f"Ошибка: {e}")


def check_logs():
    if os.path.exists(log_path):
        if os.path.getsize(log_path) > 10 * 1024 * 1024:
            with open(log_path, "w"):
                pass
            logging.info("Файл логов очищен (превышен лимит 10MB)")
