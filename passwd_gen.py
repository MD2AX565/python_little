#!/usr/bin/python
# -*- coding: UTF-8 -*-

import string
import sys
import collections
import random
import datetime
import os

filename = 'passwords.txt'
small = string.ascii_lowercase
big = string.ascii_uppercase
spec = '!@#$%&*?^'
digits = string.digits
all_symbols = spec+digits+string.ascii_letters
parameters = sys.argv
today = str(datetime.date.today()).replace('-', '/')
Symbols = collections.namedtuple('symbols','small_symbol big_symbol spec_symbol digit')
symbols = Symbols('s=', 'b=', 'S=', 'd=')
symbols_package = {'s=':small,'b=':big,'S=':spec,'d=':digits}

if not os.path.exists(filename):
    with open(filename, 'w') as logfile:
        logfile.write('{0:<32} {1:^15} {2:^10}{3}'.format('Password','Service','Date','\n'))
        logfile.write('{0:-<32} {0:-^15} {0:-^10}{1}'.format('-','\n'))

def auto_mode(all_s, length):
    count = 0
    res = []
    while count < length:
        res.append(random.choice(all_s))
        count+=1
    password = ''.join(res)
    return password

def manual_mode(symbol, parameters, symbols_package):
    for parameter in parameters:
        if symbol in parameter:
            length = int(parameter[parameter.find('=')+1:])
            return symbols_package[symbol], length
        else:
            continue
    return symbols_package[symbol], None

def service_name(parameters):
    service_name = None
    for service in parameters:
        if 'service=' in service:
            service_name = service[service.find('=')+1:]
            break
        else:
            service_name = 'unknown'
    return service_name

def passwords_generator(today,symbols,all_symbols,filename,parameters,symbols_package):
    if len(parameters) == 1 or parameters[1] in ['-h', '--help']:
        print('''
Необходимо запустить скрипт с параметром l=[длина пароля]

Пример использования:

psswd_generator.py l=8

Настраиваемый режим: 
Генерирует явно указанные символы: 

s — английские буквы нижнего регистра
b — английские буквы верхнего регистра
d — цифры
S — спец символы

Можно использовать комбинированно:

psswd_generator.py b=3 S=2 d=2 s=1 

Будет сгенерирован пароль, длиной равной сумме всех элементов,
состоящий из явно указанного их количества.

Так-же можно указать необязательный параметр 'service',
так как по завершению выполнения работы скрипта,
пароль будет записан в файл 'passwords.txt'
в текущей директории (и это правда),
если не указываем имя сервиса для которого генерируем пароль,
по умолчанию присваивается значение 'unknown'

Фактически имя сервиса указывается для удобства,
тех к кому 'случайно' в руки попал этот файл.

psswd_generator.py b=3 S=5 service=mail.ru

Если среди параметров будет присутствовать параметр 'l'
сработает авто-режим по умолчанию, длиной указанной в 'l'
''')
        sys.exit()

    for parameter in parameters:
        if 'l=' in parameter:
            length_default = int(parameter[parameter.find('=')+1:])
            password = auto_mode(all_symbols, length_default)
            with open(filename, 'a') as logfile:
                service = service_name(parameters)
                if length_default <= 32:
                    logfile.write('{0:<32} {2:^15} {1:^10}{3}'.format(password, today, service, '\n'))
                    print('Auto mode: Password was logged to {0}'.format(filename))
                    sys.exit()
                else:
                    logfile.write('{0:.32} {2:^15} {1:^10}{3}'.format(password, today, service, '\n'))
                    print('Auto mode: Password was logged to {0}'.format(filename))
                    sys.exit()
    else:
        s = manual_mode(symbols.small_symbol, parameters, symbols_package)
        b = manual_mode(symbols.big_symbol, parameters, symbols_package)
        S = manual_mode(symbols.spec_symbol, parameters, symbols_package)
        d = manual_mode(symbols.digit, parameters, symbols_package)
        length = []
        package = [s,b,S,d]
        password = []
        for sym, true in package:
            if true:
                length.append(true)
                password_part = auto_mode(sym, true)
                password.append(password_part.replace('', ' '))
        password = ''.join(password).split()
        random.shuffle(password)
        password = ''.join(password)
        password_length = sum(length)

        with open(filename, 'a') as logfile:
            service = service_name(parameters)
            if password_length <= 32:
                logfile.write('{0:<32} {2:^15} {1:^10}{3}'.format(password, today, service, '\n'))
                print('Manual mode: Password was logged to {0}'.format(filename))
                sys.exit()
            else:
                logfile.write('{0:.32} {2:^15} {1:^10}{3}'.format(password, today, service, '\n'))
                print('Manual mode: Password was logged to {0}'.format(filename))
                sys.exit()


passwords_generator(today,symbols,all_symbols,filename,parameters,symbols_package)
