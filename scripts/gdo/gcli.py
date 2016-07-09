#! /usr/bin/env python -u
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys

import click

logger = logging.getLogger(__name__)

# Define a default machine name global. First use DO_MACHINE_NAME, then
# DOCKER_MACHINE_NAME (defined by eval $(docker-machine env ...)), finally
# default to 'eventboard'.
DEFAULT_MACHINE_NAME = os.environ.get('DO_MACHINE_NAME')
if not DEFAULT_MACHINE_NAME:
    DEFAULT_MACHINE_NAME = os.environ.get('DOCKER_MACHINE_NAME', 'eventboard')

# use to allow -h for for help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def get_container_id(name):
    logger.debug('get_container_id for {}'.format(name))

    name_id = _run_command('docker-compose ps -q {}'.format(name))
    logger.debug('get_container_id found {}'.format(name_id))

    name_id = name_id.strip()

    if '\n' in name_id:
        name_id = name_id.split('\n')[-1]

    return name_id.strip()


def set_logging(ctx, param, level):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise click.BadParameter('Invalid log level: {}'.format(level))

    logging.basicConfig(level=numeric_level)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--log',
    default='ERROR', help='Set the log level',
    expose_value=False,
    callback=set_logging,
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']))
@click.version_option('1.0.0')
@click.pass_context
def cli(ctx):
    pass


@cli.command()
def reload():
    """Restart all containers"""
    _run_command('docker-compose stop')
    _run_command('docker-compose up -d')


@cli.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('ARGS', nargs=-1, type=click.UNPROCESSED)
def test(args):
    """Run tests"""
    args = ('--settings=eventboard.settings.testpg', ) + args

    web_id = get_container_id('web')

    _run_command(
        'docker exec -it {} /vagrant/runtests {}'.format(
            web_id, ' '.join(args)),
        interactive=True)


@cli.command()
@click.argument('CONTAINER', default='garage', type=click.STRING, nargs=1)
def bash(container):
    """Start a bash shell on CONTAINER. Default: web"""
    container_id = get_container_id(container)

    _run_command(
        'docker exec -it {} /bin/sh --login'.format(container_id),
        interactive=True)


@cli.command()
def shell():
    """Start the Django shell on the web container"""
    web_id = get_container_id('garage')

    _run_command(
        'docker exec -it {} ipython'.format(web_id),
        interactive=True)


@cli.command()
def psql():
    """Start the postgres shell on the db container"""
    db_id = get_container_id('db')

    _run_command(
        'docker exec -it {} psql -U eb -d eb'.format(db_id),
        interactive=True)


@cli.command()
def debug():
    """Start an interactive runserver for debugging"""
    _run_command(
        'docker-compose stop web')
    _run_command(
        'docker-compose run web python manage.py runserver 0.0.0.0:8503',
        interactive=True)
    _run_command(
        'docker-compose start web')


def _run_command(cmd, interactive=False, use_docker_env=True,
                 unbuffered_print=False):
    """
    Executes a given shell command

    Args:
        cmd (str): The command to execute
        interact (bool): If True hand the controlling terminal over to the
            subprocess. Useful when user input is needed for the command
        use_docker_env (bool): Prefix the commands with the output of
            ``docker-machine env <machine name>``.

    Returns:
        str: Output of the command
    """
    logger.debug(cmd)

    if interactive:
        try:
            import pexpect
        except ImportError:
            sys.stderr.write('Missing pexpect requirement. pip install '
                             'pexpect')
            sys.exit(1)
        sys.stdout.write('Running interactive command...\n')

        cmd = cmd.split(' ')
        pexpect.spawn(cmd[0], list(cmd[1:])).interact()
    else:
        import subprocess

        try:
            p = subprocess.Popen(
                cmd.strip(),
                shell=True,
                bufsize=0,
                stdout=subprocess.PIPE,
                stderr=sys.stderr,
            )

            if unbuffered_print:
                while p.poll() is None:
                    for l in p.stdout.readline():
                        click.echo(l, nl=False)
            else:
                p.wait()
                return p.stdout.read()

        except subprocess.CalledProcessError:
            sys.exit(1)

if __name__ == '__main__':
    cli()
