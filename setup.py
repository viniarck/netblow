from setuptools import setup
from netblow.version import __version__
desc = 'Vendor agnostic network testing framework to stress network failures'

setup(
    name='netblow',
    version=__version__,
    description=desc,
    author='Vinicius Arcanjo',
    author_email='viniciusarcanjov@gmail.com',
    keywords='network testing netblow napalm eos junos ios iosxr',
    url='http://github.com/viniciusarcanjo/netblow',
    packages=['netblow', 'netblow/monkey_patch', 'netblow/bin'],
    license='Apache',
    install_requires=['napalm==2.3.1', 'coloredlogs'],
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    entry_points='''
        [console_scripts]
        netblow=netblow.bin.netblow_cli:main
    ''',
    zip_safe=False,
)
