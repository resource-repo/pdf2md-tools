# pdf2md-tools

Convert PDF files to Markdown using [marker-pdf](https://github.com/the-loki/marker/tree/v1.10.2-fix) with LLM enhancement.

## Features

- LLM-enhanced conversion via any OpenAI-compatible API
- Tables rendered as HTML inside Markdown for better fidelity
- Images extracted and saved alongside the output file
- HuggingFace model downloads routed through `hf-mirror.com` by default

## Download

Pre-built single-file binaries are available on the [Releases](../../releases) page.

| File | Platform |
|------|----------|
| `convert_pdf-windows.exe` | Windows x86_64 |
| `convert_pdf-macos-arm64` | macOS Apple Silicon |
| `convert_pdf-macos-x86_64` | macOS Intel |
| `convert_pdf-linux` | Linux x86_64 |

On macOS/Linux, make the binary executable after download:

```bash
chmod +x convert_pdf-macos-arm64
```

> **Note:** ML models (~2 GB) are downloaded from HuggingFace on first run and cached in `~/.cache/marker`.

## Usage

```bash
convert_pdf <input.pdf> --openai_api_key <key> [options]
```

### Options

| Argument | Env var | Default | Description |
|----------|---------|---------|-------------|
| `--openai_api_key` | `OPENAI_API_KEY` | — | API key (**required**) |
| `--openai_base_url` | `OPENAI_BASE_URL` | `https://api.openai.com/v1` | OpenAI-compatible endpoint |
| `--openai_model` | `OPENAI_MODEL` | `gpt-4o-mini` | Model name |
| `--output_dir` | — | Same directory as input | Output directory |

### Examples

```bash
# Minimal — reads key from environment variable
export OPENAI_API_KEY=sk-xxx
./convert_pdf document.pdf

# Custom endpoint (e.g. local vLLM / one-api)
./convert_pdf document.pdf \
  --openai_api_key sk-xxx \
  --openai_base_url http://localhost:8080/v1 \
  --openai_model qwen2.5-72b-instruct

# Write output to a specific directory
./convert_pdf document.pdf --openai_api_key sk-xxx --output_dir ./output
```

### Output

| File | Description |
|------|-------------|
| `<stem>.md` | Converted Markdown |
| `<stem>/` | Extracted images (if any) |

### HuggingFace mirror

The default mirror is `https://hf-mirror.com`. Override with the `HF_ENDPOINT` environment variable:

```bash
export HF_ENDPOINT=https://huggingface.co
./convert_pdf document.pdf --openai_api_key sk-xxx
```

## Build from source

**Requirements:** Python 3.10+

```bash
pip install -r requirements.txt
pip install "pyinstaller>=6.0"
pyinstaller convert_pdf.spec
# output: dist/convert_pdf  (or dist/convert_pdf.exe on Windows)
```

Alternatively, push a version tag to trigger the GitHub Actions release workflow:

```bash
git tag v1.0.0
git push origin v1.0.0
```
