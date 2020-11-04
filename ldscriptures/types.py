import re

from .utils import *


class Reference(dict):
    pattern_without_verse = '^([0-9]* ?.+) ([0-9-,]+)$'
    pattern_with_verse = '^([0-9]* ?.+) ([0-9]+):([0-9-,]+)$'

    _splited_reference = []
    
    def __init__(self, reference_string):
        self.text = reference_string

        if re.match(self.pattern_without_verse, reference_string):
            book, chapter = re.findall(self.pattern_without_verse, reference_string)[0]

            chapter = self._string_range(chapter)

            self.book = book
            self.chapter = chapter
            self.verse = []

        elif re.match(self.pattern_with_verse, reference_string):
            book, chapter, verse = re.findall(self.pattern_with_verse, reference_string)[0]

            chapter = [int(chapter)]
            verse = self._string_range(verse)

            self.book = book
            self.chapter = chapter
            self.verse = verse
        else:
            raise exceptions.InvalidScriptureReference('Is "{}" a valid referene?'.format(reference_string))

    def _string_range(self, string):
        divided = string.split(',')

        num_list = []

        for each in divided:
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


    # Method to convert a list of int() in a valid reference string.
    def _list_to_str(self, list):
        seq = []
        ranged_ref = []
        list = sorted(set(list))  # For ordering and removing repeated items
        last = -1

        for item in list:
            if seq == []:  # If no seq started
                seq.append(item)
            elif len(seq) > 0 and item == last+1:  # If seq started and item is last+1
                seq.append(item)
            # If seq less or equal to 2 and item not equal to last=1
            elif len(seq) <= 2 and item != last+1:
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
        if self.verse == []:
            return '{book} {chapter}'.format(book=self.book, chapter=self._list_to_str(self.chapter))
        elif len(self.verse) != 0:
            return '{book} {chapter}:{verse}'.format(book=self.book, chapter=self.chapter[0], verse=self._list_to_str(self.verse))

    def __repr__(self):
        return '<Reference: ' + self.__str__() + '>'


class Scripture(list):

    def __new__(self, reference, verses):
        return list.__new__(self, verses)

    def __init__(self, reference, verses):
        list.__init__(self, verses)
        self.reference = reference

        verses_text = ''

        for verse in verses:
            verses_text = verses_text + verse.full + '\n'

        verses_text = verses_text.strip()

        self.text = '{reference}\n\n{verses}'.format(
            reference=self.reference, verses=verses_text)


class Verse:
    def __init__(self, html):
        self.html = html
        for tag in html.find_all('sup'):
            tag.clear()
        self.number, self.content = html.get_text().strip().split(' ', 1)
        self.number = int(self.number)
        self.full = html.text
        
