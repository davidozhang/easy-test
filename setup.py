try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

setup (name='easy-test',
    version='1.6',
    py_modules=['easy_test'],
    description='Easy test-running and editing of test input and solutions.',
    author='David Zhang',
    author_email='davzee@hotmail.com',
    url='http://github.com/davidozhang/easy-test',
    install_requires=['pexpect==3.3'],
)
