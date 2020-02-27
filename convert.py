import requests
from bs4 import BeautifulSoup


def convertor(toval, val, nominal):
    val, toval, nominal = val.upper(), toval.upper(), float(nominal)
    mydict = {'RU': 1}
    url1 = 'http://www.cbr.ru/scripts/XML_daily.asp?'
    r = requests.get(url=url1)
    soup = BeautifulSoup(r.text, 'lxml')
    for tag in soup.find_all('valute'):
        mydict[tag.charcode.text] =  float((tag.value.text).replace(',', '.')) / float(tag.nominal.text)
    if (val in mydict.keys()) and (toval in mydict.keys()):
        return [(round((mydict[val] / mydict[toval]) * nominal, 2))]