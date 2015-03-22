import __builtin__
import sys
import os

from nose.tools import assert_equal
from testfixtures import TempDirectory
from mock import patch

from easy_test import EasyTest

def test_basic_instantiate():
	temp = TempDirectory()
	e = EasyTest(path=temp.path, test=True)
	assert_equal(e.base_dir, temp.path+'/')
	assert_equal(e.base_tests, e.base_dir+'tests/')
	temp.cleanup()

def test_session_with_valid_target():
	temp = TempDirectory()
	temp.write('test.py', b'some text')
	e = EasyTest(path=temp.path, test=True)
	with patch('__builtin__.raw_input', return_value='test.py'):
		e._session()
		assert_equal(e.target_name, 'test.py')
		assert_equal(e.strip_ext, 'test')
		assert_equal(e.base_tests_target, e.base_tests+e.strip_ext+'/')
		assert_equal(e.target, e.base_dir+e.target_name)
	temp.cleanup()

def test_session_with_invalid_target():
	temp = TempDirectory()
	temp.write('test.py', b'some text')
	e = EasyTest(path=temp.path, test=True)
	# Make sure no test target directory gets created
	e.base_tests_target = None
	with patch('__builtin__.raw_input', return_value='test2.py'):
		e._session()
		assert_equal(e.base_tests_target, None)
	temp.cleanup()

def test_compile():
	temp = TempDirectory()
	temp.write('test.cc', b'int main() {}')
	e = EasyTest(path=temp.path, test=True)
	e.target_name = 'test.cc'
	e.target = e.base_dir + e.target_name
	e.strip_ext = 'test'
	c = e._compile()
	assert_equal(c, True)
	assert_equal(e.target, e.base_dir+'test')
	assert_equal(e.target_name, 'test')
	temp.cleanup()

def test_compile_with_issue():
	temp = TempDirectory()
	#Purposefully omit param brackets
	temp.write('test.cc', b'int main {}')
	e = EasyTest(path=temp.path, test=True)
	e.target_name = 'test.cc'
	e.target = e.base_dir + e.target_name
	e.strip_ext = 'test'
	c = e._compile()
	assert_equal(c, False)
	temp.cleanup()

def test_not_compile():
	temp = TempDirectory()
	temp.write('test.py', b'int main:')
	e = EasyTest(path=temp.path, test=True)
	e.target_name = 'test.py'
	e.target = e.base_dir + e.target_name
	e.strip_ext = 'test'
	c = e._compile()
	assert_equal(c, True)
	assert_equal(e.target, e.base_dir+'test.py')
	assert_equal(e.target_name, 'test.py')
	temp.cleanup()

def test_testing_no_slaves():
	temp = TempDirectory()
	temp.write('test.py', b'int main:')
	temp.makedir(('tests','test'))
	e = EasyTest(path=temp.path, test=True)
	e.target_name = 'test.py'
	e.base_tests_target = e.base_tests + 'test/'
	t = e._test()
	assert_equal(t, False)
	temp.cleanup()
