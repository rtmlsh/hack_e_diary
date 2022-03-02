import argparse
import os
import random

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django.setup()

from datacenter.models import Commendation, Lesson, Schoolkid, Subject


def check_lessons(year_of_study, subject_title):
    subjects = Subject.objects.filter(year_of_study=year_of_study)
    titles = [subject.title for subject in subjects]
    if subject_title not in titles:
        raise Exception('Неправильно введено название предмета')


def create_commendation(name, subject_title, year_of_study,
                        group_letter, compliment):
    check_lessons(year_of_study, subject_title)
    kid = Schoolkid.objects.get(full_name__contains=name)
    subject = Subject.objects.filter(
        title=subject_title,
        year_of_study=year_of_study
    ).first()
    lesson = Lesson.objects.filter(
        subject=subject,
        year_of_study=year_of_study,
        group_letter=group_letter
    ).order_by('-date').first()
    recomendation = Commendation.objects.create(
        schoolkid=kid,
        subject=subject,
        teacher=lesson.teacher,
        created=lesson.date,
        text=compliment
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Скрипт позволяет связаться с базой данных'
                    'электронного журнала и добавить в него похвалу от учителя'
    )

    parser.add_argument(
        '--name',
        default='Фролов Иван',
        help='Укажите name по типу "Фамилия Имя"'
    )

    parser.add_argument(
        '--subject_title',
        default='Музыка',
        help='Укажите название предмета'
    )

    parser.add_argument(
        '--year_of_study',
        type=int,
        default=6,
        help='Укажите год обучения'
    )

    parser.add_argument(
        '--group_letter',
        default='А',
        help='Укажите букву класса'
    )

    args = parser.parse_args()
    compliments = ['Молодец!', 'Приятно удивил!', 'Великолепно ответил!',
                   'Очень хороший ответ!', 'Сегодня прыгнул выше головы!',
                   'Я поражен!', 'С каждым разом у тебя получается всё лучше!',
                   'Хорошая работа']

    compliment = random.choice(compliments)

    try:
        create_commendation(
            args.name,
            args.subject_title,
            args.year_of_study,
            args.group_letter,
            compliment
        )
    except Schoolkid.DoesNotExist:
        print('Имя введено неправильно')
    except Schoolkid.MultipleObjectsReturned:
        print('Уточните имя')
