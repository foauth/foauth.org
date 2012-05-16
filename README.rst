foauth.org makes OAuth optional
===============================

`OAuth`_ is a great idea for interaction between big sites with lots of users. But, as
one of those users, it’s a pretty terrible way to get at your own data. That’s where
foauth.org comes in, giving you access to these services using HTTP Basic, which is
easily available in hundreds of existing tools, such as `requests`_::

  >>> import json, requests
  >>> basic = 'email@example.com', 'password'
  >>> r = requests.get('https://foauth.org/api.twitter.com/1/statuses/home_timeline.json', auth=basic)
  >>> timeline = json.loads(r.content)
  >>> timeline[0]['text']
  "Just signed up with http://foauth.org/ and it's awesome! Thanks @kennethreitz and @Gulopine!"

.. _OAuth: http://oauth.net/
.. _requests: https://github.com/kennethreitz/requests

Implementation
--------------

TBD.

I'd love to see it be 100% an API. Users can register new apps

Perhaps it would ship with an 'foauth-client' module that wraps requests that allows usersto hit any fo the registered sites *super* easily.




* Flask + SQLAlchemy
* Heroku
* Ideally, Requests+idan's module.
