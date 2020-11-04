.. _installing:

Installing
==========

Before using the library, we need to install it.
The recommended installation method is the default Python module manager *pip*.
You can also install it by downloading the project in Github and running the setup.py.
Both methods will be explained in this article.

Installation via pip
--------------------

The most basic way of installing LDSCriptures is using pip:

.. code-block:: bash
   
   pip install ldscriptures
 
Of, if you want to update it:

.. code-block:: bash
   
   pip install -U ldscriptures

Installing via setup.py
-----------------------

But if you want to do it the hard way, you'll need to download the `zip file`__ containing the module, from Github.

__ https://github.com/TGSec/ldscriptures/archive/master.zip

Next, you need to extract the files. After extracting, you just need to run the following command in the directory that you extracted (replace "python" for you interpreter's executable):

.. code-block:: bash
   
   python setup.py install

Or, if you just want to build it:

.. code-block:: bash
   
   python setup.py build