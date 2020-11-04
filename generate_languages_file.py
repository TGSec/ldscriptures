from bs4 import BeautifulSoup
import json
import requests
import re


patt = '^/study/scriptures/([a-z-]+)/([0-9a-z-]+).+'

langs = ['eng', 'spa', 'por']

scripture_groups = ['ot', 'nt', 'bofm', 'pgp', 'dc-testament']

translations = {'eng': {}, 'spa': {}, 'por': {}}

for lang in langs:
    for scr in scripture_groups:
        print('Requesting {} for language {}...'.format(scr, lang))

        translations[lang][scr] = {}

        page = requests.get('https://www.churchofjesuschrist.org/study/scriptures/{}?lang={}'.format(scr, lang))
        html = BeautifulSoup(page.content.decode('utf-8'), 'lxml')
        
        if scr == 'dc-testament':
            tag = html.find('h1', id='title1')
            translations[lang][scr]['dc'] = tag.string
        else:
            for tag in html.find_all('a'):
                if not 'href' in tag.attrs.keys():
                    continue
                if 'title' in tag['href'] or 'introduction' in tag['href'] or 'eight' in tag['href'] or 'three' in tag['href']: continue
                if re.match(patt, tag['href']):
                    book_code = re.findall(patt, tag['href'])[0][1]
                    translations[lang][scr][book_code] = tag.string.replace('\xa0', ' ')

print('Downloaded all translations!')

print('Creating file...')

file = open('languages.json', 'w')

file.write(json.dumps(translations, indent=4, ensure_ascii=False))

file.close()

print('All work done!')