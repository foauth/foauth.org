Title: foauth.org: OAuth for one
Date: 2013-02-05
Slug: oauth-for-one
Summary: You don't need to deal with OAuth in order to get to your own data.

[OAuth](http://oauth.net/) is a complicated way for services to talk to each
other, but overall, it works pretty well. Unfortunately, its complexity makes
it difficult to implement even for seasoned programmers building a service.
It's that much harder to work with for individuals trying to get access to
their own data. Thankfully, that second point is something we can improve.

Because OAuth is designed for services to talk to each other, it's natural
that it would be difficult for individual users to work with it. But its very
nature as a service-oriented protocol offers a solution: a separate service
that sits between you and the services you're really trying to work with. It
could manage OAuth with other services, and provide you a simpler form of
authentication, which is easier to work with in simple scripts.

[foauth.org](https://foauth.org/) is the first service to do exactly that.
You can sign up for an account at foauth.org, then use the site to authorize
access to other services you'd like to work with. For many services, you even
get to choose what level of access you'd like to authorize. Then, you can make
requests using foauth.org as a proxy, providing simple credentials using HTTP
Basic authentication.

    >>> import requests
    >>> auth = 'email@example.com', 'password'
    >>> r = requests.get('https://foauth.org/api.twitter.com/1.1/statuses/user_timeline.json', auth=auth)
    >>> r.json()[0]['text']
    "Just signed up with https://foauth.org/"

------

[OAuth](http://oauth.net/) is pretty great. It's not a cure for cancer or
anything and it certainly has its warts, but as cross-site authorization
systems go, it's really pretty good. It allows one site to work with content
from users on another site, without those users having to give up their
login credentials. Instead, the sites pass around authorization tokens that
can expire or be revoked at any time, giving users a lot more control over
who has access to what.

That's all great when you're building a site that needs to access resources
from users on another site. But if you're a user of one of those sites, and
you want to get access to your own data, OAuth gets ... less great. There are
a number of steps you need to go through (which are often subtly different for
each site you want to interact with), but I won't list them all here because
there's something more pertinent:

> You don't need to deal with OAuth in order to get to your own data.

Today, I'm proud to announce [foauth.org](https://fouth.org/), my solution to
the problem of needing to use OAuth to get your own data. Essentially,
foauth.org sits between you and the sites you use, performing the "OAuth dance"
for you behind the scenes. You supply a username and password using HTTP Basic
authentication and foauth.org does the rest.

## Open source

Perhaps the most important thing about foauth.org is that it's completely
[open source](https://github.com/gulopine/foauth.org/). Feel free to run your
own instance if you want, or just use it as a reference for your OAuth client
implementation. But most importantly, you can help add to the list of supported
services.

Each OAuth provider is implemented as a Python class that includes all the
necessary details, including any aberrations from the spec. If you use a
service not currently supported on the site, you can code it up and open a pull
request to get it reviewed and merged. Not into Python? Feel free to file an
issue instead, so you can at least request it.

## Use it well
