# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['program.py'],
             pathex=['C:\\Users\\Admin\\Documents\\ITM Prov\\Proyecto Grado Ing\\HearthDiseaseProject'],
             binaries=[],
             datas=[('data/heart.csv', 'data'),
                    ('docs/PDF_Base.pdf', 'docs'),
                    ('font/Raleway-Medium.ttf', 'font'),
                    ('font/Raleway-Regular.ttf', 'font'),
                    ('img/heart-1.png', 'img'),
                    ('img/medicine-logo.png', 'img')
                    ('img/icon.ico, 'img')
                    ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
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
          name='program',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='icon.ico')
