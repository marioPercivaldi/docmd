# docmd

**Claude Code plugin** that converts file attachments to Markdown before Claude processes them, optimizing token usage by 40–80%.

Powered by [Microsoft MarkItDown](https://github.com/microsoft/markitdown).

## What it does

When you share a PDF, Word document, spreadsheet, presentation, image, or audio file with Claude, docmd automatically converts it to clean, structured Markdown — so Claude reads efficient text instead of attempting to process raw binary content.

## Supported formats

| Category | Formats |
|---|---|
| Documents | PDF, DOCX, DOC, PPTX, PPT |
| Spreadsheets | XLSX, XLS, CSV |
| Data | JSON, XML, HTML |
| Images | JPEG, PNG, GIF, WEBP, BMP, TIFF |
| Audio | MP3, WAV, M4A |
| Archives | ZIP, EPUB |

## Installation

```shell
/plugin install docmd@claude-community
```

> Requires Claude Code v2.0+. Python 3.8+ must be available on your system. Dependencies (`markitdown`, `mcp`) are installed automatically in a local virtual environment on first use.

## How it works

docmd has three layers:

### 1. MCP Server
A local Python server wrapping MarkItDown exposes two tools to Claude:
- `docmd__convert_to_markdown(file_path)` — converts any supported file to Markdown
- `docmd__list_supported_formats()` — lists supported extensions

### 2. Skill (`/docmd:convert`)
Instructs Claude to call `docmd__convert_to_markdown` whenever a supported file is referenced, before reading or analyzing it.

### 3. PreToolUse Hook
Automatically intercepts `Read` tool calls on supported file types and returns Markdown, blocking the raw binary read. Zero manual intervention needed.

## Usage

Simply reference any supported file in your prompt:

```
Analyze the attached report.pdf and summarize the key findings.
```

```
What does this spreadsheet data.xlsx contain?
```

```
Summarize the presentation deck.pptx
```

docmd handles the conversion transparently.

You can also invoke the skill directly:

```
/docmd:convert path/to/document.pdf
```

## Local development & testing

```bash
git clone https://github.com/mariopercivaldi/docmd
cd docmd
claude --plugin-dir .
```

Inside the session, test with:
```
/docmd:convert path/to/any/file.pdf
```

## Submitting to marketplace

Run validation before submitting:
```bash
claude plugin validate --plugin-dir .
```

Then submit at: https://claude.ai/settings/plugins/submit

## Configuration

The MCP server installs its Python dependencies in `.venv/` inside the plugin directory on first launch. No manual setup required.

## License

MIT — see [LICENSE](./LICENSE)
