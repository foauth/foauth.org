Title: Introducing foauth.org
Slug: introducting-foauth
Date: 2013-08-01

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

To my knowledge, foauth.org is the first service to do exactly that. You can
sign up for an account here, then use authorize access to other services you'd
like to work with. For many services, you even get to choose what level of
access you'd like to authorize. Then, you can make requests using foauth.org as
a proxy, providing simple credentials using HTTP Basic authentication.

    >>> import requests
    >>> auth = 'email@example.com', 'password'
    >>> r = requests.get('https://foauth.org/api.twitter.com/1/statuses/user_timeline.json', auth=auth)
    >>> r.json()[0]['text']
    "Just signed up with https://foauth.org/ and it's awesome! Thanks @Gulopine!"

## Sponsorship

Because of its nature, foauth.org doesn't have a business plan; making money
isn't the goal. The site is instead supported by sponsors with an interest in
giving back to open source projects like this.

The first sponsor is [Heroku](https://heroku.com/), who have graciously donated
the resources to host the site on their platform. They cover all hosting costs,
including the web dynos, production-quality database and SSL support.
Indirectly, they also support the private OAuth proxy, because it's built to
run on their free tier. More on that in the [next post](/blog/taking-privacy-seriously/).

The second sponsor to join up is [Runscope](https://runscope.com/), who have
donated financially. Their generous sponsorship will hopefully be used to fund
developer accounts with services that require them, so that you don't need to
pay for a separate account in order to access your data. The availability of
this as an option will depend on the terms and conditions set forth by each
service.

If you'd like to help your yourself, you can also donate directly, which will
help me justify the time I spend working on the site. You can either donate
[directly to foauth.org](https://gumroad.com/l/rWgD) using Gumroad, or you can
instead [support me](https://gittip.com/gulopine) and all my projects using
Gittip.

## Use it well

So if you're interested in accessing your data from your favorite services, and
you don't want to deal with OAuth, you have a couple new options to do so.
Whether you choose to run your own or let foauth.org handle the bulk of it, you
can connect to nearly 60 services, and plenty more are planned.

In addition, foauth.org is entirely [open source](https://github.com/foauth/foauth.org),
allowing you to review the code and what it does, how it stores your
credentials and what it does and doesn't do with that information. If you're
uncomfortable with any aspect of the code, you're welcome to submit an issue or
even a pull request to suggest changes.

Please feel free to report any bugs or other problems you encounter and don't
be afraid to ask for new services. I'm working on more documentation, which
should help explain the process of writing a new provider class, so you can
even submit useful pull requests to support new services.
