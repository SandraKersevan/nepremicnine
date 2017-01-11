import re
import orodja
import csv
import requests



def zajemi_bezigrad():
    vzorec = 'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/ljubljana-bezigrad/stanovanje/{0}/'
    for i in range(1,13):
        url = vzorec.format(i)
        r = requests.get(url)
        ime_datoteke = 'zajeta-bezigradP/{0}.html'.format(i)
        orodja.shrani(url, ime_datoteke)
        
def zajemi_center():
    vzorec = 'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/ljubljana-center/stanovanje/{0}/'
    for i in range(1,9):
        url = vzorec.format(i)
        r = requests.get(url)
        ime_datoteke = 'zajeta-centerP/{0}.html'.format(i)
        orodja.shrani(url, ime_datoteke)

def zajemi_moste_polje():
    vzorec = 'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/ljubljana-moste-polje/stanovanje/{0}/'
    for i in range(1,5):
        url = vzorec.format(i)
        r = requests.get(url)
        ime_datoteke = 'zajeta-moste-poljeP/{0}.html'.format(i)
        orodja.shrani(url, ime_datoteke)

def zajemi_siska():
    vzorec = 'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/ljubljana-siska/stanovanje/{0}/'
    for i in range(1,9):
        url = vzorec.format(i)
        r = requests.get(url)
        ime_datoteke = 'zajeta-siskaP/{0}.html'.format(i)
        orodja.shrani(url, ime_datoteke)

def zajemi_vic_rudnik():
    vzorec = 'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/ljubljana-moste-polje,ljubljana-siska/stanovanje/{0}/'
    for i in range(1,6):
        url = vzorec.format(i)
        r = requests.get(url)
        ime_datoteke = 'zajeta-vic-rudnikP/{0}.html'.format(i)
        orodja.shrani(url, ime_datoteke)

def pocisti_niz(niz):
    a = list(niz)
    i = 0
    while i < len(a):
        if a[i] == ' ':
            del a[i]
        if a[i] == '.':
            del a[i]
        if a[i] == ' ':
            del a[i]
        if a[i] == ',':
            a[i] = '.'
            i += 1
        else: i += 1
    return ''.join(a)

def pocisti_stanovanje(stanovanje, podrocje):
    podatki = stanovanje.groupdict()
    podatki['id'] = int(podatki['id'])
    podatki['ime'] = str(podatki['ime'])
    podatki['nadstropje'] = str(podatki['nadstropje'])
    podatki['leto'] = int(podatki['leto'])
    podatki['velikost'] = float(pocisti_niz(podatki['velikost']))
    podatki['cena'] = float(pocisti_niz(podatki['cena']))
    podatki['podrocje'] = podrocje
    podatki['posredovanje'] = str(podatki['posredovanje'])
    podatki['tip1'] = str(podatki['tip1'])
    return podatki

def pocisti_tip(tip):
    podatki = tip.groupdict()
    podatki['id'] = int(podatki['id'])
    podatki['tip'] = str(podatki['tip'])
    return podatki

