# dependency_analyzer.py - Анализ реальных зависимостей пакетов
import subprocess
import sys
import os


class DependencyAnalyzer:
    def __init__(self):
        self.packages = ["requests", "flask", "numpy"]

    def get_package_dependencies(self, package_name):
        """Получить зависимости пакета через pip show"""
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
        except subprocess.CalledProcessError:
            print(f"Ошибка: пакет {package_name} не найден или не установлен")
            return []
        except Exception as e:
            print(f"Ошибка при получении зависимостей {package_name}: {e}")
            return []

    def analyze_all_packages(self):
        """Проанализировать все пакеты"""
        print("АНАЛИЗ РЕАЛЬНЫХ ЗАВИСИМОСТЕЙ ПАКЕТОВ")
        print("=" * 50)

        all_dependencies = {}

        for package in self.packages:
            print(f"\nАнализ пакета: {package}")

            # Прямые зависимости
            direct_deps = self.get_package_dependencies(package)
            print(f"Прямые зависимости: {direct_deps}")

            all_dependencies[package] = {
                "direct": direct_deps,
                "total": len(direct_deps)
            }

        return all_dependencies


def main():
    analyzer = DependencyAnalyzer()
    dependencies = analyzer.analyze_all_packages()
    return dependencies


if __name__ == "__main__":
    main()