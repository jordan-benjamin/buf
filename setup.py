from setuptools import setup, find_packages


with open("README.rst", "r") as file:
    long_description = file.read()

with open("LICENSE", "r") as file:
      license_text = file.read()

setup(name='buf',
      version='1.0.0a2',
      description='For easily making chemical buffers and solutions',
      long_description= long_description,
      long_description_content_type = "text/x-rst",
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
      ],
      keywords='buf chemistry buffer solution salt',
      # TODO: add URL
      author='Jordan Juravsky',
      author_email='jordan@mindcharger.com',
      packages=find_packages(),
      install_requires=['docopt==0.6.2', 'tabulate==0.8.2'],
      entry_points = {"console_scripts" : ["buf=buf.main:main"]},
      include_package_data = True)