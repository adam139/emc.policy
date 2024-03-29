from setuptools import setup, find_packages
import os

version = '2.0'

setup(name='emc.policy',
      version=version,
      description="A plone5 website policy package for emc project",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='python plone',
      author='Adam tang',
      author_email='568066794@qq.com',
      url='https://github.com/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['emc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'collective.autopermission',
          'z3c.jbot',
          'z3c.unconfigure',
          'collective.wtf',
          'collective.monkeypatcher',
          'collective.filepreviewbehavior',
                    
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': ['plone.app.testing',]
          },        
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
