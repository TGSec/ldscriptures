from .utils import *
from . import lang
from . import exceptions

import re
import requests
from bs4 import BeautifulSoup

def set_language(language):
    try:
        lang.get_language_dict(language)
    except:
        raise exceptions.InvalidLang('the language "{}" is not a valid language. Try one: {}.'.format(str(lang_text), str(lang.langs)))
    
    lang.default = language


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
    Easy way to access the scriptures, using a reference.
    
    :param str ref Scriptural reference.
    :return
    
    '''
    
    if type(ref) == str:
        ref = Reference(ref)
    
    book_name, chapter, verses = ref.book_name, ref.chapters, ref.verses
    
    if len(chapter) == 1 and len(verses) > 0:
        chapter_verses = request_chapter(book_name, chapter[0], lang.default)
        nverses = []
        for verse in chapter_verses:
            if verse.number in verses:
                nverses.append(verse)
        return Chapter(ref, nverses)
    
    if len(chapter) > 1 and len(verses) == 0:
        req_chapters = []
        for ch in chapter:
            req_chapters.append(Chapter(ref, request_chapter(book_name, str(ch), lang.default)))
        return req_chapters


class Reference(str):
    
    single_verse = False
    single_chapter = False
    no_verse = False

    _splited_reference = []
    
    
    def __new__(self, reference_str):
        return str.__new__(self, reference_str)
    
    
    def __init__(self, initial_value=False):
        if type(initial_value) == str:
            self.set_reference(initial_value)
    
    
    def set_book_name(self, book_name):
        if self.book_name == '':
            raise exceptions.InvalidScriptureReference('no book_name.')
        self._splited_reference[0] = book_name
    
    
    def set_chapters(self, chapters):
        if chapters == []:
            raise exceptions.InvalidScriptureReference('no chapter.')
        
        for n in chapters:
            if type(n) != int:
                exceptions.InvalidScriptureReference('all chapters must be int.')
        
        self._splited_reference[1] = chapters
    
    
    def set_verses(self, verses):
        if verses == []:
            raise exceptions.InvalidScriptureReference('no verse.')
        
        for n in verses:
            if type(n) != int:
                exceptions.InvalidScriptureReference('all verses must be int.')
        
        self._splited_reference[2] = verses
    
    
    def set_reference(self, reference_str):
        patt = '^(.+) ((?:[0-9]+(?:-[0-9]+)?,?)*)(?::((?:[0-9]+(?:-[0-9]+)?,?)*))?$'
        
        if not re.match(patt, reference_str):
            raise exceptions.InvalidScriptureReference('Regex failure: \'{0}\' is not a valid reference.'.format(reference))
            
        _splited_reference = list(re.findall(patt, reference_str)[0])
            
        if ('-' in _splited_reference[1] or ',' in _splited_reference[1]) and len(_splited_reference[2]) > 0:
            raise exceptions.InvalidScriptureReference('can\'t be set more than one chapter and be set a/some verse.')
        
        _splited_reference[1] = string_range(_splited_reference[1])
        
        if _splited_reference[2] != '':
            _splited_reference[2] = string_range(_splited_reference[2])
        else:
            _splited_reference[2] = []
        
        self._splited_reference = _splited_reference
        
        self.verify()
    
    
    @property
    def no_verse(self):
        self.verify()
        return self.verses == []
    
    
    @property
    def single_chapter(self):
        self.verify()
        return len(self.chapters) == 1
    
    
    @property
    def single_verse(self):
        self.verify()
        return len(self.verses) == 1
    
    
    @property
    def book_name(self):
        return self._splited_reference[0]
    
    
    @property
    def chapters(self):
        return self._splited_reference[1]
    
    
    @property
    def verses(self):
        return self._splited_reference[2]

    
    def verify(self):
        if len(self.chapters) > 1 and self.verses != []:
            raise exceptions.InvalidScriptureReference('can\'t be set more than one chapter and be set a/some verse.')
        if self.chapters == []:
            raise exceptions.InvalidScriptureReference('"chapters" can\'t be of lenght 0.')
        for i in self.chapters:
            if type(i) != int:
                raise exceptions.InvalidScriptureReference('"chapters" must contain only ints.')
        return True
    
    
    def _list_to_str(self, list):  # Function to convert a list of int() in a valid reference string. Basic "lexer".
        seq = []
        ranged_ref = []
        list = sorted(set(list))  # For ordering and removing repeated items
        last = -1
        
        for item in list:
            if seq == []:  # If no seq started
                seq.append(item)
            elif len(seq) > 0 and item == last+1:  # If seq started and item is last+1
                seq.append(item)
            elif len(seq) <= 2 and item != last+1:  # If seq less or equal to 2 and item not equal to last=1
                for each in seq:
                    ranged_ref.append(each)
                seq = [item]
            elif len(seq) >= 3 and item != last+1:
                ranged_ref.append('{}-{}'.format(seq[0], seq[-1]))
                seq = [item]
                
            last = item
        
        if len(seq) > 1:
            ranged_ref.append('{}-{}'.format(seq[0], seq[-1]))
        elif len(seq) == 1:
            ranged_ref.append(seq[0])
        
        string = ''
        
        for each in ranged_ref:
            string += str(each) + ','
        
        return string[:-1]
    
    
    def __str__(self):
        self.verify()
        if self.no_verse and self.single_chapter:
            return '{book_name} {chapters}'.format(book_name=self.book_name, chapters=self.chapters[0])
        if self.single_verse:
            return '{book_name} {chapters}:{verses}'.format(book_name=self.book_name, chapters=self.chapters[0], verses=self.verses)
        if not self.single_verse:
            return '{book_name} {chapters}:{verses}'.format(book_name=self.book_name, chapters=self.chapters[0], verses=self._list_to_str(self.verses))
        if not self.single_chapter:
            return '{book_name} {chapters}'.format(book_name=self.book_name, chapters=self._list_to_str(self.chapters))
    
    __repr__ = __str__
            
    


class Chapter(list):
    '''
    A class that represents a chapter.
    '''
    
    reference = ''
    '''The scriptural reference to the chapter (Reference object).'''
    
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

if __name__ == '__main__':
    ref = Reference('Mateus 5:14-16')._list_to_str([1,3,4,5])