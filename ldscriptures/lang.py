# coding: latin-1
from .utils import *
from . import exceptions
from . import utils

import json
import os

try:
    languages_file = open(os.path.join(
        os.path.dirname(__file__), 'languages.json'))
    translations = json.loads(languages_file.read())
except:
    raise exceptions.MissingLanguageData(
        'error in finding or openning "languages.json".')

default = 'eng'

available = list(translations.keys())


def set_default(language):
    if not language in available:
        raise exceptions.InvalidLang(
            'the language "{}" is not an available language (see ldscriptures.lang.available).'.format(language))
    global default
    default = language


def get_language_dict(language):
    if not language in available:
        raise exceptions.InvalidLang(
            'the language "{}" is not an available language (see ldscriptures.lang.available).'.format(language))
    return translations[language]


def get_scripture_code(book_name, language):
    language_dict = get_language_dict(language)
    book_name = book_name.lower()
    scripture = ''

    if book_name in [language_dict['ot'][book].lower() for book in language_dict['ot']]:
        scripture = 'ot'
    elif book_name in [language_dict['nt'][book].lower() for book in language_dict['nt']]:
        scripture = 'nt'
    elif book_name in [language_dict['bofm'][book].lower() for book in language_dict['bofm']]:
        scripture = 'bofm'
    elif book_name in [language_dict['pgp'][book].lower() for book in language_dict['pgp']]:
        scripture = 'pgp'
    elif book_name in [language_dict['dc-testament'][book].lower() for book in language_dict['dc-testament']]:
        scripture = 'dc-testament'
    else:
        raise exceptions.InvalidBook(
            'The book \'{}\' does not exist.'.format(str(book_name)))

    return scripture


def get_book_code(book, language):
    lang_dict = get_language_dict(language)

    for scr in lang_dict:
        for book_code in lang_dict[scr]:
            if lang_dict[scr][book_code].lower() == book.lower():
                return book_code
