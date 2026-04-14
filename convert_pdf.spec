# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

block_cipher = None

all_datas = []
all_binaries = []
all_hiddenimports = []

# Required packages — no silent catch, fail loudly if missing
for pkg in [
    "marker",
    "surya",
    "transformers",
    "tokenizers",
    "huggingface_hub",
]:
    d, b, h = collect_all(pkg)
    all_datas += d
    all_binaries += b
    all_hiddenimports += h

# Optional packages — present depending on platform / install
for pkg in [
    "PIL",
    "cv2",
    "pydantic",
    "pydantic_core",
    "ftfy",
    "regex",
    "filetype",
]:
    try:
        d, b, h = collect_all(pkg)
        all_datas += d
        all_binaries += b
        all_hiddenimports += h
    except Exception:
        pass

a = Analysis(
    ["convert_pdf.py"],
    pathex=[],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hiddenimports + [
        # explicit marker entry points used at runtime
        "marker",
        "marker.converters",
        "marker.converters.pdf",
        "marker.models",
        "marker.output",
        "marker.config",
        "marker.config.parser",
        "marker.services",
        "marker.services.openai",
        # torch
        "torch",
        "torchvision",
        "torchaudio",
    ],
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
