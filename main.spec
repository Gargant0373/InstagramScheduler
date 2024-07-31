# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

# Define paths
src_dir = 'src'
data_dir = 'data'
icon_file = 'ig.ico'

# Define the main script
main_script = os.path.join(src_dir, 'main.py')

# List of additional data files to include
datas = [(data_dir, 'data')]

# PyInstaller Analysis
a = Analysis(
    [main_script],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=None,
    noarchive=False,
)

# Create a bundled executable
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='instagram_scheduler',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True if you need a console window
    icon=icon_file,
    disable_windowed_traceback=False,
    argv_emulation=False,
)

# Collect everything into the final bundle
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='instagram_scheduler'
)
