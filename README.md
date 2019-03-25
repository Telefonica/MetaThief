# MetaThief


It is a project developed in Python, which allows to perform a PoC to extract information, for which an attack program is used, which upon reaching the victim's machine commits the team to extract office files using the Metadata fields of PDF files. The second program is used by the attacker to extract the victim's filtered office files from the received PDF metadata,



# Requirements

It is necessary to have installed the Python libraries mentioned in the file requirements,txt

pip install requirements.txt



# Use exfiltering program

Before using the program metathief.py must load the data from the emails, once this is done should only run on the victim machine

python metathief.py

If you need to run on a Windows computer without installing Python, it is possible to convert the program to executable using pyinstaller.



# Use reconstruction program

This is the help of the reconstruction program.

usage: recoonthief.py [-h] [-T TOTALFILES] [-P PATH] user

positional arguments:
 user                  specify name of the files owner

optional arguments:
 -h, --help            show this help message and exit
 -T TOTALFILES, --total TOTALFILES
                       specify numbers of extracted files
 -P PATH, --path PATH  specify path of extracted files

The requested data is taken from the name of the files received from the metathief.py program, as the structure is as follows:

[File number filtered]-th-[user name]-ie-[number of parts of the file]-f-[number of this part].pdf



# Maintainers

@dsespitia



# License

MetaThief is licensed under GNU General Public License v3.0
