from PyInstaller.utils.hooks import collect_all

# ----------------------------- ginza -----------------------------
data = collect_all('ginza')

datas = data[0]
binaries = data[1]
hiddenimports = data[2]
