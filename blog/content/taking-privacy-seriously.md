Title: We Take Your Privacy Seriously
Slug: taking-privacy-seriously
Date: 2013-08-02

A main concern from the beginning has been privacy. Everything is wrapped in
SSL, and because it uses OAuth under the covers, you'll never have to supply
foauth.org your password for any of your services. But that's not the only
aspect of the site that matters, when it comes to privacy.

Despite not giving foauth.org your password, you do grant the site access to
your accounts at other services, and you need to be confident that those
priveleges are used properly. To that end, foauth.org allows you to select
which permissions you authorize, wherever a service allows it.

In addition, foauth.org is entirely [open source](https://github.com/foauth/foauth.org),
allowing you to review the code and what it does, how it stores your
credentials and what it does and doesn't do with that information. If you're
uncomfortable with any aspect of the code, you're welcome to submit an issue or
even a pull request to suggest changes. If that's not enough, you can fork it
and run it yourself.

That last point has been important for a number of people already. Regardless
of the quality of the codebase, many people are understandably wary of giving a
third-party access to their data. Even though the code itself may be a good
steward of that information, code doesn't provide any guarantees about the
people behind it.

These concerns are completely valid, which is why I also built another project,
a [private OAuth proxy](https://github.com/foauth/oauth-proxy), built
specifically for running it yourself. There are a number of steps involved,
but it allows you to be in control of your own proxy, owning the data yourself.
It's designed to run on [Heroku](https://heroku.com/), and will work quite well
on their free tier.

Running your own proxy is a bit more complicated than using foauth.org though,
because you'll have to also manage your own application keys. You'll have to
sign up for developer accounts, register OAuth applications and enter your app
keys into the proxy configuration. When you use foauth.org, all these steps
have been done for you, so it's a trade-off between ownership and ease of use.

Inspecting traffic
------------------

On foauth.org itself, the Terms of Service forbid the service from inspecting
your API traffic beyond just the OAuth dance and storing your username with
each service. Any additional traffic is always passed through, unmonitored and
as unmodified as possible. Having your own private OAuth proxy allows you the
chance to see traffic in more detail if you'd like.

To that end, the private proxy supports simple [Runscope](http://runscope.com/)
integration to log your API traffic. To make it as easy as possible to work
with, [Runscope has a Heroku add-on](https://addons.heroku.com/runscope) that
you can install easily. Once you install it, your OAuth proxy will see that
and automatically send your requests through it.

## So which should you use?

Now you have two choices: the fully-managed foauth.org or your own self-hosted
OAuth proxy. They do most of the same things, so it can be hard to see why you
would choose one or the other. Essentially, it boils down to a tradeoff between
control and convenience. foauth.org provides some benefits and drawbacks:

* It's easy to setup, because everything can be done over the web.
* You don't need to register applications with each provider service.
* You're not in control of your own access keys; they're managed by foauth.org.
* You can't inspect any of the traffic going across the wire.
* You're sharing hosting resources with all other foauth.org users.

On the other hand, running your own has a different set of things to consider:

* You have full control over all your access keys.
* You can optionally inspect all your API traffic through Runscope.
* You can choose your own custom domain for your proxy.
* You get a dedicated set of hosting resources, which you can adjust yourself.
* You need to register an application with each service provider you'll use.
* The service is managed mostly in your terminal, using the Heroku toolbelt.

If you're just looking to get up and running quickly, foauth.org can be a great
way to determine if the process will work for you, even if you decline to grant
write access to your services. If you need more access than you're willing to
provide to a third-party, you ocan switch to running your own private proxy, as
long as you're willing to do some extra work to install and manage it.

I've tried to make the installation and management of the private proxy as easy
as possible, so that anyone who can work with a command-line interface should
be able to work with it just fine. In general use, it's probably a better
approach for most users' needs.

## Which one is better for production use?

This is difficult to answer, because terminology gets in the way. Most of the
time, "production use" refers to running a public-facing website that users can
rely on. I'd argue that neither of these offerings should ever be used in such
a case, but it's not because of reliability concerns.

These services are designed for use by individuals retrieving their own data.
Public sites with their own sets of users would be better served by having real
OAuth implementations designed specifically for the sites in question. This is
a stopgap for people *not* running a real site to get their data more easily.
If you're running a real site, your users deserve better integration than
you'll get from anything foauth can offer.