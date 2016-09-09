import os
from invoke import task

HERE = os.path.dirname(os.path.abspath(__file__))
API = os.path.join(HERE, 'meetings')


@task
def test_all(ctx):
    flake(ctx)
    test_api(ctx)
    ember_test(ctx)
    jshint(ctx)


# PYTHON
@task(aliases=['flake8'])
def flake(ctx, echo=True):
    ctx.run('flake8 {}'.format(API), echo=echo)


@task
def api_server(ctx):
    ctx.run('python {}/manage.py runserver'.format(API), echo=True)


@task
def test_api(ctx):
    ctx.run(
        'python {}/manage.py test {}'.format(API, API), echo=True, pty=True)


@task(aliases=['req'])
def requirements(ctx):
    ctx.run('pip install -r requirements.txt', echo=True)


# EMBER
@task
def npm_install(ctx):
    ctx.run('npm install', echo=True, pty=True)


@task
def bower_install(ctx):
    ctx.run('bower install', echo=True)


@task
def assets(ctx):
    npm_install(ctx)
    bower_install(ctx)


@task
def ember_server(ctx, environment='local'):
    ctx.run('ember server --environment={}'.format(environment),
            echo=True, pty=True)


@task
def ember_test(ctx):
    ctx.run('ember test', echo=True, pty=True)


@task
def jshint(ctx):
    ctx.run('jshint {}/app'.format(HERE), echo=True)
