import json
import os

import click

filename = 'lapat_metadata.json'


def handle_metadata(mode: str,
                    average_speed: float,
                    mistake_percentage: float) -> None:
    if os.path.exists('lapat_metadata.json'):
        with open(filename, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {
            'listen': {},
            'talk': {},
            'hybrid': {}
        }
        pass
        metadata[mode] = {
            'mistake_percentage': mistake_percentage,
            'average_speed': average_speed
        }

    if average_speed >= metadata[mode].get('average_speed', 100.0) \
            and mistake_percentage <= metadata[mode].get('mistake_percentage',
                                                         0.0):
        click.echo(
            click.style('Новый рекорд скорости!', bold=True, fg='green')
        )
        metadata[mode]['average_speed'] = average_speed
        metadata[mode]['mistake_percentage'] = mistake_percentage
        with open(filename, 'w') as f:
            json.dump(metadata, f)
