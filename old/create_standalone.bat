
@echo off
cd lark-parser
python --version

python -m pushdown.tools.standalone ../grammars_grammar.lark "language_syntax" > ../lexer.py
pause
