
@echo off
cd ../pushdown/source/
python --version

python -m pushdown.tools.standalone ../tests/test_grammar.pushdown "start" > ../tests/lexer.py
pause
