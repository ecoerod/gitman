from setuptools import setup

setup(
    name='github-manager',
    version='0.2.1',
    description='Gitman - Simple CLI Github Repository Manager',
    url='https://github.com/Nelthorim/gitman',
    author='Eduardo Coello Rodriguez',
    author_email='ecoerod@gmail.com',
    license="MIT",
    keywords='git github repository manager',

    packages=['gitman'],

    install_requires=['requests>=.2.12'],

    entry_points={
        'console_scripts': [
            'gitman = gitman.__main__:main'
        ]
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ]

)
