import django
import types
import pdb
import re


def get_route_pattern(route):
    def handle_nested_type(pattern):
        # pdb.set_trace()
        if isinstance(pattern, str):
            return pattern
        elif isinstance(pattern, re.Pattern):
            return pattern.pattern
        elif isinstance(pattern, django.urls.resolvers.RegexPattern):
            return handle_nested_type(pattern.regex)
        elif isinstance(pattern, django.urls.resolvers.URLPattern):
            return handle_nested_type(pattern.pattern)
        elif isinstance(pattern, django.urls.resolvers.RoutePattern):
            return handle_nested_type(pattern.regex)
        else:
            pdb.set_trace()
            raise Exception(
                "unhandled: route pattern type not handled - ",
                type(pattern),
            )

    return handle_nested_type(route.pattern)


def join_nested_route(base, route):
    if base.endswith("/"):
        base = base[:-1]
    if route.startswith("/"):
        route = route[1:]
    return base + "/" + route


def merge_nested_routes(base_route, nested_routes):
    routes = []
    for n_route in nested_routes:
        routes.append(join_nested_route(base_route, n_route))
    return routes


def get_routes(urlpatterns):
    routes = []
    for route in urlpatterns:

        if isinstance(route, django.urls.resolvers.URLPattern):
            routes.append(get_route_pattern(route))

        elif isinstance(route, django.urls.resolvers.URLResolver):

            if isinstance(route.urlconf_name, list):
                routes.extend(
                    merge_nested_routes(
                        get_route_pattern(route), get_routes(route.urlconf_name)
                    )
                )

            elif isinstance(route.urlconf_name, types.ModuleType):
                if route.urlconf_name.urlpatterns != None:
                    routes.extend(
                        merge_nested_routes(
                            get_route_pattern(route),
                            get_routes(route.urlconf_name.urlpatterns),
                        )
                    )
                else:
                    raise Exception("unhandled: urlconf_name has no urlpattern")

            else:
                raise Exception(
                    "unhandled: route.urlconf_name type not handled - ",
                    type(route.urlconf_name),
                )

        else:
            raise Exception("unhandled: route type not handled - ", type(route))

    return routes
