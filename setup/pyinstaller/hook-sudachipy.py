from PyInstaller.utils.hooks import collect_all

# ----------------------------- SudachiPy -----------------------------
data = collect_all('sudachipy')

datas = data[0]
binaries = data[1]
hiddenimports = data[2]
