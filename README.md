easy-test
=========
This command line utility enables easy editing of test inputs, solutions and running tests
against the inputs.

Version
=======
1.6

Terminology
===========
Target: The file you are running the tests against.

Slave: The test inputs you design for your target.

Install
=======
####python setup.py install####

Usage
=====
####python easy_test.py [test-directory]####

Where test-directory is the path to the directory of your test targets.

The hierarchy of the interface is as follows:

- Select Target
    * Test Target or Edit (Target) Slaves
        * Select Slave (to Edit)

Travelling downwards of the hierarchy simply requires you to follow the program. Enter ```CTRL-C``` to move up the hierarchy. You can exit the program by entering ```CTRL-C``` at 'Select Target', or enter ```CTRL-D``` or ```CTRL-Z``` during execution.

The program will check for directory ```/tests``` under your test-directory; if it doesn't exist it will create one. 

When you choose a target, a directory with _the extension-stripped name of the target_ will be created under ```/tests``` . When you edit target slaves by entering ```E``` or ```e``` at _Test Target or Edit (Target) Slaves_, you will be asked for the slave's file name. The program will check the slave's existence and create the file if it doesn't exist. You will first be asked to enter the slave's content through vim of the slave file. After editing and saving the slave file, you will be asked to enter the slave's corresponding solution in a file with ```.sol``` appended to the slave's name.

To run the slaves against your target, simply navigate to _Test Target or Edit Slaves_ and enter ```T``` or ```t```.

Future Features
=====
The following features are considered and will be gradually rolled out as they become available:
- Autocomplete file names and paths in-program
- Browse and search directories in-program
- Add configuration file option for greater test customization
- Send target file to a remote server, check compile status (if applicable) and send test results back