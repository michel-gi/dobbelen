# -*- coding: utf-8 -*-
# Dit bestand bevat de metadata voor de Windows executable.
# PyInstaller gebruikt dit om de 'Details' tab in de bestandseigenschappen te vullen.
 
# Definieer dummy classes om linters (zoals in VS Code) tevreden te stellen.
# PyInstaller zelf leest dit bestand als tekst en heeft deze classes niet nodig;
# het herkent de `VSVersionInfo` structuur op basis van de naam.
class VSVersionInfo:
    def __init__(self, ffi, kids): pass
class FixedFileInfo:
    def __init__(self, **kwargs): pass
class StringFileInfo:
    def __init__(self, kids): pass
class StringTable:
    def __init__(self, name, kids): pass
class StringStruct:
    def __init__(self, name, value): pass
class VarFileInfo:
    def __init__(self, kids): pass
class VarStruct:
    def __init__(self, name, kids): pass

VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers: (Major, Minor, Patch, Build)
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    # Set flags and OS
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo([StringTable(u'040904B0', [ # Language ID: U.S. English, Character Set: Unicode
        StringStruct(u'CompanyName', u'Michel Gieskens'),
        StringStruct(u'FileDescription', u'Een programma om dobbelsteenworpen te simuleren'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'InternalName', u'DobbelSim'),
        StringStruct(u'LegalCopyright', u'© 2024 Michel Gieskens. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'dobbelsteen_simulatie.exe'),
        StringStruct(u'ProductName', u'Dobbelsteen Simulatie'),
        StringStruct(u'ProductVersion', u'1.0.0')])]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])]) # 1033: U.S. English, 1200: Unicode
  ]
)