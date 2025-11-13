"""Модуль для работы с командной строкой"""

import argparse
import sys
import os

# Импортируем наш парсер
from .config_parser import create_config_parser


def main():
    """Основная функция CLI"""
    parser = argparse.ArgumentParser(
        description='Инструмент визуализации графа зависимостей пакетов',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'config_file',
        nargs='?',
        default='configs/config.xml',
        help='Путь к конфигурационному файлу'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Подробный вывод'
    )

    args = parser.parse_args()

    if args.verbose:
        print(" Запуск инструмента визуализации зависимостей")
        print(f" Конфигурационный файл: {args.config_file}")

    # Загрузка конфигурации
    config_parser = create_config_parser(args.config_file)

    if not config_parser:
        print(" Не удалось загрузить конфигурацию. Программа завершена.")
        sys.exit(1)

    # Вывод параметров (требование этапа 1)
    config_parser.print_parameters()

    if args.verbose:
        print(" Конфигурация готова к использованию.")

    print("\n Конфигурация загружена.")


if __name__ == "__main__":
    main()