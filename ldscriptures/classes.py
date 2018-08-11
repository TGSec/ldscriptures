

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
                exceptions.InvalidScriptureReference(
                    'all chapters must be int.')

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
            raise exceptions.InvalidScriptureReference(
                'Regex failure: \'{0}\' is not a valid reference.'.format(reference))

        _splited_reference = list(re.findall(patt, reference_str)[0])

        if ('-' in _splited_reference[1] or ',' in _splited_reference[1]) and len(_splited_reference[2]) > 0:
            raise exceptions.InvalidScriptureReference(
                'can\'t be set more than one chapter and be set a/some verse.')

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
            raise exceptions.InvalidScriptureReference(
                'can\'t be set more than one chapter and be set a/some verse.')
        if self.chapters == []:
            raise exceptions.InvalidScriptureReference(
                '"chapters" can\'t be of lenght 0.')
        for i in self.chapters:
            if type(i) != int:
                raise exceptions.InvalidScriptureReference(
                    '"chapters" must contain only ints.')
        return True

    # Function to convert a list of int() in a valid reference string. Basic "lexer".
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

        self.text = '{reference}\n\n{verses}'.format(
            reference=self.reference, verses=verses_text)


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
