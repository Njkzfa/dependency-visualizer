# dependency_visualizer.py - Визуализация зависимостей пакета requests
import matplotlib.pyplot as plt
import networkx as nx


def create_dependency_graph():
    """Создание графа зависимостей пакета requests"""

    # Создаем ориентированный граф
    G = nx.DiGraph()

    # Основной пакет
    main_package = "requests"

    # Прямые зависимости (из нашего анализа этапа 2)
    direct_dependencies = [
        "PySocks", "certifi", "chardet",
        "charset_normalizer", "idna", "urllib3"
    ]

    # Зависимости второго уровня (упрощенные)
    second_level_dependencies = {
        "urllib3": ["brotli", "brotlicffi", "pyOpenSSL", "cryptography", "idna", "certifi"],
        "charset_normalizer": [],
        "certifi": [],
        "idna": [],
        "PySocks": [],
        "chardet": []
    }

    # Добавляем узлы и связи
    G.add_node(main_package, size=2000, color='red')

    # Прямые зависимости
    for dep in direct_dependencies:
        G.add_node(dep, size=1000, color='blue')
        G.add_edge(main_package, dep)

    # Зависимости второго уровня
    for parent, children in second_level_dependencies.items():
        for child in children:
            G.add_node(child, size=500, color='green')
            G.add_edge(parent, child)

    return G


def visualize_dependencies():
    """Визуализация графа зависимостей"""
    print("=== СОЗДАНИЕ ВИЗУАЛИЗАЦИИ ЗАВИСИМОСТЕЙ ===")

    # Создаем граф
    G = create_dependency_graph()

    # Настройки визуализации
    plt.figure(figsize=(14, 10))

    # Позиционирование узлов
    pos = nx.spring_layout(G, k=2, iterations=50)

    # Цвета узлов
    node_colors = [G.nodes[node].get('color', 'gray') for node in G.nodes()]
    node_sizes = [G.nodes[node].get('size', 300) for node in G.nodes()]

    # Рисуем граф
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20, alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

    # Настройки графика
    plt.title("ГРАФ ЗАВИСИМОСТЕЙ ПАКЕТА 'requests'", fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')

    # Легенда
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Основной пакет'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Прямые зависимости'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10,
                   label='Зависимости 2-го уровня')
    ]
    plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1))

    # Сохраняем и показываем
    plt.tight_layout()
    plt.savefig('requests_dependencies.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("Визуализация сохранена в файл: requests_dependencies.png")


def analyze_dependency_tree():
    """Анализ дерева зависимостей"""
    print("\n=== АНАЛИЗ ДЕРЕВА ЗАВИСИМОСТЕЙ ===")

    G = create_dependency_graph()

    print("ОСНОВНАЯ СТАТИСТИКА:")
    print(f"Всего пакетов: {G.number_of_nodes()}")
    print(f"Всего зависимостей: {G.number_of_edges()}")
    print(f"Прямые зависимости: 6")
    print(f"Зависимости 2-го уровня: {G.number_of_nodes() - 7}")

    print("\nУРОВНИ ЗАВИСИМОСТЕЙ:")
    print("Уровень 0: requests (основной пакет)")
    print("Уровень 1: PySocks, certifi, chardet, charset_normalizer, idna, urllib3")
    print("Уровень 2: brotli, brotlicffi, pyOpenSSL, cryptography, idna, certifi")

    print("\nНАЗНАЧЕНИЕ ОСНОВНЫХ ЗАВИСИМОСТЕЙ:")
    dependencies_info = {
        "urllib3": "HTTP-клиент низкого уровня, обработка соединений",
        "certifi": "SSL-сертификаты для безопасных соединений",
        "idna": "Поддержка международных доменных имен (IDN)",
        "charset_normalizer": "Определение кодировки текста",
        "chardet": "Определение кодировки (альтернатива)",
        "PySocks": "Поддержка SOCKS-прокси"
    }

    for dep, info in dependencies_info.items():
        print(f"- {dep}: {info}")


def export_dependency_data():
    """Экспорт данных о зависимостях в текстовый файл"""
    print("\n=== ЭКСПОРТ ДАННЫХ О ЗАВИСИМОСТЯХ ===")

    dependencies_data = {
        "package": "requests",
        "version": "2.31.0",
        "direct_dependencies": [
            "PySocks", "certifi", "chardet", "charset_normalizer", "idna", "urllib3"
        ],
        "dependency_tree": {
            "requests": {
                "PySocks": {"purpose": "SOCKS proxy support"},
                "certifi": {"purpose": "SSL certificates"},
                "chardet": {"purpose": "Character encoding detection"},
                "charset_normalizer": {"purpose": "Character encoding normalization"},
                "idna": {"purpose": "Internationalized Domain Names"},
                "urllib3": {
                    "purpose": "HTTP client library",
                    "dependencies": ["brotli", "brotlicffi", "pyOpenSSL", "cryptography", "idna", "certifi"]
                }
            }
        },
        "total_packages": 13
    }

    with open('requests_dependencies_report.txt', 'w', encoding='utf-8') as f:
        f.write("ОТЧЕТ О ЗАВИСИМОСТЯХ ПАКЕТА 'requests'\n")
        f.write("=" * 50 + "\n\n")

        f.write("ОСНОВНАЯ ИНФОРМАЦИЯ:\n")
        f.write(f"Пакет: {dependencies_data['package']}\n")
        f.write(f"Версия: {dependencies_data['version']}\n")
        f.write(f"Всего пакетов в дереве: {dependencies_data['total_packages']}\n\n")

        f.write("ПРЯМЫЕ ЗАВИСИМОСТИ:\n")
        for i, dep in enumerate(dependencies_data['direct_dependencies'], 1):
            f.write(f"{i}. {dep}\n")

        f.write("\nДЕРЕВО ЗАВИСИМОСТЕЙ:\n")
        for parent, children in dependencies_data['dependency_tree'].items():
            f.write(f"\n{parent}:\n")
            for child, info in children.items():
                f.write(f"  └── {child}: {info['purpose']}\n")
                if 'dependencies' in info:
                    for sub_dep in info['dependencies']:
                        f.write(f"      └── {sub_dep}\n")

    print("Отчет сохранен в файл: requests_dependencies_report.txt")


if __name__ == "__main__":
    visualize_dependencies()
    analyze_dependency_tree()
    export_dependency_data()