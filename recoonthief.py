import argparse
import os
from PyPDF2 import PdfFileReader

#Permite determinar la cantidad de segmentos a reensamblar
def valida(td,usr, path):
    name = str(td) + "-th-" + usr + "-ie-"
    lstPath = os.walk(path)
    for root, dirs, files in lstPath:
        for fileName in files:
            if fileName.find(name) == 0:
                f = fileName.find("-f-")
                e = fileName.find("-ie-") + 4
                cant = int(fileName[e:f])
                return cant
                break


#Se crean los archvios resultado de recostruir los fragmentos recibidos
def reensamblar(td,user,frag,path):
    i = 0
    name = path + "/" +"exfilt" + user + str(td)
    exfil = open(name, 'wb')
    while i < frag:
        allname = path + "/" +str(td) + "-th-" + user + "-ie-" + str(frag) + "-f-" + str(i) + ".pdf"
        pdfFile = PdfFileReader(open(allname, 'rb'))
        docInfo = pdfFile.getDocumentInfo()
        rec = docInfo['/Comment']
        exfil.write(rec)
        i = i+1
    print("Recuperado el archivo " + str(td) + " llamado " + name)
    exfil.close()



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-T', "--total", dest='totalfiles', type=int, help='specify numbers of extracted files', default=1)
    parser.add_argument('-P', "--path", type=str, help='specify path of extracted files', default=os.getcwd())
    parser.add_argument("user", type=str, help='specify name of the files owner')
    args = parser.parse_args()
    if args.user == None:
        print(parser.print_usage)
        exit(0)
    else:
        if os.path.exists(args.path):
            td = 1
            while td <= args.totalfiles:
                frag = valida(td,args.user, args.path)
                reensamblar(td,args.user,frag,args.path)
                td = td + 1
        else:
            print("Path dont exist")
            exit(0)


if __name__ == '__main__':
    main()
