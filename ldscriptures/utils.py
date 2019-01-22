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
    "ot": {
        "gen": "50",
        "ex": "40",
        "lev": "27",
        "num": "36",
        "deut": "34",
        "josh": "24",
        "judg": "21",
        "ruth": "4",
        "1-sam": "31",
        "2-sam": "24",
        "1-kgs": "22",
        "2-kgs": "25",
        "1-chr": "29",
        "2-chr": "36",
        "ezra": "10",
        "neh": "13",
        "esth": "10",
        "job": "42",
        "ps": "150",
        "prov": "31",
        "eccl": "12",
        "song": "8",
        "isa": "66",
        "jer": "52",
        "lam": "5",
        "ezek": "48",
        "dan": "12",
        "hosea": "14",
        "joel": "3",
        "amos": "9",
        "obad": "1",
        "jonah": "4",
        "micah": "7",
        "nahum": "3",
        "hab": "3",
        "zeph": "3",
        "hag": "2",
        "zech": "14",
        "mal": "4"
    },
    "nt": {
        "matt": "28",
        "mark": "16",
        "luke": "24",
        "john": "21",
        "acts": "28",
        "rom": "16",
        "1-cor": "16",
        "2-cor": "13",
        "gal": "6",
        "eph": "6",
        "philip": "4",
        "col": "4",
        "1-thes": "5",
        "2-thes": "3",
        " 1-tim": "6",
        "2-tim": "4",
        "titus": "3",
        "philem": "1",
        "heb": "13",
        "james": "5",
        "1-pet": "5",
        "2-pet": "3",
        "1-jn": "5",
        "2-jn": "1",
        "3-jn": "1",
        "jude": "1",
        "rev": "22"
    },
    "bofm": {
        "1-ne": "22",
        "2-ne": "33",
        "jacob": "7",
        "enos": "1",
        "jarom": "1",
        "omni": "1",
        "w-of-m": "1",
        "mosiah": "29",
        "alma": "63",
        "hel": "16",
        "3-ne": "30",
        "4-ne": "1",
        "morm": "9",
        "ether": "15",
        "moro": "10"
    },
    "dc-testament": {'dc': 138}
}