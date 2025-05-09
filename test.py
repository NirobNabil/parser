from ntpath import isfile
import astor
from search import search, search_source
import ast
import xml.etree.ElementTree as ET
from xml.dom import minidom
from linecache import getline
import os
import pdb 

_filename = "gg.py"
root_dir = "c:\\kognito\\krait\\djangotut"
# _s = open(_filename).read()
# print(astor.dump_tree(ast.parse(_s)))

def get_line(filename, line_number):
    with open(filename, 'r') as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number == line_number:
                return line.rstrip()

def get_arg(node):
    args = []
    for arg in node.args:
        if isinstance(arg, ast.Constant):  # For string or numeric literals
            args.append(arg.value)
        elif isinstance(arg, ast.Name):  # For variable references
            args.append(arg.id)
        else:
            args.append(arg)  # Fallback for more complex expressions
    return args

def get_func_params(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            args = get_arg(node)
            return args


def get_module_method_params(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            args = get_arg(node)
            return args

def follow_include_path(path):
    path = "/".join(path.split(".")) + ".py"
    path = os.path.join(root_dir, path)
    print(path)
    if not os.path.isfile(path):
        raise Exception("include url path not found")
    
    return get_routes(path)  

def join_nested_route(base, route):
    if base.endswith("/"):
        base = base[:-1]
    if route.startswith("/"):
        route = route[1:]
    return base + "/" + route

func_xpaths = [
    ".//Call/func/Name[@id='path']",
    ".//Call/func/Name[@id='re_path']",
    ".//Call/func/Name[@id='url']",
]

module_method_xpaths = [
    ".//Call/func/Attribute[@attr='get']/value/Name[@id='client']",     # client.get()  -  internal api call
    ".//Call/func/Attribute[@attr='get']/value/Name[@id='requests']",   # requests.get()  -  external api call
]

def get_routes(filename):
    all_routes = []
    
    for n in search(filename, " | ".join(func_xpaths), recurse=False, print_xml=False):
        line = get_line(n[0], n[1]).strip()
        node = ast.parse(line)
        params = get_func_params(node)
        if params[0] == "^old-way/$":
            pdb.set_trace()

        #### handle include in url definition
        if( 
           isinstance(params[1], ast.Call) and
           isinstance(params[1].func, ast.Name) and
           params[1].func.id == 'include'    # TODO: make sure this include is the django include  
        ):
            if isinstance(params[1].args[0], ast.Constant):
                routes = [join_nested_route(params[0], route) for route in follow_include_path(params[1].args[0].value)]
                all_routes.extend(routes)
                continue
            else:
                raise Exception("Unhandled edge case")
                
        route = params[0]
        all_routes.append(route)
    
    
    
    for n in search(filename, " | ".join(module_method_xpaths), recurse=False, print_xml=False):
        line = get_line(n[0], n[1]).strip()
        params = get_module_method_params(ast.parse(line))
        route = params[0]
        all_routes.append(route)
    
    return all_routes


print(get_routes(_filename))