import json
import os
from typing import Dict, Any, Optional

try:
    from lxml import etree

    HAS_LXML = True
except ImportError:
    HAS_LXML = False
    print(" Предупреждение: lxml не установлен. XML парсинг недоступен.")


class ConfigParser:
    """Парсер конфигурационных файлов для анализа зависимостей пакетов"""

    REQUIRED_PARAMS = ['package_name']

    DEFAULT_CONFIG = {
        'package_name': '',
        'repository_url': 'https://pypi.org/pypi',
        'test_mode': False,
        'package_version': '',
        'output_image': 'dependencies_graph.svg',
        'max_depth': 5,
        'substring_filter': '',
        'ascii_tree': False
    }

    def __init__(self):
        self.config_data = self.DEFAULT_CONFIG.copy()
        self.is_loaded = False
        self.config_file_path = None

    def load_from_file(self, file_path: str) -> bool:
        """Загрузка конфигурации из файла"""
        try:
            if not os.path.exists(file_path):
                print(f" Ошибка: Файл '{file_path}' не найден")
                return False

            self.config_file_path = file_path
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension == '.xml':
                if not HAS_LXML:
                    print(" Ошибка: lxml не установлен. Установите: pip install lxml")
                    return False
                return self._parse_xml(file_path)
            elif file_extension in ['.json', '.conf']:
                return self._parse_json(file_path)
            else:
                print(f" Ошибка: Неподдерживаемый формат файла '{file_extension}'")
                return False

        except Exception as e:
            print(f" Ошибка при загрузке конфигурации: {e}")
            return False

    def _parse_xml(self, file_path: str) -> bool:
        """Парсинг XML конфигурационного файла"""
        try:
            tree = etree.parse(file_path)
            root = tree.getroot()

            for element in root:
                tag = element.tag
                text = element.text

                if text is not None:
                    if tag in ['test_mode', 'ascii_tree']:
                        self.config_data[tag] = text.lower() in ['true', '1', 'yes']
                    elif tag in ['max_depth']:
                        try:
                            self.config_data[tag] = int(text)
                        except ValueError:
                            print(f" Предупреждение: Некорректное значение для {tag}")
                    else:
                        self.config_data[tag] = text

            self.is_loaded = True
            print(f" XML конфигурация загружена из '{file_path}'")
            return True

        except Exception as e:
            print(f" Ошибка парсинга XML: {e}")
            return False

    def _parse_json(self, file_path: str) -> bool:
        """Парсинг JSON конфигурационного файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            for key, value in json_data.items():
                if key in self.config_data:
                    self.config_data[key] = value
                else:
                    print(f" Предупреждение: Неизвестный параметр '{key}'")

            self.is_loaded = True
            print(f" JSON конфигурация загружена из '{file_path}'")
            return True

        except Exception as e:
            print(f" Ошибка парсинга JSON: {e}")
            return False

    def validate_config(self) -> bool:
        """Валидация загруженной конфигурации"""
        if not self.is_loaded:
            print(" Ошибка: Конфигурация не загружена")
            return False

        for param in self.REQUIRED_PARAMS:
            if not self.config_data.get(param):
                print(f" Ошибка: Обязательный параметр '{param}' не указан")
                return False

        if not self.config_data['test_mode'] and not self.config_data['repository_url']:
            print(" Ошибка: Для обычного режима должен быть указан repository_url")
            return False

        if self.config_data['max_depth'] < 1:
            print(" Ошибка: max_depth должен быть положительным числом")
            return False

        print(" Конфигурация прошла валидацию")
        return True

    def print_parameters(self):
        """Вывод всех параметров конфигурации в формате ключ-значение"""
        if not self.is_loaded:
            print(" Конфигурация не загружена")
            return

        print("\n" + "=" * 50)
        print(" ПАРАМЕТРЫ КОНФИГУРАЦИИ")
        print("=" * 50)

        for key, value in self.config_data.items():
            print(f"  {key}: {value}")

        print("=" * 50)

    # Геттеры
    def get_package_name(self) -> str:
        return self.config_data['package_name']

    def get_repository_url(self) -> str:
        return self.config_data['repository_url']

    def is_test_mode(self) -> bool:
        return self.config_data['test_mode']

    def get_package_version(self) -> str:
        return self.config_data['package_version']

    def get_output_image(self) -> str:
        return self.config_data['output_image']

    def get_max_depth(self) -> int:
        return self.config_data['max_depth']

    def get_substring_filter(self) -> str:
        return self.config_data['substring_filter']

    def is_ascii_tree(self) -> bool:
        return self.config_data['ascii_tree']


def create_config_parser(file_path: str) -> Optional[ConfigParser]:
    """Создает и загружает парсер конфигурации"""
    parser = ConfigParser()
    if parser.load_from_file(file_path) and parser.validate_config():
        return parser
    return None