import requests
import json
from base64 import b64encode
from nacl import encoding, public
import re
import string, random
import os

organization = "Pooposting"
url = "https://api.github.com/"
nazwaSekretu = "APP_SECRET_GENERATED_"
regex = nazwaSekretu + "[0-9]"
dlugosc = 64
NoS = "NoS"
key = os.getenv('API_KEY_DEVOPS')
headers={
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {key}',
    'X-GitHub-Api-Version': '2022-11-28',
}

def sprawdzCzyIstniejeZmienna(nazwa):
    nurl = url + f"orgs/{organization}/actions/variables/{nazwa}"
    response = requests.get(url=nurl, headers=headers)
    if(response.status_code == 200):
        return 0
    else:
        return 1

def zaktualizujWartoscZmienna(nazwa, wartosc):
    data={
        'name': f'{nazwa}',
        'value': f'{wartosc}',
    }
    nurl = url + f"orgs/{organization}/actions/variables/{nazwa}"
    response = requests.patch(url=nurl, headers=headers, json=data)
    if(response.status_code == 204):
        return 0
    else:
        return 1

def dodajZmienna(nazwa, wartosc, widocznosc):
    data={
        'name': f'{nazwa}',
        'value': f'{wartosc}',
        'visibility': f'{widocznosc}'
    }
    nurl = url + f"orgs/{organization}/actions/variables"
    if(sprawdzCzyIstniejeZmienna(nazwa) == 1):
        response = requests.post(url=nurl, headers=headers, json=data)
    else:
        zaktualizujWartoscZmienna(nazwa, wartosc)

def usunZmienna(nazwa):
    nurl = url + f"orgs/{organization}/actions/variables/{nazwa}"
    if(sprawdzCzyIstniejeZmienna(nazwa) == 0):
        response = requests.delete(url=nurl, headers=headers)
        
def odczytZmienna(nazwa):
    nurl = url + f"orgs/{organization}/actions/variables/{nazwa}"
    if(sprawdzCzyIstniejeZmienna(nazwa) == 0):
        response = requests.get(url=nurl, headers=headers).json()['value']
        return response
        
def liczSekrety():
    nurl = url + f"orgs/{organization}/actions/secrets"
    response = requests.get(url=nurl, headers=headers).json()['secrets']
    return len(response)
    
def liczAppSekrety(regex=""):
    nurl = url + f"orgs/{organization}/actions/secrets"
    response = requests.get(url=nurl, headers=headers).json()['secrets']
    ilosc=0
    for i in range(liczSekrety()):
        if(regex != ""):
            if(re.match(regex.upper(), response[i]['name'])):
                ilosc = ilosc+1
    return ilosc
        
def sprawdzCzyIstniejeSkeret(nazwa):
    nurl = url + f"orgs/{organization}/actions/secrets/{nazwa}"
    response = requests.get(url=nurl, headers=headers)
    if(response.status_code == 200):
        return 0
    else:
        return 1

def dodajZaktualizujSekret(nazwa, wartosc, widocznosc):
    nurl = url + f'orgs/{organization}/actions/secrets/public-key'
    orgKeyresponse = requests.get(url=nurl, headers=headers)
    orgKey = orgKeyresponse.json()['key']
    keyID = orgKeyresponse.json()['key_id']
    orgKey = public.PublicKey(orgKey.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(orgKey)
    encrypted = sealed_box.encrypt(wartosc.encode("utf-8"))
    szyfr = b64encode(encrypted).decode("utf-8")
    data={
        'name': f'{nazwa}',
        'encrypted_value': f'{szyfr}',
        'visibility': f'{widocznosc}',
        'key_id': f'{keyID}'
    }
    nurl = url + f"orgs/{organization}/actions/secrets/{nazwa}"
    response = requests.put(url=nurl, headers=headers, json=data)
    
def usunSekret(nazwa):
    nurl = url + f"orgs/{organization}/actions/secrets/{nazwa}"
    if(sprawdzCzyIstniejeSkeret(nazwa) == 0):
        response = requests.delete(url=nurl, headers=headers)

def generowanieString(dlugosc):
    generated = ''.join(random.choice(string.ascii_letters) for i in range(dlugosc))
    return generated

def porownanieZmiennychZWartosciami(odpowiedz = ""):
    if(int(odczytZmienna(NoS)) > int(liczAppSekrety(regex))):
        if(odpowiedz == "owszem"):
            poczatek = 1
        else:
            poczatek = int(liczAppSekrety(regex)+1)
        for i in range(poczatek, int(odczytZmienna(NoS))+1):
            dodajZaktualizujSekret(nazwaSekretu+str(i), generowanieString(dlugosc), 'all')
    elif(int(odczytZmienna(NoS)) < int(liczAppSekrety(regex))):
        for i in range(int(liczAppSekrety(regex)), int(odczytZmienna(NoS)), -1):
            usunSekret(nazwaSekretu+str(i))
        if(odpowiedz == "owszem"):
            poczatek = 1
            for i in range(poczatek, int(odczytZmienna(NoS))+1):
                dodajZaktualizujSekret(nazwaSekretu+str(i), generowanieString(dlugosc), 'all')
    else:
        if(odpowiedz == "owszem"):
            poczatek = 1
            for i in range(poczatek, int(odczytZmienna(NoS))+1):
                dodajZaktualizujSekret(nazwaSekretu+str(i), generowanieString(dlugosc), 'all')
#try:
porownanieZmiennychZWartosciami(os.getenv('aktualizowac'))
#except:
#    print("Error!")