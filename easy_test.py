#!/usr/bin/python
import os
import pexpect

'''
Easy Test Terminal Client
Author: David Zhang
Version: 1.0
Last Updated: March 2015
(C) Copyright David Zhang, 2015.

This module enables easy editing of test inputs, solutions and running tests
against the inputs.
'''

class EasyTest():
	def __init__(self):
		self._display_header()
		self.root = os.getcwd()+'/tests/'
		self._check_dir(self.root)
		while True:
			try:
				self._session()
			except:
				exit()

	def _append(self, path):
		_buffer=[]
		try:
			while True:
				_buffer.append(raw_input())
		except KeyboardInterrupt:
			f=open(path, 'a')
			for i in _buffer:
				f.write(i+'\n')
			f.close()

	def _add_content(self, name, path):
		print 'Appending to slave {}, CTRL-C when done >'.format(name)
		self._append(path)

		f=open(path+'.out', 'w')
		f.close()

		print '\nAppending to slave\'s solution, CTRL-C when done >'
		self._append(path+'.sol')

	def _check_dir(self, _dir):
		if not os.path.isdir(_dir):
			pexpect.run('mkdir '+ _dir)

	def _display_header(self):
		wrap([
			'Easy Test: A More Human Way to Test!',
			'You can test using your slaves, or add/edit slaves!',
		])

	def _edit(self):
		wrap(
			['You are now editing slaves. Enter CTRL-C to stop editing >'],
			char='$',
			alt='$',
		)
		try:
			while True:
				self.slave = raw_input('\nEnter slave name > ')
				self._add_content(self.slave, self.test_target+self.slave)
		except KeyboardInterrupt:
			return

	def _error(self, log):
		wrap(['ERROR > '+log], char='.', alt='|')

	def _session(self):
		self.target = raw_input('\nEnter target file (with ext.) > ')
		if not os.path.exists(os.getcwd()+'/'+self.target):
			self._error(
				'Target {0} is not valid.'.format(self.target),
			)
			return
		strip_extension = self.target[:self.target.index('.')]
		self.test_target = self.root+strip_extension+'/'
		self._check_dir(self.test_target)

		command = raw_input('[T]est with slaves or [E]dit slaves > ')
		if command.lower() == 't':
			self._test()
		elif command.lower() == 'e':
			self._edit()
		else:
			self._error('Invalid Command')

	def _test(self):
		wrap(
			['You are now testing slaves >'],
			char='$',
			alt='$',
		)
		for i in os.listdir(self.test_target):
			if not is_slave(i):
				continue
			slave = self.test_target+i
			out = slave+'.out'
			sol = slave+'.sol'
			os.system('./{0}<{1}>{2}'.format(self.target, slave, out))
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

def is_slave(_file):
	return True if '.' not in _file else False

if __name__=='__main__':
	e = EasyTest()