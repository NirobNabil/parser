import ast
import pdb
import os

def find_name_val(source, name):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id == name:
                        if isinstance(node.value, ast.Constant):
                            return node.value.value
                        else:
                            raise Exception("Unhandled edge case")
    return None


## read function body for external api cal, given fn source

## read function returns to get return values

def verify_import_path(node, name, path):
    base_path = ".".join(path.split(".")[:-1])
    expected_name = path.split(".")[-1]
    if isinstance(node, ast.Import):
        func_module_name = name.split(".")[:-1]
        for import_name_node in node.names:
            while( len(func_module_name) > 0 ):
                if import_name_node.name == ".".join(func_module_name):
                    if name == path:
                        return True
                func_module_name.pop()
    
    ## partial module not handled for importfrom
    elif isinstance(node, ast.ImportFrom):
        if expected_name != name:
            return False
        if node.module == base_path:
            for alias in node.names:
                if alias.asname:
                    if alias.asname == name and alias.name == expected_name:
                        return True
                else:
                    if alias.name == expected_name:
                        return True
    return False

def match_child(node, match_fn):
    for n in ast.walk(node):
        if match_fn(n):
            return n



def find_file(filename, search_dir):
    for root, dirs, files in os.walk(search_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None


def get_full_func_name(node):
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return get_full_func_name(node.value) + "." + node.attr
    else:
        raise Exception("Unhandled: function call type unknown")

def join_nested_route(base, route):
    if base.endswith("/"):
        base = base[:-1]
    if route.startswith("/"):
        route = route[1:]
    return base + "/" + route
                