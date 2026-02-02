# -*- mode: python ; coding: utf-8 -*-
def filter_binaries(binaries):
    """更精确的DLL过滤"""
    filtered = []
    java_keywords = ['java', 'jre', 'jdk']
    excluded_dlls = ['api-ms-win', 'ext-ms-win']  # Windows 10+需要这些
    
    for name, path, typecode in binaries:
        path_lower = path.lower()
        
        # 保留Python相关的DLL
        if 'python' in path_lower and 'scripts' not in path_lower:
            filtered.append((name, path, typecode))
            continue
            
        # 过滤Java DLL
        if any(keyword in path_lower for keyword in java_keywords):
            continue
            
        # 保留必要的系统DLL
        if any(dll in path_lower for dll in excluded_dlls):
            continue
            
        filtered.append((name, path, typecode))
    
    return filtered
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('./assets', './assets'), ('./packages/pywebwinui3/web', './packages/pywebwinui3/web'), ('./xaml', './xaml')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'tkinter', 'tcl', 'tk', 'wxPython', 'wx', 'matplotlib', 'seaborn', 'matplotlib', 'seaborn', 'numpy', 'pandas', 'scipy', 'PIL', 'pillow', 'pip', 'wheel', 'flask', 'django', 'jinja2', 'sqlite3', 'sqlalchemy', 'markupsafe', 'twisted', 'tornado', 'Crypto', 'Cipher', 'packaging', 'pkg_resources', 'setuptools', 'cryptography', 'venv', 'test', 'fastapi', 'rq', 'py_compile'],
    noarchive=False,
    optimize=1,
)
a.binaries = filter_binaries(a.binaries)
pyz = PYZ(
    a.pure,
    optimize=2,
    compression=0,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='HertaLauncher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\icon.ico'],
)
