"""Простой тест для проверки работы"""

import os
import sys

# Добавляем src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.config_parser import create_config_parser


def test_basic():
    """Базовый тест загрузки конфигурации"""
    print("🧪 Тестирование загрузки конфигурации...")

    # Тестируем XML
    parser = create_config_parser('../configs/config.xml')
    if parser:
        print(" XML конфигурация работает!")
        parser.print_parameters()
    else:
        print(" XML конфигурация не работает")

    # Тестируем JSON
    parser = create_config_parser('../configs/config.json')
    if parser:
        print(" JSON конфигурация работает!")
        parser.print_parameters()
    else:
        print(" JSON конфигурация не работает")


if __name__ == "__main__":
    test_basic()