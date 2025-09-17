# -*- mode: python ; coding: utf-8 -*-

from __future__ import annotations

from pathlib import Path

block_cipher = None

SPEC_DIR = Path(SPECPATH).resolve()
PROJECT_ROOT = SPEC_DIR.parents[1]
CLIENT_MAIN = PROJECT_ROOT / "client" / "main.py"
CONFIG_DIR = PROJECT_ROOT / "config"


a = Analysis(
    [str(CLIENT_MAIN)],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=[(str(CONFIG_DIR), "config")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="shamash-client",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
