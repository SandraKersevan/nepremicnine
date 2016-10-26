import orodja
import re
import csv


html_datoteke = []
nepremicnine = []

for stran in range(1, 40):
    osnovni_naslov = 'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/'
    naslov = '{}/'.format(osnovni_naslov, stran)
    html_datoteka = 'html_dat/{0}.html'.format(stran)
    html_datoteke += {html_datoteka}
    orodja.shrani(naslov, html_datoteka)
   

vzorec_nepremicnina = re.compile(
    r'<h2><a href="\/oglasi-prodaja\/.*?\/" title="(?P<id>\d+)">.*?<span class="title">(?P<naslov>.*?)<\/span><\/a><\/h2>.*?<span class="atribut">Nadstropje: <strong>(?P<nadstropje>.*?)<\/strong>\/?.*?<\/span><span class="atribut">Leto: <strong>(?P<leto>\d{4})<\/strong>.*?<div class="kratek">(?P<opis>.*?)<\/div>.*?<span class="velikost">(?P<velikost>\d+?.*?)<\/span><br\s?\/>.*?<span class="cena">(?P<cena>.*?) &?euro;',
    flags=re.DOTALL
)


def pocisti_nepremicnino(nepremicnina):
    podatki = nepremicnina.groupdict()
    podatki['id'] = int(podatki['id'])
    podatki['naslov'] = str(podatki['naslov'])
    podatki['nadstropje'] = str(podatki['nadstropje'])
    podatki['leto'] = int(podatki['leto'])
    podatki['opis'] = podatki['opis'].strip()
    podatki['velikost'] = str(podatki['velikost'])
    podatki['cena'] = str(podatki['cena'])
    return podatki

def izloci_podatke():
    for html_datoteka in html_datoteke:
        for nepremicnina in re.finditer(vzorec_nepremicnina, orodja.vsebina_datoteke(html_datoteka)):
            nepremicnine.append(pocisti_nepremicnino(nepremicnina))
    return nepremicnine

izloci_podatke()
orodja.zapisi_tabelo(nepremicnine, ['id', 'naslov', 'nadstropje', 'leto', 'velikost', 'cena', 'opis'], 'csv-dat/nepremicnine.csv')
