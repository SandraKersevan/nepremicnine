import re
import os
import requests
import sys
import csv
import unicodedata


def shrani(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {}...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)
    with open(ime_datoteke, 'w', encoding = 'utf-8') as datoteka:
        datoteka.write(r.text)
        print('shranjeno!')


def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding = 'utf-8') as datoteka:
        vsebina = datoteka.read()
    return vsebina


def datoteke(imenik):
    '''Vrne imena vseh datotek v danem imeniku skupaj z imenom imenika.'''
    return [os.path.join(imenik, datoteka) for datoteka in os.listdir(imenik)]


def zapisi_tabelo(slovarji, imena_polj, ime_datoteke):
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)
    with open(ime_datoteke, 'w',encoding='utf-8') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

