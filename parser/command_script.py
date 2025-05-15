import sys
import os

# add parser package to PYTHONPATH
sys.path.insert(0, "/home/twin_n/workspace/parser/parser")

ROOT_URLCONF = (
    "/home/twin_n/workspace/parser/django-realworld-example-app/conduit/urls.py"
)
PROJECT_DIR = os.getcwd()

# execute ROOT_URLCONF so that it's urlpatterns is visible
exec(open(ROOT_URLCONF).read())
exec(open("/home/twin_n/workspace/parser/parser/main.py").read())
