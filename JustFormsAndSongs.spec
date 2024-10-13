# JustFormsAndSongs.spec
block_cipher = None

a = Analysis(
    ['core.pyw'],  # Entry point of your application
    pathex=['.'],  # Path to search for source files
    binaries=[],
    datas=[
        # Include your vanilla content (modify as necessary)
        ('C:/Users/alecn/OneDrive/Escritorio/Just Forms and Songs/vanilla', 'vanillas'),
        ('C:/Users/alecn/OneDrive/Escritorio/Just Forms and Songs/modules', 'modules'),
    ],
    hiddenimports=[
        # List any hidden imports here
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['venv', '.vscode', 'uidata'],  # Exclude these folders
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='JustFormsAndSongs',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True if you want to see console output
    manifest=None,
    onefile=True  # Add this line to create a single executable
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='JustFormsAndSongs',
)
