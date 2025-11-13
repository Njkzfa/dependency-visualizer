# comparison_tool.py - Сравнение с штатными инструментами
import subprocess
import sys
from dependency_analyzer import DependencyAnalyzer


class ComparisonTool:
    def __init__(self):
        self.packages = ["requests", "flask", "numpy"]
        self.analyzer = DependencyAnalyzer()

    def run_pip_show(self, package_name):
        """Запустить pip show и извлечь зависимости"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", package_name],
                capture_output=True, text=True, check=True
            )

            dependencies = []
            for line in result.stdout.split('\n'):
                if line.startswith('Requires:'):
                    deps = line.replace('Requires:', '').strip()
                    if deps:
                        dependencies = [dep.strip() for dep in deps.split(',')]
                    break

            return dependencies
        except Exception as e:
            return f"Ошибка: {e}"

    def compare_analysis(self):
        """Сравнить наш анализ с pip show"""
        print("СРАВНЕНИЕ НАШЕГО АНАЛИЗА С PIP SHOW")
        print("=" * 50)

        for package in self.packages:
            print(f"\nПАКЕТ: {package}")
            print("-" * 30)

            # Наш анализ
            our_deps = self.analyzer.get_package_dependencies(package)
            print(f"Наш анализ: {our_deps}")
            print(f"Количество: {len(our_deps)}")

            # Pip show
            pip_deps = self.run_pip_show(package)
            if isinstance(pip_deps, list):
                print(f"Pip show: {pip_deps}")
                print(f"Количество: {len(pip_deps)}")

                # Сравнение
                our_set = set(our_deps)
                pip_set = set(pip_deps)

                if our_set == pip_set:
                    print("РЕЗУЛЬТАТ: Совпадение")
                else:
                    print("РЕЗУЛЬТАТ: Расхождение")
                    if our_set - pip_set:
                        print(f"  Только в нашем анализе: {list(our_set - pip_set)}")
                    if pip_set - our_set:
                        print(f"  Только в pip show: {list(pip_set - our_set)}")
            else:
                print(f"Pip show: {pip_deps}")

    def explain_differences(self):
        """Объяснить возможные расхождения"""
        print(f"\nОБЪЯСНЕНИЕ ВОЗМОЖНЫХ РАСХОЖДЕНИЙ:")
        print("=" * 50)
        print("1. ВРЕМЯ ВЫПОЛНЕНИЯ АНАЛИЗА:")
        print("   - pip show работает с установленными пакетами")
        print("   - Наш анализ может использовать кэшированные данные")
        print("")
        print("2. ВЕРСИИ ПАКЕТОВ:")
        print("   - Разные версии имеют разные зависимости")
        print("   - Могли установиться обновленные версии")
        print("")
        print("3. ОКРУЖЕНИЕ:")
        print("   - Зависимости могут различаться в разных ОС")
        print("   - Наличие компиляторов влияет на зависимости")


def main():
    tool = ComparisonTool()
    tool.compare_analysis()
    tool.explain_differences()


if __name__ == "__main__":
    main()