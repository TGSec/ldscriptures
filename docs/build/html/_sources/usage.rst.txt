.. _usage:

Usage/Tutorial
==============

Ok, you did like the library, but you want to really start using it. Let's start!

The get() function
------------------

The most basic thing you expect from a library that request and parses scriptural texts is a easy way of doing so. That's exactly what the :any:`get` function does.
Let's start with a simple example:

.. code-block:: python
   
   import ldscriptures as lds
   
   chapter = lds.get('2 Nephi 28:30')
   
   print(chapter.text)

Output:

.. code-block:: text
    
    2 Nephi 28
    
    30 For behold, thus saith the Lord God: I will give unto the children of men line upon line, precept upon precept, here a little and there a little; and blessed are those who hearken unto my precepts, and lend an ear unto my counsel, for they shall learn wisdom; for unto him that receiveth I will give more; and from them that shall say, We have enough, from them shall be taken away even that which they have.


Ok, it's kind a simple function, but I'll explain everything is happenning here. In the first line, we import the ldscriptures module with the lds shortname. I did it for making the code
easier to read, but it's optional.

Then, in second line we use the :any:`get` function for requesting for "2 Nephi 28:30", and the chapter object result we put at the "chapter" variable.

In the last line we printed the "text" attribute of "chapter", wich is represented in the output above.