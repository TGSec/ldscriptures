# coding: latin-1
from .utils import *
from . import exceptions
from . import utils

import json
import os

try:
    languages_file = open(os.path.join(
        os.path.dirname(__file__), 'languages.json'))
    language_data = json.loads(languages_file.read())
except:
    raise exceptions.MissingLanguageData(
        'error in finding or openning "languages.json".')

default = 'eng'

available = list(language_data.keys())


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
    return language_data[language]


def get_scripture_code(book_name, language):
    language_dict = get_language_dict(language)
    book_name = book_name.lower()
    scripture = ''

    if book_name in [book.lower() for book in language_dict['ot']]:
        scripture = 'ot'
    elif book_name in [book.lower() for book in language_dict['nt']]:
        scripture = 'nt'
    elif book_name in [book.lower() for book in language_dict['bofm']]:
        scripture = 'bofm'
    elif book_name in [book.lower() for book in language_dict['pgp']]:
        scripture = 'pgp'
    elif book_name in [book.lower() for book in language_dict['dc-testament']]:
        scripture = 'dc-testament'
    else:
        raise exceptions.InvalidBook(
            'The book \'{}\' does not exist.'.format(str(book_name)))

    return scripture


# Deprecated: match_scripture
match_scripture = get_scripture_code


def get_book_code(book, language):
    language_dict = get_language_dict(language)
    book = book.lower()

    scripture = get_scripture_code(book, language)

    codes = list(chapter_numbers[scripture].keys())

    return codes[item_position(book, language_dict[scripture])]


def item_position(item, list):
    n = -1

    for i in list:
        n += 1

        if i.lower() == item.lower():
            return n

    return -1


def translate_book_name(book_name, from_lang, to_lang):
    from_lang_dict = get_language_dict(from_lang)
    to_lang_dict = get_language_dict(to_lang)

    scripture = get_scripture_code(book_name, from_lang)

    position = item_position(book_name, from_lang_dict[scripture])

    return to_lang_dict[scripture][position]
