import argparse
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django.setup()
from datacenter.models import Mark, Schoolkid


def fix_marks(name):
    kid = Schoolkid.objects.get(full_name__contains=name)
    bad_marks = Mark.objects.filter(schoolkid=kid, points__lt=4)
    for mark in bad_marks:
        mark.points = 5
        mark.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Скрипт позволяет связаться с базой данных'
                    'электронного журнала и изменить оценки'
    )

    parser.add_argument(
        '--name',
        default='Фролов Иван',
        help='Укажите name по типу "Фамилия Имя"'
    )

    args = parser.parse_args()

    try:
        fix_marks(args.name)
    except Schoolkid.DoesNotExist:
        print('Имя введено неправильно')
    except Schoolkid.MultipleObjectsReturned:
        print('Уточните имя')
