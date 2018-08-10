from setuptools import setup, find_packages


with open("README.rst", "r") as file:
    long_description = file.read()

setup(name='buf',
      version='1.0',
      description='For easily making chemical buffers and solutions',
      long_description= long_description,
      # TODO: more classifiers? license?
      classifiers=[
        'Programming Language :: Python :: 3.6',
      ],
      keywords='buf chemistry solution salt',
      # TODO: add URL
      author='Jordan Juravsky',
      author_email='jordan@mindcharger.com',
      # TODO: license kwarg
      packages=find_packages(exclude=["tests"]),
      install_requires=['docopt', 'tabulate'],
      entry_points = {"console_scripts" : ["buf=buf.main:main"]},
      include_package_data = True)