import os
import ast

from . import utils
from .visitor import DefinitionResolver
import pdb

ROOT_DIR = os.path.join("/home/twin_n/workspace/parser/Django-Projects-for-beginners/To-Do_app", "ToDo_app")

def get_root_url_file():
    settings_file = utils.find_file("settings.py", ROOT_DIR)
    if settings_file is None:
        raise Exception("settings.py not found in root directory")
    root_url_file = utils.find_name_val(open(settings_file).read(), "ROOT_URLCONF")
    if root_url_file is None:
        raise Exception("ROOT_URLCONF not found in settings.py")
    else:
        return os.path.join(ROOT_DIR, "/".join(root_url_file.split("."))+".py")  # TODO: verify if the format of root_urlconf is correct


class RouteBuilder(ast.NodeVisitor):
    def __init__(self, source=None, file=None):
        self.routes = []
        self.resolver = DefinitionResolver()
        if source:
            self.resolver.visit(ast.parse(source))
        elif file:
            self.resolver.visit(ast.parse(open(file).read()))
        else:
            self.resolver.visit(ast.parse(open(get_root_url_file()).read()))
        self.scope_stack = [""]

    def visit_Call(self, node):
        try:
            # if result[0] is an import, check if it is django.urls.path, ensuring node.func.id is django path
            func_name = utils.get_full_func_name(node.func)
            result = self.resolver.resolve(".".join(self.scope_stack), func_name)
            if result[0] == "import":
                if utils.verify_import_path(result[1], func_name, "django.urls.include"):
                    new_file_path = os.path.join(ROOT_DIR, "/".join(node.args[0].value.split("."))+".py")
                    new_builder = RouteBuilder(file=new_file_path)
                    new_builder.visit(ast.parse(open(new_file_path).read()))
                    parent_path = self.routes[-1]   # because for include to have been called, a path or re_path had been called just before
                    self.routes.pop()
                    for route in new_builder.routes:
                        self.routes.append(utils.join_nested_route(parent_path, route))

                if utils.verify_import_path(result[1], func_name, "django.urls.path"):
                    self.routes.append(node.args[0].value)  # as its made sure node is django path so its first arg will be constant
                elif utils.verify_import_path(result[1], func_name, "django.urls.re_path"):
                    self.routes.append(node.args[0].value)  # as its made sure node is django path so its first arg will be constant
                elif utils.verify_import_path(result[1], func_name, "django.urls.url"):
                    self.routes.append(node.args[0].value)  # as its made sure node is django path so its first arg will be constant

            self.generic_visit(node)
        except Exception as e:
            print(e)
            return
            

# print(ast.dump(ast.parse(open(get_root_url_file()).read()), indent=2))

# if __name__ == "__main__":
#     builder = RouteBuilder()
#     builder.visit(ast.parse(open(get_root_url_file()).read()))
#     print(builder.routes)
    