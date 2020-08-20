from setuptools import setup

setup(name='crs_relate_plugin',
    version='0.0.1',
    description='pygeoapi plugin for checking DE-9IM relathionship tests between WKT geometries and their declared CRS',
    url='https://github.com/manaakiwhenua/crs-relate-plugin',
    author='Richard Law',
    author_email='lawr@landcareresearch.co.nz',
    license='MIT',
    packages=['crs_relate_plugin'],
    install_requires=[
        'pyproj>=2.6.1.post1', 'shapely>=1.7.0'
    ],
    zip_safe=False
)
