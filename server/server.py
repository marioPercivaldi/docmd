#!/usr/bin/env python3
"""docmd MCP server — wraps Microsoft MarkItDown for Claude Code."""

import os
import sys
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import mcp.types as types
from markitdown import MarkItDown
import whisper

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".doc", ".pptx", ".ppt",
    ".xlsx", ".xls", ".csv",
    ".json", ".xml", ".html", ".htm",
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff",
    ".mp3", ".wav", ".m4a",
    ".zip", ".epub",
}

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a"}

server = Server("docmd")
md = MarkItDown()

_whisper_model_name = os.environ.get("DOCMD_WHISPER_MODEL", "base")
_whisper_model = whisper.load_model(_whisper_model_name)


def transcribe_with_whisper(file_path: str) -> str:
    result = _whisper_model.transcribe(file_path)
    text = result["text"].strip()
    if not text:
        return "### Audio Transcript:\n[No speech detected]"
    language = result.get("language", "unknown")
    md_content = f"**Detected language:** {language}\n\n"
    md_content += f"### Audio Transcript:\n{text}"
    return md_content


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="convert_to_markdown",
            description=(
                "Convert a file (PDF, DOCX, PPTX, XLSX, image, audio, CSV, JSON, XML, HTML, EPUB, ZIP) "
                "to Markdown. Use this instead of the Read tool for any non-plain-text file to optimize "
                "token usage. Returns the full Markdown representation of the file content."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Absolute or relative path to the file to convert.",
                    }
                },
                "required": ["file_path"],
            },
        ),
        Tool(
            name="list_supported_formats",
            description="List all file extensions supported by docmd for Markdown conversion.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "list_supported_formats":
        exts = sorted(SUPPORTED_EXTENSIONS)
        return [TextContent(type="text", text="\n".join(exts))]

    if name == "convert_to_markdown":
        file_path = arguments.get("file_path", "")
        path = Path(file_path).expanduser().resolve()

        if not path.exists():
            return [TextContent(type="text", text=f"Error: file not found: {file_path}")]

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            return [TextContent(
                type="text",
                text=(
                    f"Warning: extension '{path.suffix}' may not be supported. "
                    "Attempting conversion anyway..."
                ),
            )]

        try:
            if path.suffix.lower() in AUDIO_EXTENSIONS:
                content = transcribe_with_whisper(str(path))
            else:
                result = md.convert(str(path))
                content = result.text_content
            if not content or not content.strip():
                return [TextContent(type="text", text="(empty or unreadable content)")]
            return [TextContent(type="text", text=content)]
        except Exception as exc:
            return [TextContent(type="text", text=f"Error converting file: {exc}")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
