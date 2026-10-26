"""Ієрархія винятків застосунку: один корінь, кілька конкретних нащадків."""


class BookTrackerError(Exception):
    """Базовий виняток застосунку."""


class SourceError(BookTrackerError):
    """Проблема з джерелом даних: файл, мережа, формат."""


class ParseError(SourceError):
    """Запис не вдалося розібрати."""


class ConfigError(BookTrackerError):
    """Некоректна конфігурація застосунку."""
