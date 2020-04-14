from PyInstaller.utils.hooks import collect_all

# ----------------------------- ja_ginza -----------------------------
data = collect_all('ja_ginza')

datas = data[0]
binaries = data[1]
hiddenimports = data[2]
