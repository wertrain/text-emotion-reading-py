from PyInstaller.utils.hooks import collect_all

# ----------------------------- mlask -----------------------------
data = collect_all('mlask')

datas = data[0]
binaries = data[1]
hiddenimports = data[2]
