from . import utils
from . import lang
from . import exceptions

import re
import requests
from bs4 import BeautifulSoup

def set_language(lang_text):
    try:
        lang.lang_verify(lang_text)
    except:
        raise exceptions.InvalidLang('The language "{}" is not a valid language. Try one: {}.'.format(str(lang_text), str(langs)))
    
    lang.default = lang_text
    

def get_scripture(ref):
    book_name, chapter, verse = utils.reference_spliter(ref)
    
    if len(chapter) == 1:
        requester = PageRequester()

class PageExtractor:

    def __init__(self, html):
        self.html = BeautifulSoup(html, 'html5lib')
    
    def verses(self):
        verses = []
        
        html = self.html
        brute_verses = html.find_all('p', {'class': 'verse'})
        
        for verse in brute_verses:
            for tag in verse.find_all('sup'):
                tag.clear()
            verses.append(verse.get_text().replace('\u2014', '-').replace('\xa0', ' '))
        
        return verses
        
    def study_summaries(self):
        study_summaries = []
        
        html = self.html
        brute_summ = html.find_all('p', {'class': 'study-summary'})
        
        for summ in brute_summ:
            study_summaries.append(summ.get_text().replace('\u2014', ' - ').replace('\xa0', '').replace('  ', ' '))
            
        return study_summaries
    
    def fac_simile(self):
        html = self.html
        
        fac_url = html.find('a', {'class': 'view-larger'})['href']
        
        fac_explanation = html.find('section')
        fac_explanation.find('h2').clear()
        fac_explanation = fac_explanation.get_text()
        fac_explanation = fac_explanation.replace('\n\t\t\t\t\t\n\t\t\t\t\t', '').replace('\n\t\t\t\t\t', '\n').replace('\n\t\t\t\t', '')
        
        return [fac_url, fac_explanation]
        
    def official_declaration(self):  # From Doctrine and Covenants
        html = self.html
        
        official_dec_part1 = html.find('p', {'class': 'study-intro'}).get_text()
        
        official_dec_part2 = html.find('div', {'class': 'article'}).get_text()
        official_dec_part2 = official_dec_part2.replace('\t', '').replace('\n\n\n', '\n\n')
        
        while official_dec_part2[0] in ' \n':  # While the first character of "official_dec_part2" is a space or a new line
            official_dec_part2 = official_dec_part2[1:]  # Remove the first character
        
        while official_dec_part2[len(official_dec_part2)-1] in ' \n':  # While the last character of "official_dec_part2" is a space or a new line
            official_dec_part2 = official_dec_part2[:-1]  # Remove the last character
        
        official_dec = official_dec_part1 + '\n\n' + official_dec_part2
        
        return official_dec


class PageRequester:
    
    def __init__(self, lang=lang.default):
        self.lang = lang
    
    def url_compose(self, scripture, book, chapter):
        scripture_url = '/' + scripture
            
        book_url = '/' + book
        
        chapter_url = '/' + chapter
        
        url = utils.scriptures_url_base + scripture_url + book_url + chapter_url + '?lang=' + self.lang
        
        return url
    
    def request_scripture(self, scripture, book, chapter):
        url = self.url_compose(scripture, book, chapter)
        
        html = requests.get(url).text
        
        return html
