import re

from . import exceptions

scriptures_url_base = 'https://www.churchofjesuschrist.org/study/scriptures/'

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
    "dc-testament": {'dc': 138},
    
    "pgp": {
        "moses": 8,
        "abr": 5,
        "js-m": 1,
        "js-h": 1,
        "a-of-f": 1
    }
}