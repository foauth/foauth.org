foauth.org makes OAuth optional
===============================

`OAuth`_ is a great idea for interaction between big sites with lots of users.
But, as one of those users, it's a pretty terrible way to get at your own data.
That's where foauth.org comes in, giving you access to these services using
HTTP Basic, which is easily available in hundreds of existing tools, such as
`requests`_::

  >>> import json, requests
  >>> basic = 'email@example.com', 'password'
  >>> r = requests.get('https://foauth.org/api.twitter.com/1/statuses/home_timeline.json', auth=basic)
  >>> timeline = json.loads(r.content)
  >>> timeline[0]['text']
  "Just signed up with http://foauth.org/ and it's awesome! Thanks @Gulopine and @kennethreitz!"

Implementation
--------------

foauth.org uses the OAuth support from `requests`_ (powered by `oauthlib`_) to
handle the OAuth signatures, behind `Flask`_ for interacting with users.
Currently, requests and oauthlib only fully support OAuth 1.0, so the current
crop of supported providers only includes those that use 1.0. Once requests and
oauthlib land full support for OAuth 2.0, another list of providers can be
added as well.

Providers themselves are implemented as Python classes that inherit from base
OAuth support. This means that new providers can be requested and added using
GitHub's pull requests. Documentation for how to define these provider classes
is still forthcoming.

.. _OAuth: http://oauth.net/
.. _requests: https://github.com/kennethreitz/requests
.. _oauthlib: https://github.com/idan/oauthlib
.. _Flask: https://flask.pocoo.org/
