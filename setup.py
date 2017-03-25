from setuptools import setup

# Get common version from version file.
exec(open('dupi/version.py').read())

setup(name='dupi',
      version=version_string(),
      description='File hash indexer for duplicate file finding.',
      url='https://github.com/jleverenz/dupi',
      author='Jeff Leverenz',
      author_email='jeff.leverenz@gmail.com',
      license='MIT',
      packages=['dupi'],
      entry_points = {
          'console_scripts': ['dupi=dupi.__main__:main'] },
      zip_safe=False)
