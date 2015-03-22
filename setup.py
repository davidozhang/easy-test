try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

setup (
    name='easy-test',
    version='2.0',
    py_modules=['easy_test'],
    description='Easy test-running and editing of test input and solutions.',
    author='David Zhang',
    author_email='davzee@hotmail.com',
    url='http://github.com/davidozhang/easy-test',
    install_requires=[
        'pexpect==3.3',
        'termcolor==1.1.0',
        'testfixtures==4.1.2',
        'mock==1.0.1',
    ],
)
