Introduction
============

TTW template customization manager.

This package aims to bring support for TTW jbot(or "Just a bunch of templates")
support for Plone. jbot customizations can be added for each plone site. There
is likely a minor performance impact on utilizing this product. No benchmarks
have been taken yet.

This package is an extension of z3c.jbot which allows you to do template
overrides in python packages for Plone.


JBOT with Diazo
---------------

All you need to do is install this package on a plone site and then create
a `jbot` folder in your diazo theme.


JBOT without Diazo
------------------

Just add a file with the dotted name in the control panel.
Lets say you want to override the serch template. You first go to /portal_view_customization, 
click on the template you want to override and look at the name. In this case it would be:
plone.app.search.search.pt.
Add a file with this name, thats all.


Site customizations
-------------------

Once you install the product on a plone site, in `Site Setup`, there will
be a `jbot` control panel entry. From there, you can add your jbot
customizations for that site.


Conflicting customizations
--------------------------

If the same resource is customized at both the site and theme level, the theme
customization takes precedence.


Installation
------------

This implementation requires the use of the data directory of a running
plone client. For most plone installs, the directory used will be something
like `<buildout-dir>/var/instance/jbot`. The user running the plone client
will need write access to this directory.


.. DANGER::
    The template customizations are not run in restricted python. Be sure to
    inspect any third party themes that utilize this. Additionally, be sure
    to trust site owner who will be adding their own customizations.
