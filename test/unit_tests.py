# -*- coding: utf-8 -*-

import __builtin__
import os
import unittest

from testfixtures import TempDirectory
from mock import patch

from easy_test import EasyTest


class EasyTestUnitTests(unittest.TestCase):

    def setUp(self):
        self.configs = {
            'server-ip': '1.2.3.4',
            'test-directory': None,
            'editor': 'subl',
        }

    def test_basic_instantiate_with_path(self):
        temp = TempDirectory()
        e = EasyTest(path=temp.path, test=True)
        self.assertEqual(e.base_dir, temp.path+'/')
        self.assertEqual(e.base_tests, e.base_dir+'tests/')
        temp.cleanup()

    def test_basic_instantiate_with_config_file(self):
        temp = TempDirectory()
        self.configs['test-directory'] = temp.path
        e = EasyTest(configs=self.configs, test=True)
        self.assertEqual(e.base_dir, temp.path+'/')
        self.assertEqual(e.base_tests, e.base_dir+'tests/')
        self.configs['test-directory'] = None
        temp.cleanup()

    def test_session_with_valid_target(self):
        temp = TempDirectory()
        temp.write('test.py', b'some text')
        e = EasyTest(path=temp.path, test=True)
        with patch('__builtin__.raw_input', return_value='test.py'):
            e._session()
            self.assertEqual(e.target_name, 'test.py')
            self.assertEqual(e.strip_ext, 'test')
            self.assertEqual(e.base_tests_target, e.base_tests+e.strip_ext+'/')
            self.assertEqual(e.target, e.base_dir+e.target_name)
        temp.cleanup()

    def test_session_with_invalid_target(self):
        temp = TempDirectory()
        temp.write('test.py', b'some text')
        e = EasyTest(path=temp.path, test=True)
        # Make sure no test target directory gets created
        e.base_tests_target = None
        with patch('__builtin__.raw_input', return_value='test2.py'):
            e._session()
            self.assertEqual(e.base_tests_target, None)
        temp.cleanup()

    def test_compile(self):
        temp = TempDirectory()
        temp.write('test.cc', b'int main() {}')
        e = EasyTest(path=temp.path, test=True)
        e.target_name = 'test.cc'
        e.target = e.base_dir + e.target_name
        e.strip_ext = 'test'
        c = e._compile()
        self.assertTrue(c)
        self.assertEqual(e.target, e.base_dir+'test')
        self.assertEqual(e.target_name, 'test')
        temp.cleanup()

    def test_compile_with_issue(self):
        temp = TempDirectory()
        # Purposefully omit param brackets
        temp.write('test.cc', b'int main {}')
        e = EasyTest(path=temp.path, test=True)
        e.target_name = 'test.cc'
        e.target = e.base_dir + e.target_name
        e.strip_ext = 'test'
        c = e._compile()
        self.assertFalse(c)
        temp.cleanup()

    def test_not_compile(self):
        temp = TempDirectory()
        temp.write('test.py', b'int main:')
        e = EasyTest(path=temp.path, test=True)
        e.target_name = 'test.py'
        e.target = e.base_dir + e.target_name
        e.strip_ext = 'test'
        c = e._compile()
        self.assertTrue(c)
        self.assertEqual(e.target, e.base_dir+'test.py')
        self.assertEqual(e.target_name, 'test.py')
        temp.cleanup()

    def test_testing_no_slaves(self):
        temp = TempDirectory()
        temp.write('test.py', b'int main:')
        temp.makedir(('tests', 'test'))
        e = EasyTest(path=temp.path, test=True)
        e.target_name = 'test.py'
        e.base_tests_target = e.base_tests + 'test/'
        t = e._test()
        self.assertFalse(t)
        temp.cleanup()
