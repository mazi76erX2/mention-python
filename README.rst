==============
Mention-Python
==============

.. image:: https://img.shields.io/pypi/v/MentionAPI.svg
    :target: https://pypi.python.org/pypi/MentionAPI

.. image:: https://travis-ci.org/mazi76erX2/mention-python.svg?branch=master
    :target: https://travis-ci.org/mazi76erX2/mention-python

.. image:: https://coveralls.io/repos/github/mazi76erX2/mention-python/badge.svg?branch=master
:target: https://coveralls.io/github/mazi76erX2/mention-python?branch=master


.. image:: https://readthedocs.org/projects/mention/badge/?version=latest
    :target: https://mention.readthedocs.org/en/latest

**A Python wrapper around the Mention API.**

Installation
------------

.. code-block:: console

    $ python3 -m pip install mention


.. code-block:: python

    >>> from mention import FetchAMentionAPI
    >>> first_mention = FetchAMentionAPI('access_token', 'account_id', 'alert_id', 'mention_id')

    >>> first_mention_data = first_mention.query()

    >>> title = first_mention_data['title']

Examples
--------

**Fetch all alerts of an account**

.. code-block:: python

    >>> allAlerts = mention.FetchAlertsAPI(access_token,
    							 		   account_id)

    >>> data = nandosAlert.query()

    >>> alertsList = data['alerts']	
    >>> alertsList[5]['alert']['name']
    >>> 'Nandos'			 			

    >>> data['alert']['query']['included_keywords']
    >>> ['Nandos', 'Flame-grilled Chicken', 'Peri-Peri Sauce']

**Fetch a mention**

.. code-block:: python

    >>> nandosMention = mention.FetchAMentionAPI(access_token,
    							 			  	 account_id,
    							 			  	 alert_id,
    							 			  	 mention_id)

    >>> data = nandosMention.query()

    >>> data['title']					 			
    >>> 'Nando's launches their own food ordering app'

    >>> data['description']				 			
    >>> 'Nando's has launched their own app that will allow people to order their favourite meal from the comfort of their own home.'

    >>> data['original_url']				 			
    >>> 'https:\/\/www.iol.co.za\/business-report\/technology\/nandos-launches-their-own-food-ordering-app-18378360'


 - `Full Documentation`_
     - `Installation`_
     - `Basic Usage`_
     - `Contributing`_

.. _Full Documentation: http:///mention-python.readthedocs.org/en/latest/
.. _Installation: http://mention-python.readthedocs.org/en/latest/pages/installation.html
.. _Basic Usage: http:///mention-python.readthedocs.org/en/latest/pages/quickstart.html
.. _Contributing: http:///mention-python.readthedocs.org/en/latest/pages/contributing.html