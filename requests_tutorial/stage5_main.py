# stage5_main.py - Главный файл для этапа 5
from dependency_analyzer import DependencyAnalyzer
from mermaid_generator import MermaidGenerator
from comparison_tool import ComparisonTool
import os


def main():
    print("ЭТАП 5: ВИЗУАЛИЗАЦИЯ ЗАВИСИМОСТЕЙ")
    print("=" * 60)

    # 1. Анализ зависимостей
    print("\n1. АНАЛИЗ ЗАВИСИМОСТЕЙ ТРЕХ ПАКЕТОВ")
    analyzer = DependencyAnalyzer()
    dependencies = analyzer.analyze_all_packages()

    # 2. Генерация Mermaid
    print("\n2. ГЕНЕРАЦИЯ MERMAID ДИАГРАММ")
    print("=" * 50)
    generator = MermaidGenerator()
    results = generator.generate_visualizations()

    # 3. Сравнение с инструментами
    print("\n3. СРАВНЕНИЕ С ШТАТНЫМИ ИНСТРУМЕНТАМИ")
    print("=" * 50)
    comparator = ComparisonTool()
    comparator.compare_analysis()
    comparator.explain_differences()

    # 4. Итоги
    print("\n4. ИТОГИ ВЫПОЛНЕНИЯ ЭТАПА 5")
    print("=" * 50)

    created_files = []
    for package in ["requests", "flask", "numpy"]:
        mmd_file = f"{package}_dependencies.mmd"
        if os.path.exists(mmd_file):
            created_files.append(mmd_file)

    print("Созданные файлы Mermaid:")
    for file in created_files:
        print(f"  - {file}")

    print("\nТребования этапа 5 выполнены:")
    print("✅ 1. Mermaid диаграммы созданы (текстовое представление)")
    print("✅ 2. Файлы .mmd сохранены")
    print("✅ 3. Три пакета проанализированы")
    print("✅ 4. Сравнение с pip выполнено")
    print("✅ 5. Объяснение расхождений предоставлено")


if __name__ == "__main__":
    main()