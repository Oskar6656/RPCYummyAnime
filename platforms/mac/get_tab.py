import os
import subprocess
import pygetwindow as gw
from AppKit import (
    NSApplication,
    NSApp,
    NSApplicationActivationPolicyAccessory,
    NSApplicationActivationPolicyRegular,
)
from src.save_log import logging


def hide_from_dock():
    try:
        app = NSApp
        app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
        app.activateIgnoringOtherApps_(True)
    except Exception as e:
        logging.warning(f"Ошибка: {e}")


async def get_tab_name(yummyanime_tags, browsers):
    active_window = gw.getActiveWindow()
    browser_name = None

    for browser in browsers:
        if browser in active_window:
            browser_name = browser
            break

    script = f'''
    tell application "{browser_name}"
        if exists (window 1) then
            return title of active tab of front window
        else
            return "Нет открытых вкладок"
        end if
    end tell
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    tab_name = result.stdout.strip()

    if any(tag in tab_name for tag in yummyanime_tags):
        return tab_name

