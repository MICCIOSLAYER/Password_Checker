# CHECK-THESE-PASSWORDS: 

This is my first project that i upload on Github, to increase my skill in coding and achieve a better understanding in code organization. The core execution is performed while attending the course of Andrei Nagoie on python Developement. Then it is adapted and integrated to be submitted on the course of Software and Computing in Applied Physics degree.

## WHAT USED FOR..
This code is used to check if a password or a list of them through the website: https://haveibeenpwned.com/Passwords
Once selected the option of check your password(s), the program return a string expressing the number of count, that quantify how many times this string is searched online

## INSTRUCTION, better to read what to do for a proper use of it

To use the program after installation, you have to run it from terminal:
- You can give the passwords from the terminal itself, no worries, they are known only by your fingers, since they aren't visible during the typing; or through a txt file

### IMPORTANT NOTE: 
- The passwords in the txt file must be placed **one for each lines**
- Be sure to encode the txt file with utf-8
- After running the code and read the password in your txt file, it will be overwritten by a blank file, to keep secret your passwords

## HOW CAN I HAVE IT 

Download the repo in a folder whose name has to be `Password_Checker`.
In the terminal, once you are in the same location of this folder, launch the command `pip install .` (that is the same directory of the `setup.py` file); alternatively you can launch the command `pip install --editable Password_Checker` in the folder where you store the download (if you use another name to the saving folder as `Saving_Folder` you have to change the command in `pip install --editable Saving_Folder`)
In the latter case you probably need to manually install, if not already present the `requests` library, with `pip install requests` or similar.

## HOW TO USE IT?

The command for the program are:
    * `-fh` or `--from-here` to manually introduce your passwords on the terminal, there are left no trace in local disk since the method to get them is `getpass.getpass()`.
    * `-fl` or `--from-file` to read passwords from a file, tin this case put the absolute path to your file, it has to be a txt and passwords must be separated by space or put in different lines.
    * `-ex` or `--example` to show how the program works and what's the output.
    * `-v` or `--verbosity` to get some suggestion in case your passwords have been violated.

In case none of these command are specified the program create a file named `default_list.txt` in your Desktop and get a pre-set list of passwords: [`D_default_path4`, `these@password`, `isins1de`, `thi5Pc`].

You can launch the program as latter case, while inserting the passwords to check in the same directory of `default_list.txt`, as security measure the file will be overwritten by an empty file.

Hope your you are not been pwned 👌
