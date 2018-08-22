from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name = 'anywherepython',
		version = '0.0.1',
		description = 'Python library for interacting with the pythonanywhere API!',
		author = 'Szabó Dániel Ernő',
		author_email = 'r3ap3rpy@gmail.com',
		license = 'MIT',
		packages = ['anywherepython'],
		zip_safe = False,
		include_package_data=True,
		install_requires=[
          'requests',
      ],
	)