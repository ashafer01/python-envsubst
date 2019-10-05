from setuptools import setup

with open('README.rst') as f:
    long_desc = f.read()

setup(
    name='envsubst',
    version='0.1.5',
    description='Substitute environment variables in a string',
    long_description=long_desc,
    author='Alex Shafer',
    author_email='ashafer@pm.me',
    url='https://github.com/ashafer01/python-envsubst',
    license='MIT',
    py_modules=['envsubst'],
    entry_points={
        'console_scripts': [
            'envsubst = envsubst:main',
        ],
    },
)
