easy-test
=========
This command line utility enables easy editing of test inputs, solutions and running tests
against the inputs.

Version
=======
1.7

Terminology
===========
Target: The file you are running the tests against.

Slave: The test inputs you design for your target.

Requirements
============
Python 2 with Pip installed on Unix Machines (preferably Macs)

Install
=======
####python setup.py install####

Usage
=====
####python easy_test.py -d/--directory path_to_test_directory####

Where test-directory is the directory where your test targets are located.

The hierarchy of the interface is as follows:

- Select Target
    * Test Target, Edit Slaves or Delete Slaves
        * Select Slave (to Edit or Delete)

Travelling downwards of the hierarchy simply requires you to follow the program. Enter ```CTRL-C``` to move up the hierarchy. You can exit the program by entering ```CTRL-C``` at 'Select Target', or enter ```CTRL-D``` or ```CTRL-Z``` during execution.

The program will check for directory ```/tests``` under your test-directory; if it doesn't exist it will create one. 

When you choose a target, a directory with _the extension-stripped name of the target_ will be created under ```/tests``` . When you edit target slaves by entering ```E``` or ```e``` at _Test Target or Edit (Target) Slaves_, you will be asked for the slave's file name. The program will check the slave's existence and create the file if it doesn't exist. You will first be asked to enter the slave's content through vim of the slave file. After editing and saving the slave file, you will be asked to enter the slave's corresponding solution in a file with ```.sol``` appended to the slave's name.

You can delete target slaves by entering ```D``` or ```d``` at _Test Target or Edit (Target) Slaves_. You will be asked for the slave's file name. Safety features were implemented to prevent accidental deletion of files, such as using interactive rm to manually confirm deletes, displaying error warnings for non-existent files, and terminating the program when sensitive things are being rm-ed. The associated output and solution files will also be deleted.

To run the slaves against your target, simply navigate to _Test Target or Edit Slaves_ and enter ```T``` or ```t```.

Future Features
=====
The following features are considered and will be gradually rolled out as they become available:
- Autocomplete file names and paths in-program
- Detailed error results and performance analysis
- Add description tag (optional) to slaves so search can be done (suitable for larger test input directories)
- Add metadata directory in slave directory for keeping track of description tags of slaves and other information
- Add configuration file option for greater test customization (ie. supporting different test scenarios, different configurations of slave and target types)
- Send target file to a remote server, check compile status (if applicable) and send test results back
