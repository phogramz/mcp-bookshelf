"""
MCP BookShelf Server - Debug Version
"""

import asyncio
import sys
import json
import traceback
from typing import List, Dict, Any

def debug_log(msg: str):
    """Логирование с immediate flush"""
    print(f"[DEBUG] {msg}", file=sys.stderr, flush=True)

# Импорты с обработкой ошибок
try:
    from mcp.server import Server as MCPServer
    debug_log("✓ MCPServer imported")
except ImportError as e:
    debug_log(f"✗ MCPServer import failed: {e}")
    sys.exit(1)

try:
    from mcp.server.stdio import stdio_server
    debug_log("✓ stdio_server imported")
except ImportError as e:
    debug_log(f"✗ stdio_server import failed: {e}")
    sys.exit(1)

try:
    from mcp.server.models import InitializationOptions
    debug_log("✓ InitializationOptions imported")
except ImportError as e:
    debug_log(f"✗ InitializationOptions import failed: {e}")
    sys.exit(1)

try:
    from mcp.types import Resource, Tool, TextContent, ReadResourceResult
    debug_log("✓ MCP types imported")
except ImportError as e:
    debug_log(f"✗ MCP types import failed: {e}")
    sys.exit(1)

try:
    from pydantic import BaseModel
    debug_log("✓ Pydantic imported")
except ImportError as e:
    debug_log(f"✗ Pydantic import failed: {e}")
    sys.exit(1)


# --- Модели данных ---
class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    read: bool = False


# --- Хранилище ---
class BookStorage:
    def __init__(self):
        self.books = {
            1: Book(id=1, title="1984", author="George Orwell", genre="Dystopian", read=True),
            2: Book(id=2, title="Dune", author="Frank Herbert", genre="Sci-Fi", read=False),
        }

    def get_all_books(self):
        return list(self.books.values())


# --- Создаем сервер ---
try:
    debug_log("Создаем MCPServer...")
    mcp_server = MCPServer("bookshelf")
    debug_log("✓ MCPServer создан")
except Exception as e:
    debug_log(f"✗ Ошибка создания сервера: {e}")
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

storage = BookStorage()


# --- Ресурсы ---
@mcp_server.list_resources()
async def handle_list_resources():
    debug_log("Вызов handle_list_resources")
    return [
        Resource(
            uri="bookshelf://books",
            name="All Books",
            description="Список книг",
            mimeType="application/json"
        )
    ]


@mcp_server.read_resource()
async def handle_read_resource(uri: str):
    debug_log(f"Чтение ресурса: {uri}")
    if uri == "bookshelf://books":
        books = storage.get_all_books()
        return ReadResourceResult(
            contents=[{"type": "text", "text": json.dumps([b.dict() for b in books], indent=2)}]
        )
    raise ValueError(f"Неизвестный URI: {uri}")


# --- Инструменты ---
@mcp_server.list_tools()
async def handle_list_tools():
    debug_log("Вызов handle_list_tools")
    return [
        Tool(
            name="mark_book_as_read",
            description="Отметить книгу как прочитанную",
            inputSchema={
                "type": "object",
                "properties": {
                    "bookId": {"type": "integer", "description": "ID книги"}
                },
                "required": ["bookId"]
            }
        )
    ]


@mcp_server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]):
    debug_log(f"Вызов инструмента: {name} с аргументами: {arguments}")
    if name == "mark_book_as_read":
        return [TextContent(type="text", text="Книга отмечена как прочитанная")]
    raise ValueError(f"Неизвестный инструмент: {name}")


# --- Основная функция ---
async def main():
    debug_log("=== НАЧАЛО main() ===")

    try:
        debug_log("1. Вход в stdio_server context manager")
        async with stdio_server() as (read_stream, write_stream):
            debug_log("2. stdio_server успешно подключен")
            debug_log(f"3. read_stream: {read_stream}, write_stream: {write_stream}")

            debug_log("4. Вызов mcp_server.run()")

            await mcp_server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="bookshelf",
                    server_version="1.0.0",
                    capabilities={
                        "tools": {},
                        "resources": {},
                        "logging": None
                    }
                )
            )

            debug_log("5. mcp_server.run() завершен")

    except KeyboardInterrupt:
        debug_log("Получен KeyboardInterrupt")
    except Exception as e:
        debug_log(f"ОШИБКА в main(): {e}")
        debug_log("Полный traceback:")
        traceback.print_exc(file=sys.stderr)
        raise
    finally:
        debug_log("6. Выход из context manager")

    debug_log("=== КОНЕЦ main() ===")


if __name__ == "__main__":
    debug_log("=== ЗАПУСК СКРИПТА ===")
    debug_log(f"Python: {sys.version}")
    debug_log(f"Platform: {sys.platform}")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        debug_log("Скрипт остановлен пользователем (Ctrl+C)")
    except Exception as e:
        debug_log(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

    debug_log("=== СКРИПТ ЗАВЕРШЕН ===")