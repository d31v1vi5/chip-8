from setuptools import setup, find_packages

setup(
    name='chip8',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'chip8 = src.emulator:emulator',
        ],
    },
)