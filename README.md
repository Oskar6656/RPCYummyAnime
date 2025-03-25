  # RPCYummyAnime

## О программе
**RPCYummyAnime** – это утилита, позволяющая отображать Вашу активность с сайта [YummyAnime](https://yummy-anime.ru/) в профиле Discord.

## Установка

1. Скачайте архив с программой по [ссылке](https://discord.yani.tv/).
2. Распакуйте архив.
3. Запустите программу.


## Настройка Discord
1. Откройте **Discord**.
2. Перейдите в **Настройки пользователя > Конфиденциальность активности**.
3. Включите все 4 пункта в настройках. ([Пример](https://discord.yani.tv/static/img/docs_pics/rpc_sw.png))

## Использование
1. Убедитесь, что **Discord** запущен.
2. Запустите **RPCYummyAnime**.
3. Откройте сайт [YummyAnime](https://yummy-anime.ru/).
4. Теперь Ваша активность с сайта будет отображаться в профиле Discord!

## Установка зависимостей (для разработчиков)
Если вы собираете программу самостоятельно, установите зависимости:

### macOS:
```bash
pip install -r requirements-mac.txt
```

### Windows:
```powershell
pip install -r requirements-win.txt
```

## Сборка исполняемых файлов (.exe и .app)
Для создания исполняемых файлов используется PyInstaller. Установите его перед сборкой:

```bash
pip install pyinstaller
```
После установки запустите соответствующий скрипт для сборки:

### Windows
Запустите сборку

```powershell
build.bat
```

### macOS
1. Сделайте файл исполняемым

```bash
chmod +x build.sh
```

2. Запустите сборку

```bash
./build.sh
```

**Требуемая версия Python:** 3.10

## Лицензия
MIT License

