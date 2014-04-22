from setuptools import setup, find_packages
import os

version = '1.0a1'

setup(name='collective.jbot',
      version=version,
      description="",
      long_description="%s\n%s" % (
          open("README.rst").read(),
          open(os.path.join("docs", "HISTORY.txt")).read()
      ),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
      ],
      keywords='plone templates customizations',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='https://github.com/collective/collective.jbot',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'z3c.jbot',
          'five.globalrequest',
          'plone.app.theming',
          'plone.resource'
      ],
      extras_require={
          'test': [
              'plone.app.testing',
          ]
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
