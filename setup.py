from setuptools import setup, find_packages


setup(name='python-forecastapp',
      version='0.3.3',
      description='Python wrapper for the Forecast API',
      author='Joe Joiner',
      author_email='joe@legato.digital',
      url='https://github.com/joejoinerr/python-forecastapp',
      packages=find_packages(),
      install_requires=[
        'requests',
      ])
