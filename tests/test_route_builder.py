from parser.route_builder import RouteBuilder
import ast

def test_func_import_with_import_from():
    code = """
from django.urls import path
path("route")
    """
    builder = RouteBuilder(source=code)
    builder.visit(ast.parse(code))
    assert builder.routes == ["route"]

def test_module_import():
    code = """
import django.urls
django.urls.path("route")
    """
    builder = RouteBuilder(source=code)
    builder.visit(ast.parse(code))
    assert builder.routes == ["route"]

def test_module_import2():
    code = """
import django
django.urls.path("route")
    """
    builder = RouteBuilder(source=code)
    builder.visit(ast.parse(code))
    assert builder.routes == ["route"]

def test_module_import2_re_path():
    code = """
import django
django.urls.re_path("route", view)
    """
    builder = RouteBuilder(source=code)
    builder.visit(ast.parse(code))  
    assert builder.routes == ["route"]

def test_module_import2_url():
    code = """
import django
django.urls.url("route", view)
    """
    builder = RouteBuilder(source=code)
    builder.visit(ast.parse(code))
    assert builder.routes == ["route"]

def test_func_name_reassign():
    code = """
from django.urls import path
p = path
p("route")
    """
    builder = RouteBuilder(source=code)
    builder.visit(ast.parse(code))
    assert builder.routes == ["route"]


