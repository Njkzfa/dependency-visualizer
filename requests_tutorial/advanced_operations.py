# advanced_operations.py - Продвинутые операции
import requests
import time
import json


def test_headers_and_auth():
    """Работа с заголовками и авторизацией"""
    print("=== ЗАГОЛОВКИ И АВТОРИЗАЦИЯ ===")

    headers = {
        'User-Agent': 'MyLearningApp/1.0 (https://example.com)',
        'Accept': 'application/json',
        'Custom-Header': 'MyValue'
    }

    response = requests.get('https://httpbin.org/headers', headers=headers)

    print(f"Статус: {response.status_code}")

    if response.status_code == 200:
        headers_data = response.json()
        print("Полученные заголовки:")
        print(json.dumps(headers_data['headers'], indent=2))

    print("-" * 50)


def test_session():
    """Использование сессий для сохранения состояния"""
    print("=== РАБОТА С СЕССИЯМИ ===")

    # Создаем сессию
    session = requests.Session()

    # Устанавливаем общие заголовки для всех запросов в сессии
    session.headers.update({
        'User-Agent': 'MySessionApp/1.0',
        'X-Custom-Value': 'SessionDemo'
    })

    print(" Устанавливаем cookies...")
    response1 = session.get('https://httpbin.org/cookies/set/session_id/abc123')

    print(" Проверяем cookies...")
    response2 = session.get('https://httpbin.org/cookies')

    if response2.status_code == 200:
        cookies = response2.json()
        print(f" Cookies в сессии: {cookies['cookies']}")

    print("-" * 50)


def test_timeouts():
    """Тестирование таймаутов"""
    print("=== ТАЙМАУТЫ ===")

    try:
        # Этот запрос будет ждать 5 секунд, но мы установили таймаут 2 секунды
        response = requests.get('https://httpbin.org/delay/3', timeout=2)
        print(" Запрос выполнен успешно")
    except requests.exceptions.Timeout:
        print(" Запрос превысил время ожидания!")
    except requests.exceptions.RequestException as e:
        print(f" Ошибка запроса: {e}")

    print("-" * 50)


def test_file_upload():
    """Загрузка файлов"""
    print("=== ЗАГРУЗКА ФАЙЛОВ ===")

    # Создаем временный файл для демонстрации
    with open('test_file.txt', 'w') as f:
        f.write('This is a test file content for requests tutorial!')

    # Загружаем файл
    with open('test_file.txt', 'rb') as file:
        files = {'file': file}
        response = requests.post('https://httpbin.org/post', files=files)

    if response.status_code == 200:
        result = response.json()
        print(f" Файл загружен! Имя: {result['files']['file']}")

    print("-" * 50)


if __name__ == "__main__":
    test_headers_and_auth()
    test_session()
    test_timeouts()
    test_file_upload()