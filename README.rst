Introduction
============

TTW template customization manager.

This package aims to bring support for TTW jbot (or "Just a bunch of templates")
support for Plone. jbot customizations can be added for each Plone site. There
is likely a minor performance impact on utilizing this product. No benchmarks
have been taken yet.

This package is an extension of z3c.jbot which allows you to do template
overrides in python packages for Plone.


JBOT with Diazo
---------------

All you need to do is install this package on a Plone site and then create
a `jbot` folder in your diazo theme.


Site customizations / JBOT without Diazo
----------------------------------------

Once you install the product on a Plone site, in `Site Setup`, there will
be a `jbot` control panel entry. From there, you can add your jbot
customizations for that site.

Lets say you want to override the footer template. Click the `Search
Resources` button, search for `footer`, and click the customize button
next to the template name in the search results. You can then make changes
to the template, save, and the changes will be visible in the site on refresh.



Conflicting customizations
--------------------------

If the same resource is customized at both the site and theme level, the theme
customization takes precedence.


Installation
------------

This implementation requires the use of the data directory of a running
Plone client. For most Plone installs, the directory used will be something
like `<buildout-dir>/var/instance/jbot`. The user running the Plone client
will need write access to this directory.


.. DANGER::
    The template customizations are not run in restricted python. Be sure to
    inspect any third party themes that utilize this. Additionally, be sure
    to trust site owner who will be adding their own customizations.


TODO
----
- plone 5 compatible
- decide core, installed by default
- potentially unify interface from resource registries
- improve ace edit integration
- mockup/theme editor like
- search needs to be able to filter by types
- filter out editable items that are not useful
- template registraiton information
- icons for files
- be able to export/import of the content
- indexing the contents so searching is by contents of them, not just the name
- versioning of customizations
