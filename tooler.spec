# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('Tesseract-OCR', 'Tesseract-OCR')],  # Include Tesseract
    hiddenimports=[
        'core.auto_clicker',
        'core.image_converter',
        'core.speed_tester',
        'core.translator',
        'core.video_converter',
        'core.youtube_downloader',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # Exclude unused large libraries to reduce size and startup time
    excludes=[
        'matplotlib', 
        'scipy', 
        'pandas', 
        'numpy.random',
        'PIL.ImageQt',
        'IPython',
        'notebook',
        'test',
        'tkinter.test',
        'unittest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove unnecessary binary files to reduce size
excluded_binaries = [
    'VCRUNTIME140.dll',
    'ucrtbase.dll',
    'api-ms-win-core-*.dll',
    'api-ms-win-crt-*.dll',
]

a.binaries = TOC([x for x in a.binaries if not any(pattern in x[0] for pattern in excluded_binaries)])

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Tooler',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression for faster loading
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Tooler',
)
