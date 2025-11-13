# mermaid_generator.py - Генерация Mermaid диаграмм из реальных данных
from dependency_analyzer import DependencyAnalyzer


class MermaidGenerator:
    def __init__(self):
        self.analyzer = DependencyAnalyzer()

    def generate_mermaid_diagram(self, package_name, dependencies_data):
        """Сгенерировать Mermaid код для пакета"""
        direct_deps = dependencies_data["direct"]

        mermaid_code = f"flowchart TD\n"

        # Основной пакет
        mermaid_code += f"    A[{package_name}\\nОСНОВНОЙ ПАКЕТ]\n"

        # Прямые зависимости
        for i, dep in enumerate(direct_deps, 1):
            mermaid_code += f"    A --> B{i}[{dep}\\nПРЯМАЯ ЗАВИСИМОСТЬ]\n"

        return mermaid_code

    def save_mermaid_file(self, package_name, mermaid_code):
        """Сохранить Mermaid код в файл"""
        filename = f"{package_name}_dependencies.mmd"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        print(f"Mermaid файл сохранен: {filename}")
        return filename

    def generate_visualizations(self):
        """Сгенерировать визуализации для всех пакетов"""
        print("ГЕНЕРАЦИЯ ВИЗУАЛИЗАЦИЙ ЗАВИСИМОСТЕЙ")
        print("=" * 50)

        dependencies = self.analyzer.analyze_all_packages()
        results = {}

        for package, data in dependencies.items():
            print(f"\nОбработка пакета: {package}")

            # Генерация Mermaid
            mermaid_code = self.generate_mermaid_diagram(package, data)

            # Вывод Mermaid кода
            print("Mermaid код:")
            print(mermaid_code)

            # Сохранение Mermaid
            mmd_file = self.save_mermaid_file(package, mermaid_code)

            results[package] = {
                "mermaid_file": mmd_file,
                "mermaid_code": mermaid_code,
                "direct_dependencies": data["direct"],
                "total_dependencies": len(data["direct"])
            }

        return results


def main():
    generator = MermaidGenerator()
    results = generator.generate_visualizations()

    print(f"\nРЕЗУЛЬТАТЫ:")
    print("=" * 50)
    for package, data in results.items():
        print(f"{package}:")
        print(f"  Mermaid файл: {data['mermaid_file']}")
        print(f"  Зависимостей: {data['total_dependencies']}")


if __name__ == "__main__":
    main()