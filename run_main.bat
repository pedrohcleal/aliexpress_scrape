@echo off
REM Define a cor do terminal para verde
color 0a

REM Ativa o ambiente virtual
call venv\Scripts\activate

REM Executa o script Python
python main.py

REM Permite que o usuário pressione Ctrl+C para interromper o script
REM O `Ctrl+C` é tratado nativamente pelo Python, então nenhum tratamento adicional é necessário.
echo Pressione Ctrl+C para interromper a execução.

REM Sai do ambiente virtual
deactivate
