import json
import math
import os
import random
from time import time

import click

from core.mappings import TALK_LETTERS, TALK_DIGITS_RU, TALK_DIGITS_EN

SPEED_THRESHOLD = 7.0


def is_correct(letter: str, number: str, answer: str) -> bool:
    answer = answer.strip().replace(' ', '-')

    try:
        answer_letter_codeword, \
        answer_number_codewords = [w.lower() for w in
                                   answer.split('-', 1)]
    except ValueError:
        return False

    answer_number_codewords = answer_number_codewords.split('-')

    letter_matched = False
    for codeword in TALK_LETTERS[letter]:
        if answer_letter_codeword == codeword:
            letter_matched = True

    for digits_set in TALK_DIGITS_EN, TALK_DIGITS_RU:
        digits_matched = 0

        for i, answer_number_codeword in enumerate(answer_number_codewords):
            digit = number[i]
            for codeword in digits_set[digit]:
                if answer_number_codeword == codeword:
                    digits_matched += 1

        if digits_matched:
            break

    return letter_matched and len(number) == digits_matched


def suggest(letter: str, number: str) -> str:
    digits_set = random.choice([TALK_DIGITS_EN, TALK_DIGITS_RU])
    letter_suggestion = random.choice(TALK_LETTERS[letter])

    number_suggestion = ''
    for digit in number:
        digit_suggestion = random.choice(digits_set[digit])
        number_suggestion += f'-{digit_suggestion}'
    return f'{letter_suggestion}{number_suggestion}'


def talk(max_duration: float) -> None:
    duration = 0.0
    results = []
    speeds = []
    while duration <= max_duration * 60.0:
        start = time()
        random_letter = random.choice(list(TALK_LETTERS.keys()))
        random_number = str(random.randint(1, 26))

        click.echo(click.style(f'{random_letter}{random_number}', bold=True))

        answer = click.prompt(click.style('>>', fg='yellow'), prompt_suffix='')

        end = time()
        speed = end - start
        duration += speed

        if speed > SPEED_THRESHOLD:
            click.echo(click.style(f'Ошибка! Слишком медленно.',
                                   fg='red'))
            results.append(False)
        elif is_correct(random_letter, random_number, answer):
            click.echo(click.style('Верно.', fg='green'))
            results.append(True)
            speeds.append(speed)
        else:
            suggestion = suggest(random_letter, random_number)
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

    if os.path.exists('lapat_metadata.json'):
        with open('lapat_metadata.json', 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {
            'record': {
                'mistake_percentage': mistake_percentage,
                'average_speed': average_speed
            }
        }

    if average_speed >= metadata['record']['average_speed'] \
            and mistake_percentage <= metadata['record']['mistake_percentage']:
        click.echo(
            click.style('Новый рекорд скорости!', bold=True, fg='green')
        )
        metadata['record']['average_speed'] = average_speed
        metadata['record']['mistake_percentage'] = mistake_percentage
        with open('lapat_metadata.json', 'w') as f:
            json.dump(metadata, f)
