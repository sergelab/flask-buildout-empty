
from setuptools import setup, find_packages

setup_args = dict(
    name = 'sergelab',
    version = '0.1',
    author = 'Brandproduction Ltd.',
    author_email = 'info@brpr.ru',
    url = '',
    description = 'Flask sergelab project',
    long_description = open('README.md').read(),
    install_requires = [
        'setuptools',
        'zc.buildout',
    ],
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    zip_safe = True
)

if __name__ == '__main__':
    setup(**setup_args)

