import argparse
import os

from PyPDF2 import PdfFileReader



def _reensamblar(td, user, frag, path):
    """ Se crean los archvios resultado de recostruir los fragmentos recibidos"""
    i = 0
    name = path + "/" + "exfilt" + user + str(td)
    exfil = open(name, 'wb')
    while i < frag:
        allname = path + "/" + str(td) + "-th-" + user + "-ie-" + str(frag) + "-f-" + str(i) + ".pdf"
        pdfFile = PdfFileReader(open(allname, 'rb'))
        docInfo = pdfFile.getDocumentInfo()
        rec = docInfo['/Comment']
        exfil.write(rec)
        i = i + 1
    print("Recuperado el archivo " + str(td) + " llamado " + name)
    exfil.close()
    

def _valida(td, usr, path):
    """ Permite determinar la cantidad de segmentos a reensamblar """
    name = str(td) + "-th-" + usr + "-ie-"
    lstPath = os.walk(path)
    for root, dirs, files in lstPath:
        for fileName in files:
            if fileName.find(name) == 0:
                f = fileName.find("-f-")
                e = fileName.find("-ie-") + 4
                return int(fileName[e:f])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-T',
                        "--total",
                        dest='totalfiles',
                        type=int,
                        help='specify numbers of extracted files',
                        default=1)
    parser.add_argument('-P',
                        "--path",
                        type=str,
                        help='specify path of extracted files',
                        default=os.getcwd())
    parser.add_argument("user",
                        type=str,
                        help='specify name of the files owner')
    args = parser.parse_args()
    if args.user == None:
        print(parser.print_usage)
        exit(0)
    else:
        if os.path.exists(args.path):
            td = 1
            while td <= args.totalfiles:
                frag = _valida(td, args.user, args.path)
                _reensamblar(td, args.user, frag, args.path)
                td = td + 1
        else:
            print("Path dont exist")
            exit(0)


if __name__ == '__main__':
    main()
