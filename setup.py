from setuptools import setup, find_packages

setup(
    name="Optima",
    version="1.0.5",
    authors="In CODE we trust",
    description="Optima - an interactive assistant for managing notes and contacts",
    long_description="""Optima is a command-line assistant that allows you to store,
                      edit, search, and manage notes and contacts.
                      It features a convenient interface and easy integration with your system.
                      Developed by Yulia Chorna, Valentyn Tonkonig, Anastasia Makarova,
                      Ryslan Shypka, Vita Filimonikhina, Roman Synyshyn.""",
    url="https://github.com/YuliiaChorna1/OPTIMA",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'optima = Optima.main:main',
        ],
    },
    python_requires='>=3.6',
    include_package_data=True
)