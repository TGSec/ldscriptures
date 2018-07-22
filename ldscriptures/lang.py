# coding: latin-1
from .utils import *
from . import exceptions
from . import utils

import json
import os

try:
    languages_file = open(os.path.join(os.path.dirname(__file__), 'languages.json'))
    language_data = json.loads(languages_file.read())
except:
    raise exceptions.MissingLanguageData('error in finding or openning "languages.json".')

default = 'eng'

available = list(language_data.keys())

def set_default(language):
    if not language in available:
        raise exceptions.InvalidLang('the language "{}" is not an available language (see ldscriptures.lang.available).'.format(language))
    default = language

scripture_data = {
    'ot': {
        'chapters': ['50', '40', '27', '36', '34', '24', '21', '4', '31', '24', '22', '25', '29', '36', '10', '13', '10', '42', '150', '31', '12',
                     '8', '66', '52', '5', '48', '12', '14', '3', '9', '1', '4', '7', '3', '3', '3', '2', '14', '4'],
        'codes': ['gen', 'ex', 'lev', 'num', 'deut', 'josh', 'judg', 'ruth', '1-sam', '2-sam', '1-kgs', '2-kgs', '1-chr', '2-chr', 'ezra', 'neh', 'esth', 'job', 'ps', 'prov', 'eccl', 'song', 'isa',
                  'jer', 'lam', 'ezek', 'dan', 'hosea', 'joel', 'amos', 'obad', 'jonah', 'micah', 'nahum', 'hab', 'zeph', 'hag', 'zech', 'mal']
    },
    'nt': {
        'chapters': ['28', '16', '24', '21', '28', '16', '16', '13', '6', '6', '4', '4', '5', '3', '6', '4', '3', '1', '13', '5', '5', '3', '5',
                     '1', '1', '1', '22'],
        'codes': ['matt', 'mark', 'luke', 'john', 'acts', 'rom', '1-cor', '2-cor', 'gal', 'eph', 'philip', 'col', '1-thes', '2-thes', ' 1-tim',
                  '2-tim', 'titus', 'philem', 'heb', 'james', '1-pet', '2-pet', '1-jn', '2-jn', '3-jn', 'jude', 'rev']
    },
    'bofm': {
        'chapters': ['22', '33', '7', '1', '1', '1', '1', '29', '63', '16', '30', '1', '9', '15', '10'],
        'codes': ['1-ne', '2-ne', 'jacob', 'enos', 'jarom', 'omni', 'w-of-m', 'mosiah', 'alma', 'hel', '3-ne', '4-ne', 'morm', 'ether', 'moro']
    },
    'pgp': {
        'chapters': ['8', '5', '1', '1', '1'],
        'codes': ['moses', 'abr', 'js-m', 'js-h', 'a-of-f']},
    'dc-testament': {
        'chapters': [138],
        'codes': ['dc']
    }
}


def get_language_dict(language):
    if not language in available:
        raise exceptions.InvalidLang('the language "{}" is not an available language (see ldscriptures.lang.available).'.format(language))
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
    elif book_name in [book.lower() for book in language_dict['dc_testament']]:
        scripture = 'dc-testament'
    else:
        raise exceptions.InvalidBook('The book \'{}\' does not exist.'.format(str(book_name)))
    
    return scripture

# Deprecated: match_scripture
match_scripture = get_scripture_code


def get_book_code(book, language):
    language_dict = get_language_dict(language)
    book = book.lower()
    
    scripture = get_scripture_code(book, language)
    
    codes = scripture_data[scripture]['codes']
    
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