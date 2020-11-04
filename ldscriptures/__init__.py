from .utils import *
from .types import *
from . import lang
from . import exceptions
from . import cache

import re
import requests
from bs4 import BeautifulSoup


def request_chapter(book_name, chapter, language):
    requester = ScriptureRequester(language)
    scripture = lang.get_scripture_code(book_name, language)
    book_code = lang.get_book_code(book_name, language)
    chapter = str(chapter)

    chapter_html = requester.request_scripture(scripture, book_code, chapter)
    ext = ScriptureExtractor(chapter_html)

    return ext.verses()


def get(ref):
    '''
    Easy way to access the scriptures, using a reference.

    :param str ref Scriptural reference.
    :return

    '''
    
    if type(ref) == str:
        ref = Reference(ref)

    book, chapter, verse = ref.book, ref.chapter, ref.verse

    if len(verse) > 0:
        chapter_verses = request_chapter(book, chapter[0], lang.default)
        nverses = []
        for returned_verse in chapter_verses:
            if returned_verse.number in verse:
                nverses.append(returned_verse)
        return Scripture(ref, nverses)

    if len(verse) == 0:
        req_chapters = []
        for ch in chapter:
            req_chapters.append(
                Scripture(ref, request_chapter(book, str(ch), lang.default)))
        return req_chapters


class ScriptureExtractor:
    '''
    A powerful class that extracts the scriptural information from churchofjesuschrist.org html.

    :param str html: The html whose information will be extracted.

    '''

    def __init__(self, html):
        self.html = BeautifulSoup(html, 'lxml')

    def _clean(self, text):
        return text.replace('\u2014', ' - ').replace('\xa0', '').replace('\u2019', '\'')

    def verses(self):
        '''
        Get the verses that could be found the html.
        :return list of :py:class:`Verse` objects.
        '''
        verses = []

        raw_verses = self.html.find_all('p', class_='verse')

        for raw_verse in raw_verses:
            verse = Verse(raw_verse)
            verses.append(verse)

        return verses

    def study_summaries(self):
        study_summaries = []

        html = self.html
        brute_summ = html.find_all('p', {'class': 'study-summary'})

        for summ in brute_summ:  # -  clean "trash" bytes
            study_summaries.append(summ.get_text().replace('  ', ' '))

        return study_summaries

    def fac_simile(self):
        html = self.html

        fac_url = html.find('a', {'class': 'view-larger'})['href']

        fac_explanation = html.find('section')
        fac_explanation.find('h2').clear()
        fac_explanation = fac_explanation.get_text()
        fac_explanation = fac_explanation.replace('\n\t\t\t\t\t\n\t\t\t\t\t', '').replace(
            '\n\t\t\t\t\t', '\n').replace('\n\t\t\t\t', '')

        return [fac_url, fac_explanation]

    def official_declaration(self):  # From Doctrine and Covenants
        html = self.html

        official_dec_part1 = html.find(
            'p', {'class': 'study-intro'}).get_text()

        official_dec_part2 = html.find('div', {'class': 'article'}).get_text()
        official_dec_part2 = official_dec_part2.replace(
            '\t', '').replace('\n\n\n', '\n\n')

        # While the first character of "official_dec_part2" is a space or a new line
        while official_dec_part2[0] in ' \n':
            # Remove the first character
            official_dec_part2 = official_dec_part2[1:]

        # While the last character of "official_dec_part2" is a space or a new line
        while official_dec_part2[len(official_dec_part2)-1] in ' \n':
            # Remove the last character
            official_dec_part2 = official_dec_part2[:-1]

        official_dec = official_dec_part1 + '\n\n' + official_dec_part2

        return official_dec


class ScriptureRequester:

    def __init__(self, language=lang.default):
        self.language = language

    def url_compose(self, scripture, book, chapter):
        scripture_url = '/' + scripture

        book_url = '/' + book

        chapter_url = '/' + str(chapter)

        url = scriptures_url_base + scripture_url + \
            book_url + chapter_url + '?lang=' + self.language

        return url

    def request_scripture(self, scripture, book, chapter):
        url = self.url_compose(scripture, book, chapter)

        html = requests.get(url)

        html.encoding = html.apparent_encoding

        return html.text


if __name__ == '__main__':
    pass