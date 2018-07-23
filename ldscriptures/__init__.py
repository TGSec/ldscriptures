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


def request_chapter(book_name, chapter, language):
    requester = PageRequester(language)
    scripture = lang.match_scripture(book_name, language)
    book_code = lang.get_book_code(book_name, language)
    chapter = str(chapter)
    chapter_html = requester.request_scripture(scripture, book_code, chapter)
    ext = PageExtractor(chapter_html)
    return ext.verses()


def get(ref):
    '''
    
    '''
    
    book_name, chapter, verses = utils.reference_split(ref)
    
    if len(chapter) == 1 and len(verses) == 0:
        chapter_verses = request_chapter(book_name, chapter[0], lang.default)
        return Chapter(book_name + ' ' + str(chapter[0]), chapter_verses)
    
    if len(chapter) == 1 and len(verses) > 0:
        chapter_verses = request_chapter(book_name, chapter[0], lang.default)
        nverses = []
        for verse in chapter_verses:
            if verse.number in verses:
                nverses.append(verse)
        
        return Chapter(book_name + ' ' + str(chapter[0]), nverses)
    
    if len(chapter) > 1 and len(verses) == 0:
        req_chapters = []
        for ch in chapter:
            req_chapters.append(Chapter(book_name + ' ' + str(ch), request_chapter(book_name, str(ch), lang.default)))
        return req_chapters


class Reference(str):
    
    single_verse = False
    single_chapter = False
    no_verse = False
    book_name = ''
    chapters = []
    verses = []
    
    
    def __new__(self, reference_str):
        return str.__new__(self, reference_str)
    
    
    def __init__(self, reference_str):
        patt = '^(.+) ((?:[0-9]+(?:-[0-9]+)?,?)*)(?::((?:[0-9]+(?:-[0-9]+)?,?)*))?$'
        
        if not re.match(patt, reference_str):
            raise exceptions.InvalidScriptureReference('Regex failure: \'{0}\' is not a valid reference.'.format(reference))
            
        splited_reference = list(re.findall(patt, reference_str)[0])
            
        if ('-' in splited_reference[1] or ',' in splited_reference[1]) and len(splited_reference[2]) > 0:
            raise exceptions.InvalidScriptureReference('can\'t be set more than one chapter and be set a/some verse.')
        
        splited_reference[1] = string_range(splited_reference[1])
        
        if splited_reference[2] != '':
            splited_reference[2] = string_range(splited_reference[2])
        else:
            splited_reference[2] = []
            
        self.update()
    
    
    def update(self):
        print('update got called lol')
        self.book_name = splited_reference[0]
        self.chapters = splited_reference[1]
        self.verses = splited_reference[2]
        
        if len(self.chapters) == 1:
            self.single_chapter = True
        
        if len(self.verses) == 1:
            self.single_verse = True
        
        if len(self.verses) == 0:
            self.no_verse = True
    
    
    def _list_to_str(self, list):  # Function to convert a list of int() in a valid reference string. Basic "lexer".
        range_first = int()
        range_lenght = 0
        range_last = int()
        ranged_ref = []
        list = set(list)  # For ordering and removing repeated items
        for item in list:
        
            if range_lenght == 0:  # Start range
                range_first = item
            
            elif range_lenght > 0 and (range_first+range+lenght) == item:  # Make range
                range_last = item
                range_lenght += 1
            
            elif range_lenght > 1:  # End of range
                ranged_ref.append('{}-{}'.format(range_first, range_last))
                range_first = 0
                range_last = 0
                range_lenght = 0
            
            elif range_lenght == 1:  # End of little range
                ranged_ref.append(range_first)
                ranged_ref.append(range_last)
                range_first = 0
                range_last = 0
                range_lenght = 0
        
        string = ''
        
        for each in ranged_ref:
            string += each + ','
        
        return string[:-1]
    
    
    def __str__(self):
        if self.no_verse and self.single_chapter:
            return '{book_name} {chapters}'.format(book_name=self.book_name, chapters=self.chapters[0])
        if self.single_verse:
            return '{book_name} {chapters}:{verses}'.format(book_name=self.book_name, chapters=self.chapters[0], verses=self.verses)
            
    


class Chapter(list):
    '''
    A class that represents a chapter.
    '''
    
    reference = ''
    '''The scriptural reference to the chapter.'''
    
    complete_text = ''
    '''A simple way to access the scriptural text of the class. It uses the following format: "{reference}\n\n{verses}"'''
    
    
    def __new__(self, reference, verses):
        return list.__new__(self, verses)
    
    
    def __init__(self, reference, verses):
        list.__init__(self, verses)
        self.reference = utils.better_capitalize(reference)
        
        verses_text = ''
        
        for verse in verses:
            verses_text = verses_text + verse + '\n'
        
        verses_text = verses_text.strip()
        
        self.text = '{reference}\n\n{verses}'.format(reference=self.reference, verses=verses_text)
        

class Verse(str):
    '''A class that represents a single verse. Can be used as a str() to access the entire verse (number + text).'''
    
    number = 0
    '''The verse\'s number itself.'''
    
    only_text = ''
    '''The text of the verse, excluding its number.'''
    
    
    def __new__(self, brute_verse):
        return str.__new__(self, brute_verse)
    
    
    def __init__(self, brute_verse):
        self.brute_verse = brute_verse
        self.number = int(brute_verse.split(' ')[0])
        self.text = brute_verse.split(' ', 1)[1]


class PageExtractor:
    '''
    A powerful class that extracts the scriptural information from lds.org html.
    
    :param str html: The html whose information will be extracted.
    
    '''
    
    
    def __init__(self, html):
        self.html = BeautifulSoup(html, 'html.parser')
    
    
    def _clean(self, text):
        return text.replace('\u2014', ' - ').replace('\xa0', '').replace('\u2019', '\'')
    
    
    def verses(self):
        '''
        Get the verses that could be found the html.
        :return list of :py:class:`Verse` objects.
        '''
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
