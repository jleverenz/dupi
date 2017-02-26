# invoke tasks

from invoke import task

@task
def test(ctx):
    ctx.run("python -m unittest discover tests/", pty=True)
    ctx.run("pep8 dupi/ tests/", pty=True)

@task
def coverage(ctx):
    ctx.run("coverage run --source dupi setup.py test", pty=True)
    ctx.run("coverage report -m", pty=True)
