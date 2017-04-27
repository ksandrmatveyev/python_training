#! /usr/bin/env python
import argparse


def create_new_user(args):
    """Эта функция будет вызвана для создания пользователя"""
    # скучные проверки корректности данных, с ними разберемся позже
    age = int(args.age)
    print("{name} {age}".format(name=args.username, age=args.age))


def get_args():
    """Настройка argparse"""
    parser = argparse.ArgumentParser(description='User database utility')
    subparsers = parser.add_subparsers()
    parser_append = subparsers.add_parser('append', help='Append a new user to database')
    parser_append.add_argument('username', help='Name of user')
    parser_append.add_argument('age', help='Age of user')
    parser_append.set_defaults(func=create_new_user)

    # код для других аргументов

    return parser.parse_args()


def main():
    """Это все, что нам потребуется для обработки всех ветвей аргументов"""
    args = get_args()
    args.func(args)

if __name__ == '__main__':
    main()