:: 現在のディレクトリに移動
cd /d %~dp0
:: virtualenv を起動
call venv\Scripts\activate
:: Visual Studio Code を起動
:: ここから起動することで Visual Studio Code 内でデバッグ実行可能になる
code