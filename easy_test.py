# -*- coding: utf-8 -*-

import os
import sys
import pexpect

'''
Easy Test Terminal Client
Author: David Zhang
Last Updated: March 2015
(C) Copyright David Zhang, 2015.

This module enables easy editing of test inputs, solutions and running tests
against the inputs. For more info, refer to README.md or Wiki.
'''

class EasyTest():
	def __init__(self, path):
		display_header()
		self.remote_dir = path if path[-1]=='/' else path+'/'
		self.root = self.remote_dir+'tests/'
		check_dir(self.root)
		while True:
			try:
				self._session()
			except:
				print '\n'
				wrap(['Easy Test has terminated.'])
				exit()

	def _edit(self):
		try:
			while True:
				self.slave = raw_input('\n(Select Slave) > ')
				add_content(self.slave, self.test_target+self.slave)
		except KeyboardInterrupt:
			return

	def _session(self):
		self.target_name = raw_input(
			'\n(Select Target) > ',
		)
		if not os.path.exists(self.remote_dir+self.target_name):
			error(
				'Target {0} is not valid.'.format(self.target_name),
			)
			return
		try:
			strip_ext = self.target_name[:self.target_name.index('.')]
		except ValueError:
			pass
		self.test_target = self.root+strip_ext+'/'
		check_dir(self.test_target)
		self.target = self.remote_dir+self.target_name
		while True:
			try:
				self._target_scope()
			except KeyboardInterrupt:
				break

	def _target_scope(self):
		command = raw_input(
			'\n(Target: {}) [T]est or [E]dit slaves > '.format(
				self.target_name,
			),
		)
		if command.lower() == 't':
			self._test()
		elif command.lower() == 'e':
			self._edit()
		else:
			error('Invalid Command')

	def _test(self):
		if len(os.listdir(self.test_target))==0:
			wrap(
				['You have no slaves for {}'.format(self.target_name)],
				char='.',
				alt='|',
			)
			return
		for i in os.listdir(self.test_target):
			if '.out' in i or '.sol' in i:
				continue
			slave = self.test_target+i
			out = slave+'.out'
			sol = slave+'.sol'
			os.system('{0}<{1}>{2}'.format(self.target, slave, out))
			status = pexpect.run('diff {0} {1}'.format(out, sol))
			if status:
				wrap(
					['Slave {0} [Not OK]'.format(i)],
					char='.',
					alt='|',
				)
				print 'Here\'s the issue\n'+status
			else:
				wrap(
					['Slave {0} [OK]'.format(i)],
					char='.',
					alt='|',
				)

def add_content(name, path):
	os.system('vim '+path)
	os.system('vim '+path+'.sol')

def check_dir(_dir):
	if not os.path.isdir(_dir):
		os.system('mkdir '+ _dir)

def display_header():
		wrap([
			'Easy Test: A More Human Way to Test!',
			'Edit or test your targets with their slaves.',
			'Select Target <-> Test with Slaves/Edit Slaves <-> Select Slave',
		])

def error(log):
		wrap(['ERROR > '+log], char='.', alt='|')

def wrap(lst, char='*', alt='*'):
	border = ''
	_max = 0
	for i in lst:
		if len(i)>_max:
			_max = len(i)
	border += char*(_max+4)
	_max += 4
	print border
	for j in lst:
		print alt+' '+j+' '*(_max-1-len(alt+' '+j))+alt
	print border

def main(argv):
	if len(argv)==0:
		print 'usage: python easy_test.py DIRECTORY_TO_TEST_TARGETS'
		exit()
	else:
		e = EasyTest(argv[0])

if __name__=='__main__':
	main(sys.argv[1:])
