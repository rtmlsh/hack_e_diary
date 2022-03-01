import argparse
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django.setup()

from datacenter.models import Chastisement, Schoolkid


def remove_chastisements(name):
    kid = Schoolkid.objects.get(full_name__contains=name)
    сhastisements = Chastisement.objects.filter(schoolkid=kid)
    сhastisements.delete()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Скрипт позволяет связаться с базой данных'
                    'электронного журнала и удалить в нём замечания'
    )

    parser.add_argument(
        '--name',
        default='Фролов Иван',
        help='Укажите name по типу "Фамилия Имя"'
    )

    args = parser.parse_args()

    try:
        remove_chastisements(args.name)
    except Schoolkid.DoesNotExist:
        print('Имя введено неправильно')
    except Schoolkid.MultipleObjectsReturned:
        print('Уточните имя')
