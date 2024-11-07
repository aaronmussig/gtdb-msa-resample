import sys

import typer


def exit_error(message):
    typer.echo(typer.style(f'[ERROR] - {message}', fg=typer.colors.RED))
    sys.exit(1)


def info(message):
    typer.echo(typer.style(f'[INFO] - {message}', fg=typer.colors.GREEN))


def task(message):
    typer.echo(typer.style(f'[TASK] - {message}', fg=typer.colors.BLUE))


def warn(message):
    typer.echo(typer.style(f'[WARN] - {message}', fg=typer.colors.YELLOW))
