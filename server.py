"""
MCP BookShelf Server - MVP v0.1
"""
import asyncio
import json
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Resource, ReadResourceResult

# 1. Создаём сервер
server = Server("bookshelf")

# 2. Ресурс: список книг в JSON
@server.list_resources()
async def list_resources():
    return [Resource(
        uri="bookshelf://books",
        name="My Books",
        description="Список моих книг",
        mimeType="application/json"
    )]

# 3. Чтение ресурса (возвращаем JSON)
@server.read_resource()
async def read_resource(uri: str):
    if uri == "bookshelf://books":
        books = [
            {"id": 1, "title": "1984", "author": "George Orwell", "read": True},
            {"id": 2, "title": "Dune", "author": "Frank Herbert", "read": False}
        ]
        return ReadResourceResult(
            contents=[{"type": "text", "text": json.dumps(books, indent=2)}]
        )
    raise ValueError(f"Unknown URI: {uri}")

# 4. Запуск
async def main():
    print("MCP Server starting...", file=sys.stderr)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="bookshelf",
                server_version="1.0.0",
                capabilities={}  # Пустой словарь
            )
        )

if __name__ == "__main__":
    asyncio.run(main())