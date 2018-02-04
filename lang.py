# coding: latin-1
from . import exceptions
from . import utils

default = 'eng'

langs = ['eng', 'pt', 'spa']

class Eng:  # English

    ot_books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings',
                '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah',
                'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah',
                'Haggai', 'Zechariah', 'Malachi']

    nt_books = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians',
                'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter',
                '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']

    bofm_books = ['1 Nephi', '2 Nephi', 'Jacob', 'Enos', 'Jarom', 'Omni', 'Words of Mormon', 'Mosiah', 'Alma', 'Helaman', '3 Nephi', '4 Nephi',
                  'Mormon', 'Ether', 'Moroni']

    pgp_books = ['Moses', 'Abraham', 'Joseph Smith-Matthew', 'Joseph Smith-History', 'Articles of Faith']


class Spa:  # Spanish
 
    ot_books = ['Génesis', 'Éxodo', 'Levítico', 'Números', 'Deuteronomio', 'Josué', 'Jueces', 'Rut', '1 Samuel', '2 Samuel', '1 Reyes', '2 Reyes',
                '1 Crónicas', '2 Crónicas', 'Esdras', 'Nehemías', 'Ester', 'Job', 'Salmos', 'Proverbios', 'Eclesiastés', 'Cantares', 'Isaías',
                'Jeremías', 'Lamentaciones', 'Ezequiel', 'Daniel', 'Oseas', 'Joel', 'Amós', 'Abdías', 'Jonás', 'Miqueas', 'Nahúm', 'Habacuc',
                'Sofonías', 'Hageo', 'Zacarías', 'Malaquías']
    
    nt_books = ['Mateo', 'Marcos', 'Lucas', 'Juan', 'Hechos', 'Romanos', '1 Corintios', '2 Corintios', 'Gálatas', 'Efesios', 'Filipenses',
                'Colosenses', '1 Tesalonicenses', '2 Tesalonicenses', '1 Timoteo', '2 Timoteo', 'Tito', 'Filemón', 'Hebreos', 'Santiago', '1 Pedro',
                '2 Pedro', '1 Juan', '2 Juan', '3 Juan', 'Judas', 'Apocalipsis']
    
    bofm_books = ['1 Nefi', '2 Nefi', 'Jacob', 'Enós', 'Jarom', 'Omni', 'Palabras de Mormón', 'Mosíah', 'Alma', 'Helamán', '3 Nefi', '4 Nefi',
                  'Mormón', 'Éter', 'Moroni']
    
    pgp_books = ['Moisés', 'Abraham', 'José Smith-Mateo', 'José Smith-Historia', 'Artículos de Fe']


class Pt:  # Portuguese

    ot_books = ['Gênesis', 'Êxodo', 'Levítico', 'Números', 'Deuteronômio', 'Josué', 'Juízes', 'Rute', '1 Samuel', '2 Samuel', '1 Reis', '2 Reis',
                '1 Crônicas', '2 Crônicas', 'Esdras', 'Neemias', 'Ester', 'Jó', 'Salmos', 'Provérbios', 'Eclesiastes', 'Cantares de Salomão',
                'Isaías', 'Jeremias', 'Lamentações', 'Ezequiel', 'Daniel', 'Oseias', 'Joel', 'Amós', 'Obadias', 'Jonas', 'Miqueias', 'Naum',
                'Habacuque', 'Sofonias', 'Ageu', 'Zacarias', 'Malaquias']
    
    nt_books = ['Mateus', 'Marcos', 'Lucas', 'João', 'Atos', 'Romanos', '1 Coríntios', '2 Coríntios', 'Gálatas', 'Efésios', 'Filipenses',
                'Colossenses', '1 Tessalonicenses', '2 Tessalonicenses', '1 Timóteo', '2 Timóteo', 'Tito', 'Filemom', 'Hebreus', 'Tiago', '1 Pedro',
                '2 Pedro', '1 João', '2 João', '3 João', 'Judas', 'Apocalipse']
    
    bofm_books = ['1 Néfi', '2 Néfi', 'Jacó', 'Enos', 'Jarom', 'Ômni', 'Palavras de Mórmon', 'Mosias', 'Alma', 'Helamã', '3 Néfi', '4 Néfi',
                  'Mórmon', 'Éter', 'Morôni']
    
    pgp_books = ['Moisés', 'Abraão', 'Joseph Smith-Mateus', 'Joseph Smith-História', 'Regras de Fé']


eng = Eng
spa = Spa
pt = Pt


def lower_list(cap_list):
    low_list = []
    for item in cap_list:
        low_list.append(item.lower())
    return low_list


def lang_verify(lang):
    if lang in langs:
        return eval(lang)
    else:
        raise exceptions.InvalidLang('The language "{}" is not a valid language. Try one: {}.'.format(str(lang), str(langs)))


def match_scripture(book_name, lang):
    book_name = book_name.lower()
    scripture = ''
    
    if book_name in lower_list(lang.ot_books):
        scripture = 'ot'
        pos = item_position(book_name, lower_list(lang.ot_books))
        code = utils.ot_data.codes[pos]
    
    if book_name in lower_list(lang.nt_books):
        scripture = 'nt'
        
    if book_name in lower_list(lang.bofm_books):
        scripture = 'bofm'
        
    if book_name in lower_list(lang.pgp_books):
        scripture = 'pgp'
    
    raise exceptions.InvalidBook('The book \'{}\' does not exist.'.format(str(book_name)))


def item_position(item, list):
    n = -1
    
    for i in list:
        n += 1
        
        if i.lower() == item.lower():
            return n
    return -1


def translate_book_name(from_lang, to_lang, book_name):
    from_lang = lang_verify(from_lang)
    to_lang = lang_verify(to_lang)
    
    scripture = match_scripture(book_name, from_lang)
    
    if scripture == 'ot':
        position = item_position(book_name, from_lang.ot_books)
        if position != -1:
            return to_lang.ot_books[position]
            
    if scripture == 'nt':
        position = item_position(book_name, from_lang.nt_books)
        if position != -1:
            return to_lang.nt_books[position]
    
    if scripture == 'bofm':
        position = item_position(book_name, from_lang.bofm_books)
        if position != -1:
            return to_lang.bofm_books[position]
    
    if scripture == 'pgp':
        position = item_position(book_name, from_lang.pgp_books)
        if position != -1:
            return to_lang.pgp_books[position]
