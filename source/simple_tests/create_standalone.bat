
@echo off
cd ../pushdown/source/
python --version

python -m pushdown.tools.standalone ../tests/test_grammar.lark "start" > ../tests/lexer.py
pause
