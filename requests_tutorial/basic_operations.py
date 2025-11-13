# basic_operations.py - Базовые операции с requests
import requests
import json


def test_basic_get():
    """Тестирование базового GET запроса"""
    print("=== БАЗОВЫЙ GET ЗАПРОС ===")

    response = requests.get('https://api.github.com')

    print(f" Статус код: {response.status_code}")
    print(f" Content-Type: {response.headers.get('content-type')}")
    print(f" Кодировка: {response.encoding}")
    print(f" Время ответа: {response.elapsed.total_seconds()} сек")

    # Показываем только часть ответа для читаемости
    if response.status_code == 200:
        data = response.json()
        print(f" GitHub API доступен! User URL: {data.get('current_user_url')}")

    print("-" * 50)


def test_get_with_params():
    """GET запрос с параметрами"""
    print("=== GET С ПАРАМЕТРАМИ ===")

    # Параметры для поиска репозиториев
    params = {
        'q': 'python requests',  # поисковый запрос
        'sort': 'stars',  # сортировка по звёздам
        'per_page': 3  # количество результатов
    }

    response = requests.get('https://api.github.com/search/repositories', params=params)

    print(f" Полный URL: {response.url}")
    print(f" Статус: {response.status_code}")

    if response.status_code == 200:
        results = response.json()
        print(f" Найдено репозиториев: {results['total_count']}")

        print(" Топ-3 репозитория:")
        for repo in results['items']:
            print(f"   - {repo['name']} ({repo['stargazers_count']} )")

    print("-" * 50)


def test_post_request():
    """Тестирование POST запроса"""
    print("=== POST ЗАПРОС ===")

    # Данные для отправки
    data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'message': 'Hello from requests!'
    }

    # Отправляем POST запрос
    response = requests.post('https://httpbin.org/post', json=data)

    print(f" Статус: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f" Отправленные данные: {json.dumps(result['json'], indent=2)}")

    print("-" * 50)


if __name__ == "__main__":
    test_basic_get()
    test_get_with_params()
    test_post_request()