def pripravi():
    regex_stanovanja = re.compile(
        r'<span class="posr">(?P<posredovanje>.*?): (?P<tip1>.*?)</?span.*?>.*?'
        r'<h2><a href=".*?" title="(?P<id>\d*)">.*?<span class="title">(?P<ime>.*?)</span></a></h2>.*?'
        r'<span class="atribut">Nadstropje: <strong>(?P<nadstropje>.*?)</strong>.*?'
        r'</span><span class="atribut">Leto: <strong>(?P<leto>\d{4})</strong></span>.*?'
        r'.*?<span class="velikost">(?P<velikost>\d*,?\d*) m2</span><br />.*?'
        r'<span class="cena">(?P<cena>.*?)\s*?&euro;.*?',
        flags=re.DOTALL
    )
    regex_tipa = re.compile(
        r'<h2><a href=".*?" title="(?P<id>\d*)">.*?'
        r'<div class="kratek">.*?m2, (?P<tip>.*?), .*?<\/div>',
        flags=re.DOTALL
    )
    
    stanovanja = []
    bezigrad = []
    center = []
    mostePolje = []
    siska = []
    vicRudnik = []
    tipi = []
    
    for html_datoteka in orodja.datoteke('zajeta-bezigradP/'):
        print(html_datoteka)
        for stanovanje in re.finditer(regex_stanovanja, orodja.vsebina_datoteke(html_datoteka)):
            podrocje = 'Bezigrad'
            stanovanja.append(pocisti_stanovanje(stanovanje, podrocje))
            bezigrad.append(pocisti_stanovanje(stanovanje, podrocje))
        orodja.zapisi_tabelo(bezigrad, ['id', 'ime', 'podrocje', 'nadstropje', 'leto', 'velikost', 'cena', 'posredovanje', 'tip1'],
                             'csv-datotekeP/bezigrad.csv')
        for tip in re.finditer(regex_tipa, orodja.vsebina_datoteke(html_datoteka)):
            tipi.append(pocisti_tip(tip))
        
    for html_datoteka in orodja.datoteke('zajeta-centerP/'):
        print(html_datoteka)
        for stanovanje in re.finditer(regex_stanovanja, orodja.vsebina_datoteke(html_datoteka)):
            podrocje = 'Center'
            stanovanja.append(pocisti_stanovanje(stanovanje, podrocje))
            center.append(pocisti_stanovanje(stanovanje, podrocje))
        orodja.zapisi_tabelo(center, ['id', 'ime', 'podrocje', 'nadstropje', 'leto', 'velikost', 'cena', 'posredovanje', 'tip1'],
                             'csv-datotekeP/center.csv')
        for tip in re.finditer(regex_tipa, orodja.vsebina_datoteke(html_datoteka)):
            tipi.append(pocisti_tip(tip))
            
    for html_datoteka in orodja.datoteke('zajeta-moste-poljeP/'):
        print(html_datoteka)
        for stanovanje in re.finditer(regex_stanovanja, orodja.vsebina_datoteke(html_datoteka)):
            podrocje = 'Moste-Polje'
            stanovanja.append(pocisti_stanovanje(stanovanje, podrocje))
            mostePolje.append(pocisti_stanovanje(stanovanje, podrocje))
        orodja.zapisi_tabelo(mostePolje, ['id', 'ime', 'podrocje', 'nadstropje', 'leto', 'velikost', 'cena', 'posredovanje', 'tip1'],
                             'csv-datotekeP/mostePolje.csv')
        for tip in re.finditer(regex_tipa, orodja.vsebina_datoteke(html_datoteka)):
            tipi.append(pocisti_tip(tip))
            
    for html_datoteka in orodja.datoteke('zajeta-siskaP/'):
        print(html_datoteka)
        for stanovanje in re.finditer(regex_stanovanja, orodja.vsebina_datoteke(html_datoteka)):
            podrocje = 'Siska'
            stanovanja.append(pocisti_stanovanje(stanovanje, podrocje))
            siska.append(pocisti_stanovanje(stanovanje, podrocje))
        orodja.zapisi_tabelo(siska, ['id', 'ime', 'podrocje', 'nadstropje', 'leto', 'velikost', 'cena', 'posredovanje', 'tip1'],
                             'csv-datotekeP/siska.csv')
        for tip in re.finditer(regex_tipa, orodja.vsebina_datoteke(html_datoteka)):
            tipi.append(pocisti_tip(tip))
            
    for html_datoteka in orodja.datoteke('zajeta-vic-rudnikP/'):
        print(html_datoteka)
        for stanovanje in re.finditer(regex_stanovanja, orodja.vsebina_datoteke(html_datoteka)):
            podrocje = 'Vic-Rudnik'
            stanovanja.append(pocisti_stanovanje(stanovanje, podrocje))
            vicRudnik.append(pocisti_stanovanje(stanovanje, podrocje))
        orodja.zapisi_tabelo(vicRudnik, ['id', 'ime', 'podrocje', 'nadstropje', 'leto', 'velikost', 'cena', 'posredovanje', 'tip1'],
                             'csv-datotekeP/vicRudnik.csv')
        for tip in re.finditer(regex_tipa, orodja.vsebina_datoteke(html_datoteka)):
            tipi.append(pocisti_tip(tip))

    orodja.zapisi_tabelo(stanovanja, ['id', 'ime', 'podrocje', 'nadstropje', 'leto', 'velikost', 'cena', 'posredovanje', 'tip1'],
                             'csv-datotekeP/stanovanja.csv')
    orodja.zapisi_tabelo(tipi, ['id', 'tip'], 'csv-datotekeP/tipi.csv')
    
zajemi_bezigrad()
zajemi_center()
zajemi_moste_polje()
zajemi_siska()
zajemi_vic_rudnik()
pripravi()
