import random

import click

from core.mappings import TALK_LETTERS, TALK_DIGITS_RU, TALK_DIGITS_EN


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


def talk():
    while True:
        random_letter = random.choice(list(TALK_LETTERS.keys()))
        random_number = str(random.randint(1, 26))

        click.echo(click.style(f'{random_letter}{random_number}', bold=True))

        answer = click.prompt(click.style('>>', fg='yellow'), prompt_suffix='')

        if is_correct(random_letter, random_number, answer):
            click.echo(click.style('Верно.', fg='green'))
        else:
            suggestion = suggest(random_letter, random_number)
            click.echo(click.style(f'Неверно! '
                                   f'Пример как правильно:\n'
                                   f'{suggestion}', fg='red'))
