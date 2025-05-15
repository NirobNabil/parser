import route_builder2 as rb
import os


routes = rb.get_routes(urlpatterns)
with open("routes.txt", "w") as f:
    for r in routes:
        f.write(r[0] + "\n")
        # f.write(r[1] + "\n\n\n")
