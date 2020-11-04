.. _usage:

Usage/Tutorial
==============

Ok, you liked the library, but you want to really start using it. Let's start!

The get() function
------------------

The most basic and important thing you expect from a library that request and parses scriptural texts is a easy way of doing so. That's exactly what the :any:`get` function does.
Let's start with a simple example:

.. code-block:: python
   
   import ldscriptures as lds
   
   scripture = lds.get('2 Nephi 28:30')
   
   print(scripture.text)

Output:

.. code-block:: text
    
    2 Nephi 28
    
    30 For behold, thus saith the Lord God: I will give unto the children of men line upon line, precept upon precept, here a little and there a little; and blessed are those who hearken unto my precepts, and lend an ear unto my counsel, for they shall learn wisdom; for unto him that receiveth I will give more; and from them that shall say, We have enough, from them shall be taken away even that which they have.


Ok, it's kind a simple function, but I'll explain everything is happenning here. In the first line, we import the ldscriptures module with the lds shortname. I did it for making the code
easier to read, but it's optional.

Then, in the second line we use the :any:`get()` function for requesting for "2 Nephi 28:30", and the `Scripure` object result we put at the `scripture` variable.

In the last line we printed the "text" attribute of "chapter", wich is represented in the output above.

Acessing informations of the verses
-----------------------------------

If you want to retrieve the original html of each verse, you can access the :any:`.html` attribute of the Verse object.

.. code-block:: python
    import ldscriptures as lds

    verse = lds.get('Matthew 5:14')[0]

    print(verse.html)

You can also use the :any:`.full`, :any:`.content` or :any:`number` attributes to get other important info about the verse.

The Reference class
----------------------

This is a powerful class that let's you access the chapters, verses and scriptural book of a given valid reference (e.g. Ether 12:24). Example:

.. code-block:: python
    import ldscriptures as lds

    ref = lds.Reference('Enos 1:4-8')

    print('Book: {}'.format(ref.book))

    print('Chapter: {}'.format(str(ref.chapter).replace(']','').replace('[', '')))

    print('Verses: {}'.format(str(ref.verse).replace(']','').replace('[', '')))

Output:

.. code-block:: text
    Book: Enos
    Chapter: 1
    Verses: 4, 5, 6, 7, 8
