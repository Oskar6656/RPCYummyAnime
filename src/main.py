import os
import sys
import time
import asyncio
import threading
import webbrowser

import pystray
from pystray import MenuItem as item, Menu as menu, Icon

from get_data import *
from rpc_func import *
from save_log import *
from config_op import *


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if sys.platform == "darwin":  # macOS
    from platforms.mac.get_tab import get_tab_name, hide_from_dock
elif sys.platform == "win32":  # Windows
    from platforms.windows.get_tab import get_tab_name, hide_from_dock
else:
    raise RuntimeError("Unsupported OS")


# Переменная для отслеживания состояния
is_active = default_is_active  # Начальное состояние - из config.json
site_found = False  # Статус наличия открытого сайта
tray_icon = None  # Icon
client = None  # RPC клиент


async def update_rpc():
    global is_active, site_found, client
    previous_tab = None

    while True:
        tab = await get_tab_name(yummyanime_tags, browsers) if is_active else None

        if tab:
            site_found = True
            if tab != previous_tab:  # Изменился ли таб?
                rpc_data = get_rpc_data_from_server(tab)
                rpc_data["start"] = int(time.time())  # Устанавливаем актуальное время
                client = await set_discord_activity(rpc_data, client, is_active)
                update_tray_menu(is_active)  # Обновляем меню только при смене вкладки

        else:  # Если вкладка не найдена
            site_found = False
            if previous_tab is not None:  # Только если была вкладка раньше
                client = await set_discord_activity(None, client, is_active)
                update_tray_menu(is_active)

        previous_tab = tab  # Обновляем переменную только в конце цикла

        logging.info(
            f"tab: {tab}, previous_tab: {previous_tab}, is_active: {is_active}, site_found: {site_found}, client: {client}"
        )
        await asyncio.sleep(5)


def create_image(is_active):
    if not colorized_icon:
        return image_icon_white
    if is_active:
        image = image_icon_rpc
        if site_found:
            image = image_icon_green
    else:
        image = image_icon_grey

    return image


def update_tray_menu(is_active):
    try:
        tray_icon.menu = pystray.Menu(
            item(
                "Вкл активность" if not is_active else "Выкл активность",
                action=on_click,
            ),
            pystray.Menu.SEPARATOR,
            item("YummyAnime", action=on_click),
            item("Сайт программы", action=on_click),
            pystray.Menu.SEPARATOR,
            item(f"Версия {program_version}", action=on_click, enabled=False),
            item(text=f"Логи", action=on_click),
            item(text=f"Настройки", action=on_click),
            item(text="Выйти", action=on_click),
        )

        tray_icon.icon = create_image(is_active)
        tray_icon.update_menu()

    except Exception as e:
        logging.error(f"Ошибка: {e}")


def on_click(icon, menu_item):
    global is_active
    try:
        if menu_item.text == "Вкл активность" or menu_item.text == "Выкл активность":
            is_active = not is_active
            update_tray_menu(is_active)
        if menu_item.text == "YummyAnime":
            webbrowser.open(yum_site_url)
        if menu_item.text == "Сайт программы":
            webbrowser.open(program_site_url)
        if menu_item.text == "Настройки":
            open_config()
        if menu_item.text == "Логи":
            open_logs()
        if menu_item.text == "Выйти":
            logging.info(f"Завершение программы")
            os._exit(0)
    except Exception as e:
        logging.error(f"Ошибка: {e}")


def create_tray_icon():
    global tray_icon
    menu_items = pystray.Menu(
        item(text="Вкл активность", action=on_click),
        pystray.Menu.SEPARATOR,
        item(text="YummyAnime", action=on_click),
        item(text="Сайт программы", action=on_click),
        pystray.Menu.SEPARATOR,
        item(text=f"Версия {program_version}", action=on_click, enabled=False),
        item(text=f"Логи", action=on_click),
        item(text=f"Настройки", action=on_click),
        item(text="Выйти", action=on_click),
    )



    tray_icon = Icon(name=program_name, title=program_name, icon=create_image(is_active), menu=menu_items)
    hide_from_dock()
    tray_icon.run()


async def main():
    global start, image_icon_rpc, image_icon_green, image_icon_white, image_icon_grey
    all_img = get_all_images()
    image_icon_white = all_img[0]
    image_icon_green = all_img[1]
    image_icon_rpc = all_img[5]
    image_icon_grey = all_img[3]

    start = int(time.time())
    thread3 = threading.Thread(target=lambda: asyncio.run(update_rpc()))
    thread3.daemon = True
    thread3.start()

    create_tray_icon()



# Точка входа
if __name__ == "__main__":
    logging.info("Программа запущена")
    register_device()
    check_logs()
    asyncio.run(main())