# MCP BookShelf Server

MCP (Model Context Protocol) сервер для управления коллекцией книг.

## Возможности

### Ресурсы (Resources)
- `bookshelf://books` — список всех книг
- `bookshelf://books/{id}` — детали конкретной книги

### Инструменты (Tools)
- `mark_book_as_read` — отметить книгу как прочитанную
- `add_new_book` — добавить новую книгу

## Использование с Claude Desktop

1. Добавьте в `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "bookshelf": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}