"""
PDF 转 Markdown 转换脚本
使用 marker-pdf 库: https://github.com/the-loki/marker/tree/v1.10.2-fix

安装依赖:
    pip install git+https://github.com/the-loki/marker.git@v1.10.2-fix

用法:
    python convert_pdf.py input.pdf --openai_api_key sk-xxx
    python convert_pdf.py input.pdf --openai_api_key sk-xxx --openai_base_url http://localhost:8080/v1 --openai_model qwen2.5-72b

环境变量（可替代命令行参数）:
    OPENAI_API_KEY    API 密钥
    OPENAI_BASE_URL   Base URL
    OPENAI_MODEL      模型名称
    HF_ENDPOINT       HuggingFace 镜像地址（默认: https://hf-mirror.com）
"""

import os
import sys

# Inject environment variables before any library imports so that
# huggingface_hub and torch pick them up during their own initialization.
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

import argparse
from pathlib import Path

DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"


def parse_args():
    parser = argparse.ArgumentParser(
        description="将 PDF 文件转换为 Markdown（LLM 增强 + HTML 表格）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("input", help="输入 PDF 文件路径")
    parser.add_argument("--output_dir", default=None, help="输出目录（默认与输入文件同目录）")
    parser.add_argument(
        "--openai_api_key",
        default=os.environ.get("OPENAI_API_KEY"),
        help="API 密钥（也可通过 OPENAI_API_KEY 环境变量设置）",
    )
    parser.add_argument(
        "--openai_base_url",
        default=os.environ.get("OPENAI_BASE_URL", DEFAULT_OPENAI_BASE_URL),
        help=f"Base URL（默认: {DEFAULT_OPENAI_BASE_URL}，也可通过 OPENAI_BASE_URL 环境变量设置）",
    )
    parser.add_argument(
        "--openai_model",
        default=os.environ.get("OPENAI_MODEL", DEFAULT_OPENAI_MODEL),
        help=f"模型名称（默认: {DEFAULT_OPENAI_MODEL}，也可通过 OPENAI_MODEL 环境变量设置）",
    )
    args = parser.parse_args()

    missing = []
    if not args.openai_api_key:
        missing.append("--openai_api_key (or OPENAI_API_KEY env var)")
    if not args.openai_base_url:
        missing.append("--openai_base_url (or OPENAI_BASE_URL env var)")
    if not args.openai_model:
        missing.append("--openai_model (or OPENAI_MODEL env var)")
    if missing:
        parser.error("the following LLM settings are required:\n  " + "\n  ".join(missing))

    return args


def convert(args) -> None:
    try:
        from marker.converters.pdf import PdfConverter
        from marker.models import create_model_dict
        from marker.output import text_from_rendered
        from marker.config.parser import ConfigParser
    except ImportError:
        print(
            "Error: failed to import marker.\n"
            "Install it with: pip install git+https://github.com/the-loki/marker.git@v1.10.2-fix",
            file=sys.stderr,
        )
        sys.exit(1)

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir) if args.output_dir else input_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    config = {
        "output_format": "markdown",
        "html_tables_in_markdown": True,
        "use_llm": True,
        "llm_service": "marker.services.openai.OpenAIService",
        "openai_api_key": args.openai_api_key,
        "openai_base_url": args.openai_base_url,
        "openai_model": args.openai_model,
    }

    print(f"Converting: {input_path}")
    print(f"  model: {args.openai_model}  base_url: {args.openai_base_url}")

    config_parser = ConfigParser(config)
    converter = PdfConverter(
        config=config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
        processor_list=config_parser.get_processors(),
        renderer=config_parser.get_renderer(),
        llm_service=config_parser.get_llm_service(),
    )

    rendered = converter(str(input_path))
    text, _, images = text_from_rendered(rendered)

    output_file = output_dir / (input_path.stem + ".md")
    output_file.write_text(text, encoding="utf-8")

    if images:
        images_dir = output_dir / input_path.stem
        images_dir.mkdir(exist_ok=True)
        for img_name, img_data in images.items():
            (images_dir / img_name).write_bytes(img_data)
        print(f"Images saved to: {images_dir} ({len(images)} files)")

    print(f"Done: {output_file}")


def main():
    args = parse_args()
    convert(args)


if __name__ == "__main__":
    main()
