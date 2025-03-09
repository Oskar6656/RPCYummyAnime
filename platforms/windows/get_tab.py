import pygetwindow as gw


async def get_tab_name(yummyanime_tags, browsers):
    active_window = gw.getAllTitles()
    browser_name = None

    # Проверяем, есть ли тег в каком-либо окне
    for window in active_window:
        for tag in yummyanime_tags:
            if tag in window:
                return window


def hide_from_dock():
    pass