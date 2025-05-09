import ast
from . import utils
import pdb

class DefinitionResolver(ast.NodeVisitor):
    def __init__(self):
        self.assignments = {'': {}}   # name -> Assign node
        self.functions = {'': {}}     # name -> FunctionDef node
        self.imports = {'': {}}       # name -> Import/ImportFrom node
        self.scope_stack = [""]

    def visit_FunctionDef(self, node):
        self.functions[".".join(self.scope_stack)][node.name] = node
        self.scope_stack.append(node.name)
        self.functions[".".join(self.scope_stack)] = {}
        self.generic_visit(node)

    def visit_Return(self, node):
        self.scope_stack.pop()
        self.generic_visit(node)

    def visit_Assign(self, node):
        for i, target in enumerate(node.targets):
            if isinstance(target, ast.Tuple):
                if target.elts is None:
                    raise Exception("Unhandled: multiple variable assignment target tuple no elts")
                for j, t in enumerate(target.elts):
                    if isinstance(t, ast.Name):
                        if node.value.elts is None:
                            raise Exception("Unhandled: multiple variable assignment value tuple no elts")
                        self.assignments[".".join(self.scope_stack)][t.id] = node.value.elts[j]
            if isinstance(target, ast.Name):
                self.assignments[".".join(self.scope_stack)][target.id] = node.value
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        if isinstance(node.target, ast.Name):
            self.assignments[".".join(self.scope_stack)][node.target.id] = node
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports[self.scope_stack[-1]][alias.asname or alias.name] = node

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports[self.scope_stack[-1]][alias.asname or alias.name] = node

    def resolve(self, scope, name):
        scope = scope.split(".")
        while( len(scope) > 0 ):
            cur_scope = ".".join(scope)
            if name in self.functions[cur_scope]:
                return ("function", self.functions[cur_scope][name])
            elif name in self.assignments[cur_scope]:
                if isinstance(self.assignments[cur_scope][name], ast.Name):
                    return self.resolve(cur_scope, self.assignments[cur_scope][name].id)
                elif isinstance(self.assignments[cur_scope][name], ast.Constant):
                    return ("variable", self.assignments[cur_scope][name].value)
                else:
                    raise Exception("Unhandled: assignment to name not name or constant")
            elif name in self.imports[cur_scope]:
                return ("import", self.imports[cur_scope][name])
            else:

                ## handle nested import function call like django.urls.path
                name_path = name.split(".")[:-1]   #-1 because you cannot import a func, you always import a module
                while( len(name_path) > 0 ):
                    if ".".join(name_path) in self.imports[cur_scope] and isinstance(self.imports[cur_scope][".".join(name_path)], ast.Import):
                        return ("import", self.imports[cur_scope][".".join(name_path)])
                    # pdb.set_trace()
                    name_path.pop()
            scope.pop()
        
        raise Exception("Name not found")

# --- Usage example ---
# code = '''
# import math
# from os.gg.xx import path as osp
# from os.gg.x import path

# def foo(x):
#     return x + 1

# bar = foo
# baz = bar(5)
# '''

# tree = ast.parse(code)
# print(ast.dump(tree, indent=2))
# # resolver = DefinitionResolver()
# # resolver.visit(tree)

# # Simulate encountering a name
# name = 'path'
# #result = resolver.resolve(name)
# import pdb
# pdb.set_trace()
# if result:
#     kind, node = result
#     print(f"{name} is a {kind} defined at line {node.lineno}")
# else:
#     print(f"{name} is not defined in this file.")
