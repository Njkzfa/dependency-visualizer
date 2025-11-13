"""
Модуль для получения зависимостей пакетов из PyPI
"""

import requests
import json
from typing import Set, Dict, List, Optional
from urllib.parse import urljoin
import re


class DependencyFetcher:
    """
    Класс для получения информации о зависимостях пакетов Python из PyPI
    """

    def __init__(self, repository_url: str = "https://pypi.org/pypi"):
        """
        Инициализация fetcher'а

        Args:
            repository_url: Базовый URL репозитория пакетов
        """
        self.repository_url = repository_url
        self.session = requests.Session()
        # Устанавливаем заголовки для вежливого scraping'а
        self.session.headers.update({
            'User-Agent': 'DependencyVisualizer/1.0 (Educational Project)'
        })

    def get_package_dependencies(self, package_name: str, package_version: str = "") -> Set[str]:
        """
        Получение прямых зависимостей пакета

        Args:
            package_name: Имя пакета
            package_version: Версия пакета (если пусто - последняя версия)

        Returns:
            Set[str]: Множество имен зависимых пакетов
        """
        try:
            # Получаем информацию о пакете
            package_info = self._get_package_info(package_name)
            if not package_info:
                return set()

            # Определяем версию
            version = package_version if package_version else package_info.get('info', {}).get('version', '')
            if not version:
                print(f" Не удалось определить версию пакета {package_name}")
                return set()

            # Получаем зависимости для конкретной версии
            return self._get_dependencies_for_version(package_info, version)

        except Exception as e:
            print(f" Ошибка при получении зависимостей для {package_name}: {e}")
            return set()

    def _get_package_info(self, package_name: str) -> Optional[Dict]:
        """
        Получение общей информации о пакете из PyPI JSON API

        Args:
            package_name: Имя пакета

        Returns:
            Dict или None: Информация о пакете
        """
        try:
            url = f"{self.repository_url}/{package_name}/json"
            response = self.session.get(url, timeout=10)

            if response.status_code == 404:
                print(f" Пакет '{package_name}' не найден в репозитории")
                return None
            elif response.status_code != 200:
                print(f" Ошибка HTTP {response.status_code} при запросе {package_name}")
                return None

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f" Ошибка сети при запросе {package_name}: {e}")
            return None

    def _get_dependencies_for_version(self, package_info: Dict, version: str) -> Set[str]:
        """
        Извлечение зависимостей для конкретной версии пакета

        Args:
            package_info: Информация о пакете
            version: Версия пакета

        Returns:
            Set[str]: Множество зависимостей
        """
        dependencies = set()

        try:
            # Ищем информацию о релизах
            releases = package_info.get('releases', {})
            if version not in releases:
                print(f" Версия {version} не найдена для пакета {package_info.get('info', {}).get('name')}")
                return dependencies

            release_files = releases[version]
            if not release_files:
                print(f" Для версии {version} нет файлов релиза")
                return dependencies

            # Способ 1: Используем информацию из info (основной способ)
            info = package_info.get('info', {})
            requires_dist = info.get('requires_dist', [])

            if requires_dist:
                dependencies.update(self._parse_requires_dist(requires_dist))
                print(f" Найдено {len(dependencies)} зависимостей в метаданных пакета")
                return dependencies

            # Способ 2: Если в метаданных нет информации, пробуем скачать wheel
            print(" Зависимости не найдены в метаданных, пробуем анализ wheel...")
            for file_info in release_files:
                if file_info.get('packagetype') == 'bdist_wheel':
                    wheel_deps = self._get_dependencies_from_wheel(file_info['url'])
                    dependencies.update(wheel_deps)
                    if dependencies:
                        break

            if dependencies:
                print(f" Найдено {len(dependencies)} зависимостей из wheel")
            else:
                print(" У пакета нет зависимостей")

        except Exception as e:
            print(f" Ошибка при извлечении зависимостей: {e}")

        return dependencies

    def _parse_requires_dist(self, requires_dist: List[str]) -> Set[str]:
        """
        Парсинг списка зависимостей из requires_dist

        Args:
            requires_dist: Список строк зависимостей

        Returns:
            Set[str]: Множество имен пакетов
        """
        dependencies = set()

        for requirement in requires_dist:
            if not requirement:
                continue

            # Убираем версионные ограничения и extras
            # Пример: "requests>=2.25.0 ; extra == 'security'" -> "requests"
            package_name = self._extract_package_name(requirement)
            if package_name and package_name not in ['', 'python']:
                dependencies.add(package_name)

        return dependencies

    def _extract_package_name(self, requirement: str) -> str:
        """
        Извлечение чистого имени пакета из строки требования

        Args:
            requirement: Строка требования (например "requests>=2.25.0")

        Returns:
            str: Чистое имя пакета
        """
        try:
            # Убираем extras: requests[security] -> requests
            requirement = requirement.split('[')[0]

            # Убираем версионные ограничения и условия
            # Разбиваем по ; для условий и по пробелам для версий
            parts = requirement.split(';')[0].strip().split()

            if parts:
                package_name = parts[0]
                # Убираем операторы сравнения если они есть в начале
                for operator in ['==', '!=', '<=', '>=', '<', '>', '~=']:
                    if operator in package_name:
                        package_name = package_name.split(operator)[0]

                return package_name.strip()

            return ""

        except Exception as e:
            print(f" Ошибка парсинга требования '{requirement}': {e}")
            return ""

    def _get_dependencies_from_wheel(self, wheel_url: str) -> Set[str]:
        """
        Альтернативный способ: получение зависимостей из wheel файла
        (Более сложный, используется если в метаданных нет информации)

        Args:
            wheel_url: URL wheel файла

        Returns:
            Set[str]: Множество зависимостей
        """
        # Этот метод сложнее в реализации, пока возвращаем пустое множество
        # В реальном проекте здесь был бы код для скачивания и анализа .whl
        print(f" Пропускаем анализ wheel (сложная реализация): {wheel_url}")
        return set()

    def get_test_dependencies(self, test_file_path: str) -> Set[str]:
        """
        Получение зависимостей из тестового файла (для тестового режима)

        Args:
            test_file_path: Путь к тестовому файлу

        Returns:
            Set[str]: Множество зависимостей
        """
        try:
            with open(test_file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            # В тестовом режиме предполагаем, что файл содержит имена пакетов
            # разделенные запятыми или пробелами, или одной строкой
            dependencies = set()

            if ',' in content:
                # Формат: A, B, C
                dependencies = set(pkg.strip() for pkg in content.split(','))
            elif ' ' in content:
                # Формат: A B C
                dependencies = set(content.split())
            else:
                # Один пакет в файле
                dependencies = {content}

            # Фильтруем пустые строки
            dependencies = {pkg for pkg in dependencies if pkg}

            print(f" Загружено {len(dependencies)} тестовых зависимостей из {test_file_path}")
            return dependencies

        except Exception as e:
            print(f" Ошибка загрузки тестовых зависимостей: {e}")
            return set()


# Фабричная функция для удобства
def create_dependency_fetcher(repository_url: str = "https://pypi.org/pypi") -> DependencyFetcher:
    """
    Создает экземпляр DependencyFetcher

    Args:
        repository_url: URL репозитория

    Returns:
        DependencyFetcher: Экземпляр fetcher'а
    """
    return DependencyFetcher(repository_url)