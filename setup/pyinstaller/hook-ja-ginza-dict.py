from PyInstaller.utils.hooks import collect_all

# ----------------------------- ja_ginza_dict -----------------------------
data = collect_all('ja_ginza_dict')

datas = data[0]
binaries = data[1]
hiddenimports = data[2]
