from setuptools import setup


setup(name='python-forecastapp',
      version='0.1.1',
      description='Python wrapper for the Forecast API',
      author='Joe Joiner',
      author_email='joe@legato.digital',
      url='https://github.com/joejoinerr/python-forecastapp',
      packages=['forecast'],
      install_requires=[
        'requests',
      ])
