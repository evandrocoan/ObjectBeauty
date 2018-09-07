
@echo off
cd lark-parser
python --version

python -m lark.tools.standalone ../gramatica_compiladores.lark "language_syntax" > ../lexer.py
pause
