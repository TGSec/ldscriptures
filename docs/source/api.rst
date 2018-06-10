.. _api

LDSciptures API Reference
=========================

The complete public API reference for LDScriptures.

.. py:module:: ldscriptures

.. py:function:: ldscriptures.get(reference)

    Gets scriptural standard work text by using its reference.
    
    *reference*:
        A normal scriptural reference. It should follow one of the following patterns: "[Book Name] [Chapter]:[Verse]" or "[Book Name] [Chapter]"
        
        * *Book Name* is the name of the scriptural book. It supports any case-insensitive letter, whitespaces and numbers. Examples: "1 John", "Matthew", "Alma".
        
        * *Chapter* are the chapter or chapters. It supports any numbers. No white space allowed.
            * Range: the numbers before and after a hyphen determines a range of chapters. Examples: "1-3" (chapters 1, 2 and 3), "9-10" (chapters 9 and 10)
            
            * List: the comma determines a separator of chapters. Examples: "1,5,6" (1, 5 and 6), "8,37" (8 and 37).
            
            .. note::
                
                You can mix ranges and lists freely. Examples: "1-3,5" (1, 2, 3 and 5), "5-7,30,40-42" (5, 6, 7, 30, 40, 41 and 42)
            
            .. note::
                
                You can't use more than one chapter and determine any verse, or it will raise an exception. Examples: "John 5-6:7", "Matthew 3,5:2"
                
        * *Verse* are the verse or verses. Its specifications are the same of the *Chapter*'s specifications.
        
        Example of possible references: "Alma 5:10", "1 Nephi 3:7-8", "2 Nephi 32:3-5,7", "Relevation 10", "Jacob 3-5".
        
    The function returns a Chapter object or a list of Chapter objects (depending of the amount of defined chapters in the *reference* argument.

.. py:class:: Verse(brute_verse)

    A type class inherited from type *str* that represents a verse.
    
    .. py:attribute:: Verse.text
        
        Represents the text of the verse (excludes the verse number).
    
    .. py:attribute:: Verse.number
    
        Represents the number of the verse (excludes the verse text).

.. py:class:: Chapter()
    
    A type class inherited from type *list* that represets a list of verses of a chapter.
    
    .. py:attribute:: Chapter.reference
        
        TODO