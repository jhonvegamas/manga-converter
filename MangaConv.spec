# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "scipy", "matplotlib", "pandas", "numpy",
        "tensorflow", "torch", "keras", "sklearn",
        "cv2", "opencv-python", "sympy",
        "PyQt5", "PyQt6", "PySide2", "PySide6",
        "notebook", "jupyter", "nbformat",
        "bokeh", "plotly", "dash",
        "nltk", "spacy", "gensim",
        "scikit-image", "mahotas",
        "tqdm", "progressbar2",
    ],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MangaConv',
    icon='assets\\icon.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
