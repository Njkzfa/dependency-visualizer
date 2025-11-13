#!/usr/bin/env python3
"""Главный модуль инструмента визуализации зависимостей"""

import os
import sys

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli import main

if __name__ == "__main__":
    main()