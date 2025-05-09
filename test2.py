import astor
import ast

_filename = "gg2.py"
root_dir = "c:\\kognito\\krait\\djangotut"
_s = open(_filename).read()
print(astor.dump_tree(ast.parse(_s)))
