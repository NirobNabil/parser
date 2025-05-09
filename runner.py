from parser.route_builder import RouteBuilder, get_root_url_file
import ast


builder = RouteBuilder()
builder.visit(ast.parse(open(get_root_url_file()).read()))
print(builder.routes)