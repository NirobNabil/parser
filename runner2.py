import subprocess

subprocess.run(
    [
        "python",
        "/home/twin_n/workspace/parser/django-realworld-example-app/manage.py",
        "shell",
        '--command=exec(open("/home/twin_n/workspace/parser/parser/command_script.py").read())',
    ]
)
