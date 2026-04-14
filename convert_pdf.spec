# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

all_datas = []
all_binaries = []
all_hiddenimports = []


def collect(pkg):
    """Collect data/binaries/hiddenimports + ALL submodules. Fails loudly."""
    d, b, h = collect_all(pkg)
    all_datas.extend(d)
    all_binaries.extend(b)
    all_hiddenimports.extend(h)
    all_hiddenimports.extend(collect_submodules(pkg))


def try_collect(pkg):
    """Same as collect() but silently skips if the package is not installed."""
    try:
        collect(pkg)
    except Exception:
        pass


# ── Required packages ────────────────────────────────────────────────────────
for pkg in [
    "marker",
    "surya",
    "transformers",
    "tokenizers",
    "huggingface_hub",
    "PIL",
    "pydantic",
    "pydantic_settings",
    "openai",
    "pdftext",
    "pypdfium2",
    "markdownify",
    "markdown2",
    "filetype",
    "ftfy",
    "regex",
    "rapidfuzz",
    "tqdm",
    "click",
    "sklearn",
    "cv2",
    "dotenv",
]:
    collect(pkg)

# ── Optional packages ─────────────────────────────────────────────────────────
for pkg in [
    "mammoth",
    "openpyxl",
    "pptx",
    "ebooklib",
    "weasyprint",
    "anthropic",
    "google.genai",
    "torch",
    "torchvision",
    "torchaudio",
]:
    try_collect(pkg)


a = Analysis(
    ["convert_pdf.py"],
    pathex=[],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "matplotlib",
        "notebook",
        "ipython",
        "IPython",
        "jupyter",
        "pytest",
        "setuptools",
        "pkg_resources",
        "distutils",
        "tkinter",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="convert_pdf",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
