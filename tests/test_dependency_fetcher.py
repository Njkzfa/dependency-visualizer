"""Тесты для модуля dependency_fetcher"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Добавляем src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.dependency_fetcher import DependencyFetcher


class TestDependencyFetcher(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.fetcher = DependencyFetcher()

    def test_extract_package_name(self):
        """Тест извлечения чистого имени пакета"""
        test_cases = [
            ("requests>=2.25.0", "requests"),
            ("numpy", "numpy"),
            ("pandas[test]", "pandas"),
            ("matplotlib ; python_version > '3.6'", "matplotlib"),
            ("django>=3.0,<4.0", "django"),
            ("", ""),
        ]

        for requirement, expected in test_cases:
            with self.subTest(requirement=requirement):
                result = self.fetcher._extract_package_name(requirement)
                self.assertEqual(result, expected)

    @patch('src.dependency_fetcher.requests.Session.get')
    def test_get_package_info_success(self, mock_get):
        """Тест успешного получения информации о пакете"""
        # Мокаем успешный ответ
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'info': {
                'name': 'requests',
                'version': '2.25.1'
            }
        }
        mock_get.return_value = mock_response

        result = self.fetcher._get_package_info('requests')

        self.assertIsNotNone(result)
        self.assertEqual(result['info']['name'], 'requests')
        mock_get.assert_called_once()

    @patch('src.dependency_fetcher.requests.Session.get')
    def test_get_package_info_not_found(self, mock_get):
        """Тест случая когда пакет не найден"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.fetcher._get_package_info('nonexistent-package')

        self.assertIsNone(result)

    def test_parse_requires_dist(self):
        """Тест парсинга requires_dist"""
        requires_dist = [
            "urllib3>=1.21.1",
            "chardet>=3.0.2,<5",
            "idna>=2.5,<3",
            "certifi>=2017.4.17"
        ]

        result = self.fetcher._parse_requires_dist(requires_dist)

        expected = {"urllib3", "chardet", "idna", "certifi"}
        self.assertEqual(result, expected)

    def test_get_test_dependencies(self):
        """Тест загрузки тестовых зависимостей"""
        # Создаем временный тестовый файл
        test_content = "numpy, pandas, matplotlib"
        test_file = "test_temp_deps.txt"

        with open(test_file, 'w') as f:
            f.write(test_content)

        try:
            result = self.fetcher.get_test_dependencies(test_file)
            expected = {"numpy", "pandas", "matplotlib"}
            self.assertEqual(result, expected)
        finally:
            # Убираем временный файл
            if os.path.exists(test_file):
                os.remove(test_file)


if __name__ == '__main__':
    unittest.main()