#!/bin/bash

while true; do
    # Вход в виртуальную среду
    source flask/bin/activate
    
    # Запуск Python-скрипта
    python3 daily_titles_updater.py
    
    # Выход из виртуальной среды
    deactivate
    
    # Ожидание 5 минут (3600 секунд)
    sleep 3600
done
