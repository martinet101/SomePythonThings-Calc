# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['SomePythonThings Calc.py'],
             pathex=['/Users/marticlilop/SPTPrograms/Calc with PyQt5 (desktop version)'],
             binaries=[],
             datas=[('./icon.png', './')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='SomePythonThings Calc',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='macOSicon.icns')
app = BUNDLE(exe,
             name='SomePythonThings Calc.app',
             icon='./macOSicon.icns',
             bundle_identifier=None)
