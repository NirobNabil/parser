import sys

sys.path.insert(0, "/home/twin_n/workspace/parser")
exec(
    open(
        "/home/twin_n/workspace/parser/Django-Projects-for-beginners/To-Do_app/ToDo_app/ToDo_app/urls.py"
    ).read()
)
exec(open("/home/twin_n/workspace/parser/parser/route_builder2.py").read())
routes = get_routes(urlpatterns)
with open("routes.txt", "w") as f:
    for r in routes:
        f.write(r + "\n")
