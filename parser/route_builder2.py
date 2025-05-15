import django
import types
import pdb
import re
import inspect


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


debug_f = open("debug", "w")


def debug(v):
    debug_f.write(str(v))
    debug_f.write("\n")


def get_routes(urlpatterns, prefix=""):
    routes = []
    for route in urlpatterns:
        # debug(get_route_pattern(route))

        if isinstance(route, django.urls.resolvers.URLPattern):
            try:
                routes.append(
                    (
                        join_nested_route(prefix, get_route_pattern(route)),
                        inspect.getsource(route.callback),
                    )
                )
            except:
                pdb.set_trace()

        elif isinstance(route, django.urls.resolvers.URLResolver):

            # from https://github.com/django/django/blob/0b2ed4f7c8396c8d9aa8428a40e6b25c31312889/django/urls/resolvers.py#L724
            # its guaratneed that route.url_patterns is a `urlpatterns` array. otherwise django itself will return an error
            # TODO: verify this claim further
            routes.extend(
                get_routes(route.url_patterns, prefix=get_route_pattern(route))
            )

        else:
            raise Exception("unhandled: route type not handled - ", type(route))

    # debug(routes)
    return routes
