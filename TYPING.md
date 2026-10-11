# Базова лінія типізації (TYPING.md)

## Перший прогін (базова лінія)
- Команда: `mypy src`
- Кількість помилок: 1 помилка у 1 файлі (перевірено 7 файлів)
  - `src\booktracker\domain\parsing.py:9: error: No overload variant of "int" matches argument type "object" [call-overload]`

## Місця, де Any лишився свідомо
- `src/booktracker/sources/json_file.py`: функція `read_rows_jsonl` повертає `Iterator[dict[str, Any]]`.
  - Обґрунтування: на рівні читання сирого JSON структура полів ще невідома. Типізація та валідація гарантуються наступним шаром — моделлю `BookIn` (Pydantic).

## Підсумковий прогін (режим strict)
- Команда: `mypy src tests`
- Кількість помилок: 0 помилок у 12 файлах
- Результат: `Success: no issues found in 12 source files`

