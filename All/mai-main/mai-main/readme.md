## Окружение и примеры для выполнения лабораторных работ по дисциплине "Методы ИИ"

### Python

Используется Python версии 3.12

Установщик https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe

### Poetry

Для создания и настройки окружения проекта необходимо установить poetry

**Для Windows (Powershell)**

```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

**Linux, macOS, Windows (WSL)**

```
curl -sSL https://install.python-poetry.org | python3 -
```

**Добавление poetry в PATH**

1. Открыть настройки переменных среды \
    \
   <img src="docs/path1.png" width="300"> \
    \
   <img src="docs/path2.png" width="400"> \
2. Изменить переменную Path текущего пользователя \
    \
   <img src="docs/path3.png" width="500"> \
3. Добавление пути `%APPDATA%\Python\Scripts` до исполняемого файла poetry \
    \
   <img src="docs/path4.png" width="400">

### Создание окружения

```
poetry install
```

### Запуск тестового сервиса

Запустить тестовый сервис можно с помощью VSCode (см. launch.json в каталоге .vscode).

Также запустить тестовый сервис можно с помощью командной строки:

1. Активация виртуального окружения -- `poetry shell`

2. Запуск сервиса -- `python run.py`

Для выходы из виртуального окружения используется команду `exit`
