# error_handling.py - Обработка ошибок
import requests
import time


def test_error_handling():
    """Обработка различных ошибок"""
    print("=== ОБРАБОТКА ОШИБОК ===")

    # Тестируем разные сценарии
    test_urls = [
        'https://httpbin.org/status/200',  # Успех
        'https://httpbin.org/status/404',  # Не найдено
        'https://httpbin.org/status/500',  # Ошибка сервера
        'https://invalid-url-that-does-not-exist.xyz',  # Сеть недоступна
        'https://httpbin.org/delay/10',  # Долгий ответ (таймаут)
    ]

    for url in test_urls:
        print(f"\n Тестируем: {url}")

        try:
            if 'delay' in url:
                response = requests.get(url, timeout=2)
            else:
                response = requests.get(url, timeout=5)

            # Проверяем HTTP статус
            response.raise_for_status()
            print(f" УСПЕХ: {response.status_code}")

        except requests.exceptions.HTTPError as err:
            print(f" HTTP ОШИБКА: {err}")
        except requests.exceptions.ConnectionError as err:
            print(f" ОШИБКА ПОДКЛЮЧЕНИЯ: {err}")
        except requests.exceptions.Timeout as err:
            print(f" ТАЙМАУТ: {err}")
        except requests.exceptions.RequestException as err:
            print(f" ОБЩАЯ ОШИБКА: {err}")

    print("-" * 50)


def test_retry_logic():
    """Логика повторных попыток"""
    print("=== ПОВТОРНЫЕ ПОПЫТКИ ===")

    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f" Попытка {attempt + 1} из {max_retries}...")
            response = requests.get('https://httpbin.org/status/500', timeout=5)
            response.raise_for_status()
            print(" Успех!")
            break
        except requests.exceptions.HTTPError as err:
            print(f" Ошибка: {err}")
            if attempt < max_retries - 1:
                print(" Ждем 2 секунды перед повторной попыткой...")
                time.sleep(2)
            else:
                print(" Все попытки исчерпаны!")

    print("-" * 50)


if __name__ == "__main__":
    test_error_handling()
    test_retry_logic()