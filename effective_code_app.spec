# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['effective_code_app.py'],
    pathex=['C:\\Shuang\\MyPython\\effective_code_app\\venv64\\Lib\\site-packages\\', 'C:\\Shuang\\MyPython\\effective_code_app\\venv64\\'],
    binaries=[],
    datas=[],
    hiddenimports=[],  # 'matplotlib', 'numpy'
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='effective_code_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # pokud nastavim na False, antivirus breci ze je to vir
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='effective_code_app',
)
