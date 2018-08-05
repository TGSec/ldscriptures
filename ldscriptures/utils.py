import re

from . import exceptions


def string_range(string):
    string = string.split(',')

    num_list = []

    for each in string:
        # If sub-string is range. Just accept if there is just one
        if '-' in each and each.count('-') == 1 and each[0] != '-' and each[-1] != '-':
                                                                                          # "-" and if the first and last character aren't "-"
            splited = each.split('-')
            for num in range(int(splited[0]), int(splited[1])+1):
                num_list.append(num)

        else:
            num_list.append(int((each)))

    num_list.sort()

    return num_list


def better_capitalize(text):
    splited = text.split(' ')
    final = ''
    for part in splited:
        final = final + ' ' + part.capitalize()
    return final.strip()


def reference_split(reference):
    patt = '^(.+) ((?:[0-9]+(?:-[0-9]+)?,?)*)(?::((?:[0-9]+(?:-[0-9]+)?,?)*))?$'

    if re.match(patt, reference):
        splited = list(re.findall(patt, reference)[0])

        if ('-' in splited[1] or ',' in splited[1]) and len(splited[2]) > 0:
            raise exceptions.InvalidScriptureReference(
                'Can not exist range or list in chapter and exist verse.')

        else:
            splited[1] = string_range(splited[1])
            if splited[2] != '':
                splited[2] = string_range(splited[2])
            else:
                splited[2] = []

            return splited

    else:
        raise exceptions.InvalidScriptureReference(
            'Regex failure: \'{0}\' is not a valid reference.'.format(reference))


scriptures_url_base = 'https://www.lds.org/scriptures'

chapter_numbers = {
    'bofm': {'1-ne': '22',
             '2-ne': '33',
             '3-ne': '30',
             '4-ne': '1',
             'alma': '63',
             'enos': '1',
             'ether': '15',
             'hel': '16',
             'jacob': '7',
             'jarom': '1',
             'morm': '9',
             'moro': '10',
             'mosiah': '29',
             'omni': '1',
             'w-of-m': '1'},
    'dc-testament': {'dc': 138},
    'nt': {' 1-tim': '6',
           '1-cor': '16',
           '1-jn': '5',
           '1-pet': '5',
           '1-thes': '5',
           '2-cor': '13',
           '2-jn': '1',
           '2-pet': '3',
           '2-thes': '3',
           '2-tim': '4',
           '3-jn': '1',
           'acts': '28',
           'col': '4',
           'eph': '6',
           'gal': '6',
           'heb': '13',
           'james': '5',
           'john': '21',
           'jude': '1',
           'luke': '24',
           'mark': '16',
           'matt': '28',
           'philem': '1',
           'philip': '4',
           'rev': '22',
           'rom': '16',
           'titus': '3'},
    'ot': {'1-chr': '29',
           '1-kgs': '22',
           '1-sam': '31',
           '2-chr': '36',
           '2-kgs': '25',
           '2-sam': '24',
           'amos': '9',
           'dan': '12',
           'deut': '34',
           'eccl': '12',
           'esth': '10',
           'ex': '40',
           'ezek': '48',
           'ezra': '10',
           'gen': '50',
           'hab': '3',
           'hag': '2',
           'hosea': '14',
           'isa': '66',
           'jer': '52',
           'job': '42',
           'joel': '3',
           'jonah': '4',
           'josh': '24',
           'judg': '21',
           'lam': '5',
           'lev': '27',
           'mal': '4',
           'micah': '7',
           'nahum': '3',
           'neh': '13',
           'num': '36',
           'obad': '1',
           'prov': '31',
           'ps': '150',
           'ruth': '4',
           'song': '8',
           'zech': '14',
           'zeph': '3'},
    'pgp': {'a-of-f': '1', 'abr': '5', 'js-h': '1', 'js-m': '1', 'moses': '8'}
}
