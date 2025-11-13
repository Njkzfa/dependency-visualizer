# main.py - Главный файл для запуска всех примеров
import basic_operations
import advanced_operations
import error_handling


def main():
    print("ЗАПУСК ПРОЕКТА АНАЛИЗА REQUESTS")
    print("=" * 60)

    while True:
        print("\nВЫБЕРИТЕ РАЗДЕЛ ДЛЯ ТЕСТИРОВАНИЯ:")
        print("1. Базовые операции (GET/POST)")
        print("2. Продвинутые операции (Сессии, заголовки)")
        print("3. Обработка ошибок")
        print("4. Анализ зависимостей (Graph)")
        print("5. ВИЗУАЛИЗАЦИЯ - Mermaid и SVG")
        print("6. Запустить ВСЕ тесты")
        print("7. Выход")

        choice = input("\nВведите номер (1-7): ").strip()

        if choice == '1':
            print("\n" + "=" * 50)
            basic_operations.test_basic_get()
            basic_operations.test_get_with_params()
            basic_operations.test_post_request()

        elif choice == '2':
            print("\n" + "=" * 50)
            advanced_operations.test_headers_and_auth()
            advanced_operations.test_session()
            advanced_operations.test_timeouts()
            advanced_operations.test_file_upload()

        elif choice == '3':
            print("\n" + "=" * 50)
            error_handling.test_error_handling()
            error_handling.test_retry_logic()

        elif choice == '4':
            print("\n" + "=" * 50)
            try:
                import dependency_visualizer
                dependency_visualizer.visualize_dependencies()
                dependency_visualizer.analyze_dependency_tree()
                dependency_visualizer.export_dependency_data()
            except ImportError as e:
                print(f"Ошибка: {e}")

        elif choice == '5':
            print("\n" + "=" * 50)
            print("ЭТАП 5: ВИЗУАЛИЗАЦИЯ ЗАВИСИМОСТЕЙ")
            print("=" * 50)

            try:
                import stage5_main
                stage5_main.main()
            except ImportError as e:
                print(f"Ошибка: {e}")
                print("Создайте файлы для этапа 5:")
                print("- dependency_analyzer.py")
                print("- mermaid_generator.py")
                print("- comparison_tool.py")
                print("- stage5_main.py")

        elif choice == '6':
            print("\n" + "=" * 50)
            print("ЗАПУСК ВСЕХ ТЕСТОВ...")
            basic_operations.test_basic_get()
            basic_operations.test_get_with_params()
            basic_operations.test_post_request()
            advanced_operations.test_headers_and_auth()
            advanced_operations.test_session()
            advanced_operations.test_timeouts()
            advanced_operations.test_file_upload()
            error_handling.test_error_handling()
            error_handling.test_retry_logic()

        elif choice == '7':
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()