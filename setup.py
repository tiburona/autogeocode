from setuptools import setup

setup(name='autogeocode',
      version='0.1',
      description='A utility to fetch geocode data for a spreadsheet with location ',
      url='https://github.com/tiburona/map-collections-autogeocode',
      author='Katie Surrence',
      author_email='tiburona@gmail.com',
      license='MIT',
      packages=['autogeocode'],
      install_requires=[
            'googlemaps',
            'unicodecsv'
      ],
      entry_points = {
         'console_scripts': ['autogeocode=autogeocode.command_line:main']
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)