from .utils import *
from .lang import *
from .exceptions import *

import re
import requests
from bs4 import BeautifulSoup

def set_language(lang_text):
    try:
        lang.lang_verify(lang_text)
    except:
        raise exceptions.InvalidLang('The language "{}" is not a valid language. Try one: {}.'.format(str(lang_text), str(lang.langs)))
    
    lang.default = lang_text


def request_chapter_verses(book_name, chapter, language):
    requester = PageRequester(language)
    scripture = lang.match_scripture(book_name, language)
    book_code = lang.get_book_code(book_name, language)
    chapter = str(chapter)
    chapter_html = requester.request_scripture(scripture, book_code, chapter)
    ext = PageExtractor(chapter_html)
    return ext.verses()


def get(ref):
    book_name, chapter, verses = utils.reference_split(ref)
    
    if len(chapter) == 1 and len(verses) == 0:
        chapter_verses = request_chapter_verses(book_name, chapter[0], lang.default)
        return Chapter(book_name + ' ' + str(chapter[0]), chapter_verses)
    
    if len(chapter) == 1:
        chapter_verses = request_chapter_verses(book_name, chapter[0], lang.default)
        nverses = []
        for verse in chapter_verses:
            if verse.number in verses:
                nverses.append(verse)
        
        return Chapter(book_name + ' ' + str(chapter[0]), nverses)
    
    if len(chapter) > 1:
        req_chapters = []
        for ch in chapter:
            req_chapters.append(Chapter(book_name + ' ' + str(ch), request_chapter_verses(book_name, str(ch), lang.default)))
        return req_chapters

class Chapter(list):
    
    def __new__(self, reference, verses):
        return list.__new__(self, verses)
    
    def __init__(self, reference, verses):
        list.__init__(self, verses)
        self.reference = reference
        
        verses_text = ''
        
        for verse in verses:
            verses_text = verses_text + verse + '\n'
        
        self.text = utils.better_capitalize(ref) + '\n\n' + verses_text.strip()
    

class Verse(str):
    
    number = 0
    text = ''
    
    def __new__(self, brute_verse):
        return str.__new__(self, brute_verse)
    
    def __init__(self, brute_verse):
        self.brute_verse = brute_verse
        self.number = int(brute_verse.split(' ')[0])
        self.text = brute_verse.split(' ', 1)[1]


class PageExtractor:

    def __init__(self, html):
        
        self.html = BeautifulSoup(html, 'html5lib')
    
    def _clean(self, text):
        return text.replace('\u2014', ' - ').replace('\xa0', '').replace('\u2019', '\'')
    
    def verses(self):
        verses = []
        
        html = self.html
        brute_verses = html.find_all('p', {'class': 'verse'})
        
        for verse in brute_verses:
            for tag in verse.find_all('sup'):
                tag.clear()
            verse = Verse(self._clean(verse.get_text()).replace(chr(182), ''))
            verses.append(verse)
        
        return verses
        
    def study_summaries(self):
        study_summaries = []
        
        html = self.html
        brute_summ = html.find_all('p', {'class': 'study-summary'})
        
        for summ in brute_summ:  #   -  clean "trash" bytes
            study_summaries.append(summ.get_text().replace('  ', ' '))
            
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
    
    def __init__(self, language=lang.default):
        self.language = language
        
    def url_compose(self, scripture, book, chapter):
        scripture_url = '/' + scripture
            
        book_url = '/' + book
        
        chapter_url = '/' + chapter
        
        url = utils.scriptures_url_base + scripture_url + book_url + chapter_url + '?lang=' + self.language
        
        return url
    
    def request_scripture(self, scripture, book, chapter):
        url = self.url_compose(scripture, book, chapter)
        
        html = requests.get(url).text
        
        return html
