---
name: convert
description: Convert file attachments (PDF, DOCX, PPTX, XLSX, images, audio, CSV, JSON, XML, HTML, EPUB, ZIP) to optimized Markdown to reduce token usage. Use whenever the user provides or references a file that is not plain text, or when asked to read/analyze a document, spreadsheet, presentation, or image.
---

# docmd:convert

When the user provides a file path or attaches a file that is not plain text, convert it to Markdown before processing.

## Supported formats

PDF, DOCX, DOC, PPTX, PPT, XLSX, XLS, CSV, JSON, XML, HTML, JPEG, JPG, PNG, GIF, WEBP, BMP, TIFF, MP3, WAV, M4A, ZIP, EPUB

## How to use

1. Identify the file path the user wants to process
2. Call `docmd__convert_to_markdown` with that path
3. Use the returned Markdown content for analysis — do NOT read the original file afterward
4. If the user asks you to read/open/analyze a file in a supported format, always prefer this conversion first

## Example trigger phrases

- "analyze this PDF"
- "read the attached document"
- "summarize this spreadsheet"
- "what's in this presentation"
- "process this file: path/to/file.docx"

## Token optimization rationale

Raw binary files passed to the Read tool either fail or consume tokens inefficiently. MarkItDown converts them to clean, structured Markdown that preserves headings, tables, lists, and key content while minimizing token consumption by 40–80% compared to alternative extraction approaches.

## Using the MCP tool directly

```
docmd__convert_to_markdown(file_path="/absolute/or/relative/path/to/file.pdf")
```

Returns a string with the full Markdown representation of the file content.

To check supported formats programmatically:

```
docmd__list_supported_formats()
```
