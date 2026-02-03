# Mention-Python

[![PyPI version](https://img.shields.io/pypi/v/mention.svg)](https://pypi.org/project/mention)
[![Build Status](https://travis-ci.org/mazi76erX2/mention-python.svg?branch=master)](https://travis-ci.org/mazi76erX2/mention-python)
[![codecov](https://codecov.io/gh/mazi76erX2/mention-python/branch/master/graph/badge.svg)](https://codecov.io/gh/mazi76erX2/mention-python)
[![Documentation Status](https://readthedocs.org/projects/mention-python/badge/?version=latest)](https://mention-python.readthedocs.org/en/latest)

**A Python wrapper around the Mention API.**

## Installation

```console
$ python3 -m pip install mention
```

```python
>>> from mention import FetchAMentionAPI
>>> first_mention = FetchAMentionAPI('access_token', 'account_id', 'alert_id', 'mention_id')
>>> first_mention_data = first_mention.query()
>>> title = first_mention_data['title']
```

## Examples

**Fetch all alerts of an account**

```python
>>> import mention
>>> allAlerts = mention.FetchAlertsAPI(access_token, account_id)
>>> data = nandosAlert.query()
>>> alertsList = data['alerts']
>>> alertsList[5]['alert']['name']
'Nandos'
>>> data['alert']['query']['included_keywords']
['Nandos', 'Flame-grilled Chicken', 'Peri-Peri Sauce']
```

**Fetch a mention**

```python
>>> nandosMention = mention.FetchAMentionAPI(access_token, account_id, alert_id, mention_id)
>>> data = nandosMention.query()
>>> data['title']
"Nando's launches their own food ordering app"
>>> data['description']
"Nando's has launched their own app that will allow people to order their favourite meal from the comfort of their own home."
>>> data['original_url']
'https://www.iol.co.za/business-report/technology/nandos-launches-their-own-food-ordering-app-18378360'
```

## Read More

- [Full Documentation](http://mention-python.readthedocs.org/en/latest/)
  - [Installation](http://mention-python.readthedocs.org/en/latest/pages/installation.html)
  - [Basic Usage](http://mention-python.readthedocs.org/en/latest/pages/quickstart.html)
  - [Contributing](http://mention-python.readthedocs.org/en/latest/pages/contributing.html)
```