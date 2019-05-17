from bs4 import  BeautifulSoup as bs


import urllib.request
import urllib.parse
url= "http://www.wetter24.de/vorhersage/deutschland/march/18225000/"

def get_number(s):
    sdigits = ''.join([letter for letter in s if letter.isdigit()])
    #print(sdigits)
    return(sdigits)

def remove_space(s):
    sstring = ''.join([letter for letter in s if letter !=' '])
    return (sstring)


def get_wetterstation_data():
    response = urllib.request.urlopen(url)
    string = response.read()
    soup = bs(string,features="html.parser")

    s = soup.find_all("span", attrs={"class": "value"})
    #print(s[0].contents[1].contents[0])
    temperatur = "Temperatur",float(get_number(s[0].contents[0])),remove_space(s[0].contents[1].contents[0])
    taupunkt_temp = "Taupunkt_Temperatur", float(get_number(s[1].contents[0])),remove_space(s[1].contents[1].contents[0])
    rel_luftfeuchte = "relative_Luftfeuchte",float(get_number(s[2].contents[0])),remove_space(s[2].contents[1].contents[0])
    luft_druck = "Luftdruck", float(get_number(s[3].contents[0])),remove_space(s[3].contents[1].contents[0])
    boeen = "Boeen", float(get_number(s[4].contents[0])),remove_space(s[4].contents[1].contents[0])


    return(temperatur,taupunkt_temp,rel_luftfeuchte,luft_druck,boeen)
'''
data = get_wetterstation_data()
for i in data:
    print(i)'''
