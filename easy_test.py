# -*- coding: utf-8 -*-

import os
import sys
import argparse

import pexpect

from termcolor import colored

'''
Easy Test Terminal Client
Author: David Zhang
Version: 1.7
Last Updated: March 2015
(C) Copyright David Zhang, 2015.

This command line utility enables easy editing of test inputs, solutions
and running tests against the inputs. For more info, refer to README.md.
'''

class EasyTest():
	def __init__(self, *args, **kwargs):
		display_header()
		path = kwargs['path']
		self.base_dir = path if path[-1]=='/' else path+'/'
		self.base_tests = self.base_dir+'tests/'
		check_dir(self.base_tests)
		while True:
			try:
				self._session()
			except:
				print '\n'
				wrap(['Easy Test has terminated.'])
				exit()

	def _compile(self):
		compilers = {'.c':'gcc', '.cc': 'g++', '.cpp': 'g++'}
		extension = self.target_name[self.target_name.index('.'):]
		if extension not in compilers:
			return True
		print 'Compiling {}...'.format(self.target_name)
		status = pexpect.run(
			'{0} -o {1} {2}'.format(
				compilers[extension],
				self.base_dir + self.strip_ext,
				self.target,
			),
		)
		if status:
			print '\nCompile [{}]'.format(color(False))
			print 'Here\'s the issue:\n'+status
			return False
		else:
			print '\nCompile [{}]'.format(color(True))
			self.target = self.base_dir + self.strip_ext
			self.target_name = self.strip_ext
			return True

	def _edit(self):
		try:
			while True:
				self.slave = raw_input('\n(Select Slave to Edit) > ')
				if self.slave.lower()=='list':
					self._list(self.base_tests_target, 'exclude')
					continue
				add_content(self.base_tests_target+self.slave)
		except KeyboardInterrupt:
			return

	def _delete(self):
		try:
			while True:
				self.slave = raw_input('\n(Select Slave to Delete) > ')
				if self.slave.lower()=='list':
					self._list(self.base_tests_target, 'exclude')
					continue
				for i in ['', '.out', '.sol']:
					path = self.base_tests_target+self.slave+i
					if not os.path.exists(path):
						error('{} does not exist.'.format(path))
						continue
					child = pexpect.spawn('rm -i {}'.format(path))
					child.expect('remove {}'.format(path))
					child.sendline(raw_input(
						'Confirm deletion of {}? [y/n] > '.format(path))
					)
		except KeyboardInterrupt:
			return

	def _list(self, path, option):
		include, exclude = "ls {} | grep '\.'", "ls {} | grep -v '\.'"
		if option=='exclude':
			os.system(exclude.format(path))
		elif option=='include':
			os.system(include.format(path))

	def _session(self):
		self.target_name = raw_input('\n(Select Target) > ')
		if self.target_name.lower()=='list':
			self._list(self.base_dir, 'include')
			return
		elif not os.path.exists(self.base_dir+self.target_name):
			error('Target {0} does not exist.'.format(self.target_name))
			return
		try:
			self.strip_ext = self.target_name[:self.target_name.index('.')]
		except ValueError:
			pass
		self.base_tests_target = self.base_tests+self.strip_ext+'/'
		check_dir(self.base_tests_target)
		self.target = self.base_dir+self.target_name
		if not self._compile():
			return
		while True:
			try:
				self._target_scope()
			except KeyboardInterrupt:
				break

	def _target_scope(self):
		command = raw_input(
			'\n(Target: {}) [T]est, [E]dit or [D]elete slaves > '.format(
				self.target_name,
			),
		)
		if command.lower() == 't':
			self._test()
		elif command.lower() == 'e':
			self._edit()
		elif command.lower() == 'd':
			self._delete()
		else:
			error('Invalid Command')

	def _test(self):
		if len(os.listdir(self.base_tests_target))==0:
			error('You have no slaves for {}'.format(self.target_name)),
			return
		for i in os.listdir(self.base_tests_target):
			if '.out' in i or '.sol' in i:
				continue
			elif not os.path.isfile(self.base_tests_target+i):
				continue
			slave = self.base_tests_target+i
			out, sol = slave+'.out', slave+'.sol'
			os.system('{0}<{1}>{2}'.format(self.target, slave, out))
			status = pexpect.run('diff {0} {1}'.format(out, sol))
			if status:
				print '\nSlave {0} [{1}]\n'.format(i, color(False)),
				print 'Here\'s the issue:\n'+status
			else:
				print '\nSlave {0} [{1}]\n'.format(i, color(True)),

def add_content(path):
	os.system('vim '+path)
	os.system('vim '+path+'.sol')

def check_dir(_dir):
	if not os.path.isdir(_dir):
		os.system('mkdir '+ _dir)

def display_header():
	wrap([
		'Easy Test: A More Human Way to Test!',
		'New in 1.7: Enter \'list\' during select stages to browse files.',
		'View README.md for more info on how to use the program.',
	])

def error(log):
	wrap(['Error > '+log], char='.', alt='|')

def color(_bool):
	return colored('OK', 'green') if _bool else colored('Not OK', 'red')

def wrap(lst, char='*', alt='*'):
	_max = max([len(i) for i in lst])+4
	print char*(_max)
	for j in lst:
		print alt+' '+j+' '*(_max-1-len(alt+' '+j))+alt
	print char*(_max)

def main():
	parser = argparse.ArgumentParser(
		description=('Command line utility for easy editing of test inputs,'
			'solutions and running tests against the inputs.'),
	)
	parser.add_argument(
		'-d',
		'--directory',
		help='Specify path to test targets directory',
		required=True,
	)
	args_dict = vars(parser.parse_args())
	if 'd' in args_dict:
		e = EasyTest(path=args_dict['d'])
	elif 'directory' in args_dict:
		e = EasyTest(path=args_dict['directory'])

if __name__=='__main__':
	main()
