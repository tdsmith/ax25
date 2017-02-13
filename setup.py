from setuptools import setup

versionfile = 'ax25/version.py'
with open(versionfile, 'rb') as f:
    exec(compile(f.read(), versionfile, 'exec'))

setup(
    name='ax25',
    version=__version__,  # noqa
    url='https://github.com/tdsmith/ax25',
    license='MIT',
    author='Tim D. Smith',
    author_email='tim@tim-smith.us',
    description='Parses AX25 packets',
    packages=['ax25'],
    install_requires=['attrs'],
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points={'console_scripts': [
        'ax25_parse=ax25.util:parse_main',
    ]}
)
