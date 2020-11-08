import setuptools

setuptools.setup(
    name='apartment-backend',
    version='0.0.1',
    description='backend of web extension to look for aparts',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'apart = apartment_backend.__main__:main'
        ]
    }
)
