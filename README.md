WHAT IT IS  & HOW TO WORK WITH IT:

This is my first project that i upload on Github, to increase my skill in coding and achieve a better understanding in code organization. The core execution is performed while attending the course of Andrei Nagoie on python Developement. Then it is adapted and integrated to be submitted on the course of Software and Computing in Applied Physics degree.

HOW TO USE IT?

* First: install the program in terminal when download use <pip install .>, then you can start the program from any directory in your pc with the command <Check-these-passwords>
* The command for the program are:
    1. -fh or --from-here to manually introduce your passwords on the terminal, there are left no trace in local disk since the method to get them is getpass.getpass().
    2. -fl or --from-file to read passwords from a file, tin this case put the absolute path to your file, it has to be a txt and passwords must be separated by space or put in different lines.
    3. -ex or --example to show how the program works and what's the output.
    4. -v or --verbosity to get some suggestion in case your passwords have been violated.
In case none of these command are specified the program create a file named default_list.txt in your Desktop and get a pre-set list of passwords.
You can launch the program as latter case, while inserting the passwords to check in the same directory of default_list.txt, as security measure the file then will be overwritten by an empty file
