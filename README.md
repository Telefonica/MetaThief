# [MetaThief]

<img src="https://www.elevenpaths.com/wp-content/uploads/2014/03/11paths_logo.png?v=3&s=200" title="LogoApp" alt="LogoApp">

MetaThief is a PoC written in Python 3.6, designed to analyze the effectiveness of the controls implemented in a corporate network for detection of data leaks in metadata. This attack tool automatically detects OS, office documents and PDF files, writes the content of the selected office documents into the metadata of PDF files and then send them by email. The attacker downloads the PDF files from emails and uses a second tool that extracts and reconstruct the original files from the metadata within the PDF files.


## Getting Started

In order to use the tool, you have to configure an email address and password so that Metathief could be able to send the modified PDF files with the file fragments to extract. To modify this information, you need to edit metathief.py and configure a sender email address on line 103, this account must have SMTP allowed. Then, in line 104 you need to enter the password of the sender email account. Finally, on line 106 you must configure an email account for receiving the files.


### Prerequisites

To run the MetaThief you need python 3.6 or higher, and some python libraries. You can install this with:

```
pip install -r requirements.txt
```

### Usage

In a computer connected to the corporate network, you need to download metathief.py and execute it with the command:

python3 metathief.py

When the tool sends the files to the destination email address, the attacker can use the second tool recoonthief.py to reconstruct the extracted files, in this way:

```
usage: recoonthief.py [-h] [-T TOTALFILES] [-P PATH] user

positional arguments:
  user                  specify name of the files owner

optional arguments:
  -h, --help            show this help message and exit
  -T TOTALFILES, --total TOTALFILES
                        specify numbers of extracted files
  -P PATH, --path PATH  specify path of extracted files
```

## Languajes and Technologies

* [Python](http://www.elevenpaths.com) - The Python


## Authors

* **Diego Samuel Espitia Montenegro** - *CSA* - [dsespitia](https://twitter.com/dsespitia)


## License

This project is licensed under the GNU General Public License - see the LICENSE file for details


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
