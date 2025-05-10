import subprocess

subprocess.run(
    [
        "python",
        "/home/twin_n/workspace/parser/Django-Projects-for-beginners/To-Do_app/ToDo_app/manage.py",
        "shell",
        '--command=exec(open("/home/twin_n/workspace/parser/parser/command_script.py").read())',
    ]
)
