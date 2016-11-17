from setuptools import setup

setup(
    name='gitman',
    version='0.1',
    description='Simple CLI Github Repository Manager',
    url='https://github.com/Nelthorim/gitman',
    author='Eduardo Coello Rodriguez',
    author_email='ecoerod@gmail.com',
    license="MIT",
    keywords='git github repository manager',

    packages=['gitman'],

    install_requires=['requests>=2.12'],

    entry_points={
        'console_scripts': [
            'gitman = gitman.__main__:main'
        ]
    }

)
