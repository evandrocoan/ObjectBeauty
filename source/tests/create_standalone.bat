
@echo off
cd ../lark-parser
python --version

python -m lark.tools.standalone ../tests/test_grammar.lark "start" > ../tests/lexer.py
pause
