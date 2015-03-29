easy-test
=========

[![Build Status](https://travis-ci.org/davidozhang/easy-test.svg?branch=master)](https://travis-ci.org/davidozhang/easy-test)

This command line utility enables easy editing of test inputs, solutions and running tests
against the inputs.

Version
=======
2.1

What's New
==========
- Dedicated auto test trigger interface after selecting target to run tests as soon as you save your changes (currently only supports scripting-language-based targets)
- Auto test trigger can be configured on and off through configuration file
- Show the date and time of each test run

Recommended Usage
=================
It is recommended to use two terminal windows. One terminal window should be open with easy_test configured to have auto-trigger on, so you can easily see test results as you save your changes. Another terminal window should run easy_test with auto-trigger off, allowing easy editing of slaves

Terminology
===========
Target: The file you are running the tests against.

Slave: The test inputs you design for your target.

Requirements
============
Python 2 with Pip installed on Unix/Linux Machines

Install
=======
####python setup.py install####

Usage
=====
####python easy_test.py -c/--configuration path_to_configuration_file####
OR
####python easy_test.py -d/--directory path_to_test_directory####

where test_directory is the directory containing your test targets.

The hierarchy of the interface is as follows:

- Select Target (enter 'list' to see all available targets)
    * Test Target, Edit Slaves or Delete Slaves / Dedicated Auto-Trigger Interface
        * Select Slave (to Edit or Delete) (enter 'list' to see all available slaves)

Travelling downwards of the hierarchy simply requires you to follow the program. Enter ```CTRL-C``` to move up the hierarchy. You can exit the program by entering ```CTRL-C``` at 'Select Target', or enter ```CTRL-D``` or ```CTRL-Z``` during execution.

The program will check for directory ```/tests``` under your test-directory; if it doesn't exist it will create one. 

When you choose a target, a directory with _the extension-stripped name of the target_ will be created under ```/tests``` .

If your target needs to be compiled, it will be compiled when you select it. The extension-stripped file will become your new target. If you have specified a server IP address in the configuration file, then you will be connected to an interactive session on the server to allow you to run compile commands. Once you are done, simply ```CTRL-D``` to exit interactive session and the resulting executable will be copied to your test directory to become your new target.

To run the slaves against your target, simply enter ```T``` or ```t``` at _Test Target, Edit Slaves or Delete Slaves_.

When you edit target slaves by entering ```E``` or ```e``` at _Test Target, Edit Slaves or Delete Slaves_, you will be asked for the slave's file name. The program will check the slave's existence and create the file if it doesn't exist. You will first be asked to enter the slave's content through vim of the slave file. After editing and saving the slave file, you will be asked to enter the slave's corresponding solution in a file with ```.sol``` appended to the slave's name.

You can delete target slaves by entering ```D``` or ```d``` at _Test Target, Edit Slaves or Delete Slaves_. You will be asked for the slave's file name. Safety features were implemented to prevent accidental deletion of files, such as using interactive rm to manually confirm deletes, displaying error warnings for non-existent files, and terminating the program when sensitive things are being rm-ed. The associated output and solution files will also be deleted.

Configuration File
==================
Currently, the following configuration keys are supported:

- server-ip: The IP address of the remote server you wish to compile files on
- test-directory: The directory containing your test targets
- editor: The command-line shortcut for your favourite editor
- auto-trigger: Runs tests as soon as you save your changes to target. Supports either ```True``` or ```False```.

A line that starts with a '#' is considered a comment. _Please ensure that a space follows the semi-colons_.

See the file ```sample-configuration``` for an example of such file. You can name your configuration file anything!

Mandatory key: test-directory

Optional keys: server-ip, editor (by default easy-test will use ```vim```), auto-trigger

Future Features
===============
- More configuration file options will be supported for greater test customization, including:
	* Supporting different test scenarios
	* Custom definition of targets, slaves and solutions
