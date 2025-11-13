"""Модуль для работы с командной строкой"""

import argparse
import sys
import os

# Импортируем наши модули
from .config_parser import create_config_parser
from .dependency_fetcher import create_dependency_fetcher


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

    # ЭТАП 2: Сбор данных о зависимостях
    print("\n Сбор данных о зависимостях...")

    # Создаем fetcher для работы с зависимостями
    fetcher = create_dependency_fetcher(config_parser.get_repository_url())

    dependencies = set()

    if config_parser.is_test_mode():
        # Тестовый режим - зависимости из файла
        test_file = "test_dependencies.txt"  # Можно сделать настраиваемым
        dependencies = fetcher.get_test_dependencies(test_file)
    else:
        # Реальный режим - зависимости из репозитория
        dependencies = fetcher.get_package_dependencies(
            package_name=config_parser.get_package_name(),
            package_version=config_parser.get_package_version()
        )

    # Вывод результатов (требование этапа 2)
    print(f"\n ПРЯМЫЕ ЗАВИСИМОСТИ ПАКЕТА '{config_parser.get_package_name()}':")
    print("=" * 50)

    if dependencies:
        for i, dep in enumerate(sorted(dependencies), 1):
            print(f"  {i:2d}. {dep}")
    else:
        print("   Зависимости не найдены или пакет не имеет зависимостей")

    print("=" * 50)
    print(f" Найдено зависимостей: {len(dependencies)}")

    if args.verbose:
        print(" Данные собраны.")

    print("\n (основные операции).")


if __name__ == "__main__":
    main()