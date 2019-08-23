import math
import random
from time import time

import click

from core.mappings import LISTEN_LETTERS, LISTEN_DIGITS_EN, LISTEN_DIGITS_RU, \
    TALK_DIGITS_EN, TALK_DIGITS_RU
from core.metadata import handle_metadata

SPEED_THRESHOLD = 5.0


def is_correct(letter_codeword: str, number_codewords: str,
               answer: str) -> bool:
    answer = answer.strip().replace(' ', '-')

    letter = answer[0]
    number = answer[1:]
    number_codewords = number_codewords.strip().replace(' ', '-').split('-')

    letter_matched = False
    if LISTEN_LETTERS[letter_codeword] == letter:
        letter_matched = True

    for digits_set in LISTEN_DIGITS_EN, LISTEN_DIGITS_RU:
        digits_matched = 0
        for i, digit in enumerate(number):
            if digits_set.get(number_codewords[i]) == digit:
                digits_matched += 1
        if digits_matched:
            break

    return letter_matched and len(number_codewords) == digits_matched


def suggest(letter_codeword: str, number_codewords: str) -> str:
    letter = LISTEN_LETTERS[letter_codeword]
    digits_set = LISTEN_DIGITS_EN
    digits_set.update(LISTEN_DIGITS_RU)
    number = ''
    for codeword in number_codewords.strip().replace(' ', '-').split('-'):
        digit = digits_set[codeword]
        number += digit
    return f'{letter}{number}'


def listen(max_duration: float) -> None:
    duration = 0.0
    results = []
    speeds = []
    while duration <= max_duration * 60.0:
        start = time()

        random_letter_codeword = random.choice(list(LISTEN_LETTERS.keys()))
        random_number = str(random.randint(1, 26))
        digits_set = random.choice([TALK_DIGITS_EN, TALK_DIGITS_RU])
        random_number_codewords = [random.choice(digits_set[digit])
                                   for digit in random_number]
        random_number_codewords = ' '.join(random_number_codewords)

        click.echo(
            click.style(f'{random_letter_codeword} {random_number_codewords}',
                        bold=True)
        )

        answer = click.prompt(click.style('>>', fg='yellow'), prompt_suffix='')

        end = time()
        speed = end - start
        duration += speed

        if speed > SPEED_THRESHOLD:
            click.echo(click.style(f'Ошибка! Слишком медленно.',
                                   fg='red'))
            results.append(False)
        elif is_correct(random_letter_codeword, random_number_codewords,
                        answer):
            click.echo(click.style('Верно.', fg='green'))
            results.append(True)
            speeds.append(speed)
        else:
            suggestion = suggest(random_letter_codeword,
                                 random_number_codewords)
            click.echo(click.style(f'Ошибка! '
                                   f'Пример правильного ответа:\n'
                                   f'{suggestion}', fg='red'))
            results.append(False)

        left = max_duration - duration / 60.0
        minutes = math.floor(left)
        seconds = int((left - minutes) * 60.0)

        if len(str(minutes)) < 2:
            minutes = f'0{minutes}'

        if len(str(seconds)) < 2:
            seconds = f'0{seconds}'

        left_readable = f'{minutes}:{seconds}'
        click.echo(f'{left_readable} ..')

    click.echo(click.style('=' * 50, bold=True))
    click.echo(click.style('Время истекло.', bold=True))
    click.echo(click.style('Результаты:', bold=True))
    mistake_percentage = round(
        (results.count(False) / len(results)) * 100.0, 2
    )
    if mistake_percentage:
        click.echo(click.style(f'Уровень ошибок: '
                               f'{mistake_percentage}%',
                               bold=True, fg='red'))
    else:
        click.echo(click.style('Без ошибок!', bold=True, fg='green'))

    if speeds:
        average_speed = sum(speeds) / len(speeds)
    else:
        average_speed = 0.0
    click.echo(click.style(f'Средняя скорость: {round(average_speed, 2)}',
                           bold=True))

    handle_metadata('listen', average_speed, mistake_percentage)
