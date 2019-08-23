from logging.config import listen

import click

from core.talk import talk


@click.command()
@click.option('--duration',
              type=float,
              prompt=click.style('Сколько минут тренируемся', fg='yellow'),
              help='Продолжительность тренировки')
@click.option('--mode',
              type=click.Choice(['1', '2', '3']),
              prompt=click.style('Режим тренировки: [1] слушать, '
                                 '[2] говорить, [3] оба', fg='yellow'))
def hello(duration, mode):
    if duration <= 0:
        return
    if mode == '1':
        listen()
    elif mode == '2':
        talk(duration)


if __name__ == '__main__':
    hello()
