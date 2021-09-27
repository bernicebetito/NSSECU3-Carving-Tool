"""
Bernice Marie M. Betito
NSSECU3-S11
DATA CARVING TOOL
"""

from tkinter import *
from tkinter import ttk
from sys import platform
from pathlib import Path
import os, webbrowser
import threading, queue
import magic

root = Tk()
root.title('NSSECU3 - DATA CARVING TOOL')
root.geometry('750x500')
root.configure(bg="#191919")
root.option_add('*Font', 'Barlow 12')

main = Frame(root)
main.pack()
menubar = Menu(root)

name_folder = StringVar()
jpg = IntVar()
png = IntVar()
pdf = IntVar()
doc = IntVar()
docx = IntVar()
xls = IntVar()
xlsx = IntVar()
directory = StringVar()
num_threads = IntVar()
startSector = IntVar()
endSector = IntVar()
sectorSize = 512
maxFileSize = 10000000
current_percent = IntVar()
current_total = 0
current_sector = StringVar()
current_recovery = StringVar()
status_statements = [
    "File Recovery In Process ...",
    "This might take a while ...",
    "Still In Process ..."
]

threadLock = threading.Lock()
queue_threads = []
current_queue = queue.Queue()

fileHeaders = {}
jpgHeader = b'\xFF\xD8'
jpgTrailer = b'\xFF\xD9'
pngHeader = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
pngTrailer = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'
pdfHeader = b'\x25\x50\x44\x46'
pdfTrailer = b'\x0A\x25\x25\x45\x4F\x46'
microsoftHeader = b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1\x00'
docHeader = b'\xEC\xA5\xC1\x00'
docTrailer = b'\x00\x00\x57\x6F\x72\x64\x2E\x44\x6F\x63\x75\x6D\x65\x6E\x74\x2E'
xlsHeader = b'\x09\x08\x10\x00\x00\x06\x05\x00'
xlsTrailer = b'\xFE\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x57\x00\x6F\x00\x72\x00\x6B\x00\x62\x00\x6F\x00\x6F\x00\x6B\x00'
ooxmlHeader = b'\x50\x4B\x03\x04\x14\x00\x06\x00'
ooxmlTrailer = b'\x50\x4B\x05\x06'
fileTypes = ('.jpg', '.png', '.pdf', '.doc', '.xls', '.docx', '.xlsx')
files_ctr = dict()


def reset():
    global root, main, info, submitted, status, recovered, ctr
    try:
        name_folder.set("")
        jpg.set(0)
        png.set(0)
        pdf.set(0)
        doc.set(0)
        xls.set(0)
        docx.set(0)
        xlsx.set(0)
        num_threads.set(1)
        directory.set("")
        fileHeaders.clear()
        startSector.set(0)
        endSector.set(100000)
        current_percent.set(0)
        current_sector.set("Sector: 0")
        current_recovery.set(" ")
        info.destroy()
        submitted.destroy()
        status.destroy()
        recovered.destroy()
    except NameError:
        pass
    main = Frame(root)
    main.configure(bg="#191919")
    main.pack()
    menubar.destroy()
    mainfunc()


def newRecovery():
    global root, recovered, ctr
    try:
        recovered.destroy()
    except NameError:
        pass
    name_folder.set("")
    jpg.set(0)
    png.set(0)
    pdf.set(0)
    doc.set(0)
    xls.set(0)
    docx.set(0)
    xlsx.set(0)
    num_threads.set(1)
    directory.set("")
    fileHeaders.clear()
    startSector.set(0)
    endSector.set(100000)
    current_percent.set(0)
    current_sector.set("Sector: 0")
    current_recovery.set(" ")
    showForm(1)


def openFolder():
    webbrowser.open(name_folder.get())


def doneRecovery():
    global root, status, recovered, files_ctr
    status.destroy()

    os.chdir("..")

    recovered = Frame(root)
    recovered.configure(bg="#191919")
    recovered.pack()

    recovered.columnconfigure(0, weight=1)
    recovered.columnconfigure(0, weight=1)
    recovered.columnconfigure(0, weight=1)
    recovered.place(relx=.5, rely=.5, anchor="c")

    total_files = 0
    total_jpg = 0
    total_png = 0
    total_pdf = 0
    total_doc = 0
    total_xls = 0
    total_docx = 0
    total_xlsx = 0
    if files_ctr:
        for curr_type in fileHeaders:
            total_files += files_ctr[curr_type]
            if curr_type == "jpg":
                total_jpg = files_ctr[curr_type]
            elif curr_type == "png":
                total_png = files_ctr[curr_type]
            elif curr_type == "pdf":
                total_pdf = files_ctr[curr_type]
            elif curr_type == "doc":
                total_doc = files_ctr[curr_type]
            elif curr_type == "xls":
                total_xls = files_ctr[curr_type]
            elif curr_type == "docx":
                total_docx = files_ctr[curr_type]
            elif curr_type == "xlsx":
                total_xlsx = files_ctr[curr_type]

    Label(recovered, text=str(total_files) + " Recovered files stored in " + str(name_folder.get()), bg="#191919", fg="#FFFFFF", font=25).grid(column=0, row=0, columnspan=4, sticky=NS, padx=5, pady=10)

    current_row = 1
    if jpg.get() == 1:
        jpg_total = Label(recovered, text="JPG: " + str(total_jpg), bg="#191919", fg="#FFFFFF")
        jpg_total.grid(column=0, row=current_row, columnspan=4, sticky=NS, padx=5, pady=10)
        current_row += 1
    if png.get() == 1:
        jpg_total = Label(recovered, text="PNG: " + str(total_png), bg="#191919", fg="#FFFFFF")
        jpg_total.grid(column=0, row=current_row, columnspan=4, sticky=NS, padx=5, pady=10)
        current_row += 1
    if pdf.get() == 1:
        jpg_total = Label(recovered, text="PDF: " + str(total_pdf), bg="#191919", fg="#FFFFFF")
        jpg_total.grid(column=0, row=current_row, columnspan=4, sticky=NS, padx=5, pady=10)
        current_row += 1
    if doc.get() == 1:
        doc_total = Label(recovered, text="DOC: " + str(total_doc), bg="#191919", fg="#FFFFFF")
        doc_total.grid(column=0, row=current_row, columnspan=4, sticky=NS, padx=5, pady=10)
        current_row += 1
    if xls.get() == 1:
        xls_total = Label(recovered, text="XLS: " + str(total_xls), bg="#191919", fg="#FFFFFF")
        xls_total.grid(column=0, row=current_row, columnspan=4, sticky=NS, padx=5, pady=10)
        current_row += 1
    if docx.get() == 1:
        docx_total = Label(recovered, text="DOCX: " + str(total_docx), bg="#191919", fg="#FFFFFF")
        docx_total.grid(column=0, row=current_row, columnspan=4, sticky=NS, padx=5, pady=10)
        current_row += 1
    if xlsx.get() == 1:
        xlsx_total = Label(recovered, text="XLSX: " + str(total_xlsx), bg="#191919", fg="#FFFFFF")
        xlsx_total.grid(column=0, row=current_row, columnspan=4, sticky=NS, padx=5, pady=10)
        current_row += 1
    
    open_button = Button(recovered, text="Open Folder", width=15, height=1, command=openFolder, bg="#37AF28", fg="#FFFFFF")
    open_button.grid(column=0, row=current_row, sticky=NS, padx=20, pady=20)

    new_button = Button(recovered, text="New Recovery", width=15, height=1, command=newRecovery, bg="#4B4BE2", fg="#FFFFFF")
    new_button.grid(column=1, row=current_row, sticky=NS, padx=20, pady=20)

    exit_button = Button(recovered, text="Exit", width=15, height=1, command=root.destroy, bg="#D64000", fg="#FFFFFF")
    exit_button.grid(column=2, row=current_row, sticky=NS, padx=20, pady=20)


def findFiles(curr_drive):
    global root, files_ctr, button_start
    button_start["state"] = DISABLED
    button_start["bg"] = "#BE6E4B"

    startSector.set(0)
    files_ctr = dict((key, 0) for key in fileHeaders.keys())
    while startSector.get() < endSector.get():
        try:
            current_sector.set('Sector: ' + str(startSector.get()))
            threadLock.acquire()
            curr_drive.seek(startSector.get() * sectorSize)

            sectorFileHeader = ''
            sectorFileHeader = curr_drive.read(32)

            for curr_type in fileHeaders:
                if sectorFileHeader[:len(fileHeaders[curr_type][0])] == fileHeaders[curr_type][0]:
                    files_ctr[curr_type] += 1
                    current_recovery.set(curr_type.upper() + ' File Signature Found at Sector ' + str(startSector.get()))
                    file_name = str(files_ctr[curr_type]) + '_' + curr_type.upper() + '.' + curr_type

                    new_file = {
                        "curr_drive": curr_drive,
                        "file_name": file_name,
                        "curr_type": curr_type,
                        "starting": startSector.get(),
                        "file_queue": True
                    }
                    current_queue.put(new_file)

            threadLock.release()
        except:
            pass

        startSector.set(startSector.get() + 1)
        current_percent.set(int((startSector.get() / endSector.get()) * 100))
        root.update_idletasks()

    current_sector.set('Sector: ' + str(startSector.get()))
    for i in range (0, num_threads.get()):
        end_queue = {"file_queue": False}
        current_queue.put(end_queue)


def recoverFiles():
    file_queue = True
    while file_queue:
        try:
            current_file = current_queue.get()
            file_queue = current_file["file_queue"]
        except queue.Empty:
            pass
        else:
            if file_queue:
                curr_drive = current_file["curr_drive"]
                file_name = current_file["file_name"]
                curr_type = current_file["curr_type"]
                starting = current_file["starting"]

                threadLock.acquire()
                curr_recover = open(file_name, 'wb')
                recovering = True

                curr_drive.seek(starting * sectorSize)
                maxFileSizeCtr = 0

                fileFooterLen = len(fileHeaders[curr_type][1])
                sectorFileFooter = b'\x00' * fileFooterLen

                while recovering and maxFileSizeCtr < maxFileSize:
                    read = curr_drive.read(1)
                    sectorFileFooter = sectorFileFooter[1:fileFooterLen] + read
                    curr_recover.write(read)
                    if sectorFileFooter == fileHeaders[curr_type][1]:
                        if curr_type == 'doc' or curr_type == 'xls':
                            read = curr_drive.read(512)
                            curr_recover.write(read)
                        if curr_type == 'docx' or curr_type == 'xlsx':
                            read = curr_drive.read(18)
                            curr_recover.write(read)
                        recovering = False
                        curr_recover.close()
                    maxFileSizeCtr += 1
                if maxFileSizeCtr >= maxFileSize:
                    if curr_type == 'doc' or curr_type == 'xls':
                        read = curr_drive.read(512)
                        curr_recover.write(read)
                    if curr_type == 'docx' or curr_type == 'xlsx':
                        read = curr_drive.read(18)
                        curr_recover.write(read)
                    curr_recover.close()

                file_path = os.getcwd() + "/" + file_name
                if platform == "win32":
                    file_path = os.getcwd() + "\\" + file_name
                file_type = magic.from_file(file_path)
                if curr_type == 'doc' and file_type.find('Microsoft Office Word') == -1 and file_type.find('Word 2007+') == -1:
                    os.remove(file_path)
                    files_ctr["doc"] -= 1
                elif curr_type == 'xls' and file_type.find('Microsoft Excel') == -1 and file_type.find('Excel 2007+') == -1:
                    os.remove(file_path)
                    files_ctr["xls"] -= 1

                if curr_type == 'docx' and file_type.find('Word 2007+') == -1:
                    os.remove(file_path)
                    files_ctr["docx"] -= 1
                elif curr_type == 'xlsx' and file_type.find('Excel 2007+') == -1:
                    os.remove(file_path)
                    files_ctr["xlsx"] -= 1

                threadLock.release()


class updatingQueue (threading.Thread):
    def __init__(self, threadID, threadName, curr_drive):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
        self.curr_drive = curr_drive

    def run(self):
        findFiles(self.curr_drive)


class updatingThreads (threading.Thread):
    def __init__(self, threadID, threadName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName

    def run(self):
        recoverFiles()


def updateStatus():
    global root, files_ctr
    global button_start, threads

    button_start["state"] = DISABLED
    button_start["bg"] = "#BE6E4B"

    dir_path = directory.get()
    rec_folder = name_folder.get()
    os.chdir(rec_folder)
    try:
        with open(dir_path, 'rb') as curr_drive:
            producer_thread = updatingQueue(1, "Queue Thread", curr_drive)

            for ctr in range(0, num_threads.get()):
                threadID = ctr + 1
                threadName = "Thread-" + str(threadID)
                consumer_thread = updatingThreads(threadID, threadName)
                queue_threads.append(consumer_thread)

            producer_thread.start()
            for t in queue_threads:
                t.start()

            producer_thread.join()
            for t in queue_threads:
                t.join()

            queue_threads.clear()
            current_sector.set('Sector: ' + str(startSector.get()))
            button_start["text"] = "Proceed"
            button_start["command"] = doneRecovery
            button_start["bg"] = "#37AF28"
            button_start["state"] = NORMAL
    except PermissionError:
        current_sector.set("Permission Error! Permission to access %s was denied." % directory.get())
        button_start["text"] = "Proceed"
        button_start["command"] = doneRecovery
        button_start["bg"] = "#37AF28"
        button_start["state"] = NORMAL


def startThread():
    threading.Thread(target=updateStatus).start()


def readyEverything():
    global fileHeaders, fileTypes
    if not os.path.exists(name_folder.get()):
        os.makedirs(name_folder.get())

    if jpg.get() == 1:
        fileHeaders.update({'jpg':[jpgHeader, jpgTrailer]})
        if ".jpg" not in fileTypes:
            temp = list(fileTypes)
            temp.append(".jpg")
            fileTypes = tuple(temp)
    else:
        if "jpg" in fileHeaders:
            fileHeaders.pop('jpg')
        elif ".jpg" in fileTypes:
            temp = list(fileTypes)
            temp.remove(".jpg")
            fileTypes = tuple(temp)

    if png.get() == 1:
        fileHeaders.update({'png':[pngHeader, pngTrailer]})
        if ".png" not in fileTypes:
            temp = list(fileTypes)
            temp.append(".png")
            fileTypes = tuple(temp)
    else:
        if "png" in fileHeaders:
            fileHeaders.pop('png')
        elif ".png" in fileTypes:
            temp = list(fileTypes)
            temp.remove(".png")
            fileTypes = tuple(temp)

    if pdf.get() == 1:
        fileHeaders.update({'pdf':[pdfHeader, pdfTrailer]})
        if ".pdf" not in fileTypes:
            temp = list(fileTypes)
            temp.append(".pdf")
            fileTypes = tuple(temp)
    else:
        if "pdf" in fileHeaders:
            fileHeaders.pop('pdf')
        elif ".pdf" in fileTypes:
            temp = list(fileTypes)
            temp.remove(".pdf")
            fileTypes = tuple(temp)

    if doc.get() == 1:
        fileHeaders.update({'doc':[microsoftHeader, docTrailer]})
        if ".doc" not in fileTypes:
            temp = list(fileTypes)
            temp.append(".doc")
            fileTypes = tuple(temp)
    else:
        if "doc" in fileHeaders:
            fileHeaders.pop('doc')
        elif ".doc" in fileTypes:
            temp = list(fileTypes)
            temp.remove(".doc")
            fileTypes = tuple(temp)

    if docx.get() == 1:
        fileHeaders.update({'docx':[ooxmlHeader, ooxmlTrailer]})
        if ".docx" not in fileTypes:
            temp = list(fileTypes)
            temp.append(".docx")
            fileTypes = tuple(temp)
    else:
        if "docx" in fileHeaders:
            fileHeaders.pop('docx')
        elif ".docx" in fileTypes and xlsx.get() == 0:
            temp = list(fileTypes)
            temp.remove(".docx")
            fileTypes = tuple(temp)

    if xls.get() == 1:
        fileHeaders.update({'xls':[microsoftHeader, xlsTrailer]})
        if ".xls" not in fileTypes:
            temp = list(fileTypes)
            temp.append(".xls")
            fileTypes = tuple(temp)
    else:
        if "xls" in fileHeaders:
            fileHeaders.pop('xls')
        elif ".xls" in fileTypes:
            temp = list(fileTypes)
            temp.remove(".xls")
            fileTypes = tuple(temp)

    if xlsx.get() == 1:
        fileHeaders.update({'xlsx':[ooxmlHeader, ooxmlTrailer]})
        if ".xlsx" not in fileTypes:
            temp = list(fileTypes)
            temp.append(".xlsx")
            fileTypes = tuple(temp)
    else:
        if "xlsx" in fileHeaders:
            fileHeaders.pop('xlsx')
        elif ".xlsx" in fileTypes and docx.get() == 0:
            temp = list(fileTypes)
            temp.remove(".xlsx")
            fileTypes = tuple(temp)

    filelist = [file for file in os.listdir(name_folder.get()) if file.endswith(fileTypes)]
    for f in filelist:
        os.remove(os.path.join(name_folder.get(), f))


def printStatus():
    global root, submitted, status, button_start
    try:
        submitted.destroy()
    except NameError:
        pass

    readyEverything()

    status = Frame(root)
    status.configure(bg="#191919")
    status.pack()

    status.columnconfigure(0, weight=1)
    status.place(relx=.5, rely=.5, anchor="c")

    current_percent.set(0)
    current_sector.set("Sector: 0")
    current_recovery.set(" ")
    
    Label(status, text="Recovery Status", bg="#191919", fg="#FFFFFF", font=25).grid(column=0, row=0, sticky=NS, padx=5, pady=10)

    ttk.Progressbar(status, variable=current_percent, maximum=100, orient='horizontal', mode='determinate', length=300).grid(column=0, row=1, sticky=NS, padx=10, pady=10)
    Label(status, textvariable=current_sector, bg="#191919", fg="#FFFFFF",).grid(column=0, row=2, sticky=NS, padx=10, pady=10)
    Label(status, textvariable=current_recovery, bg="#191919", fg="#FFFFFF", ).grid(column=0, row=3, sticky=NS, padx=10, pady=10)

    button_start = Button(status, text="Start", width=10, height=1, command=startThread, bg="#37AF28", fg="#FFFFFF")
    button_start.grid(column=0, row=4, columnspan=3, sticky=NS, padx=20, pady=20)


def submitInfo():
    global info, root, submitted
    info.destroy()

    temp = jpg.get() + png.get() + pdf.get() + doc.get() + docx.get() + xls.get() + xlsx.get()
    if len(name_folder.get()) > 0 and temp > 0 and len(directory.get()) > 0 and (num_threads.get() > 0 and num_threads.get() < 21) and endSector.get() > 0:
        dir_path = Path(directory.get())
        if os.path.exists(dir_path):
            submitted = Frame(root)
            submitted.configure(bg="#191919")
            submitted.pack()

            submitted.columnconfigure(0, weight=1)
            submitted.columnconfigure(1, weight=1)
            submitted.place(relx=.5, rely=.5, anchor="c")

            Label(submitted, text="Confirm  Information", bg="#191919", fg="#FFFFFF", font=25).grid(column=0, row=0, columnspan=3, sticky=NS, padx=5, pady=10)

            Label(submitted, text="Name of Folder: ", bg="#191919", fg="#FFFFFF").grid(column=0, row=1, sticky=W, padx=5, pady=10)
            Label(submitted, text=name_folder.get(), bg="#191919", fg="#FFFFFF").grid(column=1, row=1, sticky=W, padx=5, pady=10)

            Label(submitted, text="File Types: ", bg="#191919", fg="#FFFFFF").grid(column=0, row=2, sticky=W, padx=5, pady=3)
            current_row = 2
            if jpg.get() == 1:
                Label(submitted, text="JPG", bg="#191919", fg="#FFFFFF").grid(column=1, row=current_row, sticky=W, padx=5, pady=3)
                current_row += 1
            if png.get() == 1:
                Label(submitted, text="PNG", bg="#191919", fg="#FFFFFF").grid(column=1, row=current_row, sticky=W, padx=5, pady=3)
                current_row += 1
            if pdf.get() == 1:
                Label(submitted, text="PDF", bg="#191919", fg="#FFFFFF").grid(column=1, row=current_row, sticky=W, padx=5, pady=3)
                current_row += 1
            if doc.get() == 1:
                Label(submitted, text="DOC", bg="#191919", fg="#FFFFFF").grid(column=1, row=current_row, sticky=W, padx=5, pady=3)
                current_row += 1
            if docx.get() == 1:
                Label(submitted, text="DOCX", bg="#191919", fg="#FFFFFF").grid(column=1, row=current_row, sticky=W, padx=5, pady=3)
                current_row += 1
            if xls.get() == 1:
                Label(submitted, text="XLS", bg="#191919", fg="#FFFFFF").grid(column=1, row=current_row, sticky=W, padx=5, pady=3)
                current_row += 1
            if xlsx.get() == 1:
                Label(submitted, text="XLSX", bg="#191919", fg="#FFFFFF").grid(column=1, row=current_row, sticky=W, padx=5, pady=3)
                current_row += 1

            Label(submitted, text="Directory Path: ", bg="#191919", fg="#FFFFFF").grid(column=0, row=current_row, sticky=W, padx=5, pady=10)
            Label(submitted, text=directory.get(), bg="#191919", fg="#FFFFFF").grid(column=1, row=current_row, sticky=W, padx=5, pady=10)
            current_row += 1

            Label(submitted, text="Number of Threads: ", bg="#191919", fg="#FFFFFF").grid(column=0, row=current_row, sticky=W, padx=5, pady=10)
            Label(submitted, text=num_threads.get(), bg="#191919", fg="#FFFFFF").grid(column=1, row=current_row, sticky=W, padx=5, pady=10)
            current_row += 1

            Label(submitted, text="End Sector: ", bg="#191919", fg="#FFFFFF").grid(column=0, row=current_row, sticky=W, padx=5, pady=10)
            Label(submitted, text=endSector.get(), bg="#191919", fg="#FFFFFF").grid(column=1, row=current_row, sticky=W, padx=5, pady=10)
            current_row += 1

            Button(submitted, text="Back", width=10, height=1, command=backToForm, bg="#D64000", fg="#FFFFFF").grid(column=0, row=current_row+1, sticky=NS, padx=20, pady=20)
            Button(submitted, text="Confirm", width=10, height=1, command=printStatus, bg="#37AF28", fg="#FFFFFF").grid(column=1, row=current_row + 1, sticky=NS, padx=20, pady=20)
        else:
            showForm(2)
    elif num_threads.get() <= 0 or num_threads.get() >= 21:
        showForm(3)
    else:
        showForm(0)


def backToForm():
    global main, root, submitted
    try:
        submitted.destroy()
    except NameError:
        pass
    showForm(1)


def showForm(valid):
    global info

    info = Frame(root)
    info.configure(bg="#191919")
    info.pack()

    info.columnconfigure(0, weight=1)
    info.columnconfigure(1, weight=1)
    info.columnconfigure(2, weight=1)
    info.columnconfigure(3, weight=1)
    info.place(relx=.5, rely=.5, anchor="c")

    Label(info, text="Input Information", bg="#191919", fg="#FFFFFF", font=25).grid(column=0, row=0, columnspan=4, sticky=NS, padx=5, pady=10)

    Label(info, text="Enter the name of the folder to", bg="#191919", fg="#FFFFFF").grid(column=0, row=1, sticky=W, padx=5)
    Label(info, text="contain the recovered files: ", bg="#191919", fg="#FFFFFF").grid(column=0, row=2, sticky=W, padx=5)

    name_field = Entry(info, textvariable=name_folder)
    name_field.focus()
    name_field.grid(column=1, row=1, rowspan=2, columnspan=3, sticky=W, padx=5, pady=10)
    if valid == 0 and len(name_folder.get()) <= 0:
            name_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")

    Label(info, text="Choose File Types: ", bg="#191919", fg="#FFFFFF").grid(column=0, row=3, sticky=W, padx=5)
    jpg_check = Checkbutton(info, text="JPG", variable=jpg, onvalue=1, offvalue=0, bg="#191919", fg="#FFFFFF", selectcolor="#858585", borderwidth=0, highlightthickness=0)
    png_check = Checkbutton(info, text="PNG", variable=png, onvalue=1, offvalue=0, bg="#191919", fg="#FFFFFF", selectcolor="#858585", borderwidth=0, highlightthickness=0)
    pdf_check = Checkbutton(info, text="PDF", variable=pdf, onvalue=1, offvalue=0, bg="#191919", fg="#FFFFFF", selectcolor="#858585", borderwidth=0, highlightthickness=0)
    doc_check = Checkbutton(info, text="DOC", variable=doc, onvalue=1, offvalue=0, bg="#191919", fg="#FFFFFF", selectcolor="#858585", borderwidth=0, highlightthickness=0)
    docx_check = Checkbutton(info, text="DOCX", variable=docx, onvalue=1, offvalue=0, bg="#191919", fg="#FFFFFF", selectcolor="#858585", borderwidth=0, highlightthickness=0)
    xls_check = Checkbutton(info, text="XLS", variable=xls, onvalue=1, offvalue=0, bg="#191919", fg="#FFFFFF", selectcolor="#858585", borderwidth=0, highlightthickness=0)
    xlsx_check = Checkbutton(info, text="XLSX", variable=xlsx, onvalue=1, offvalue=0, bg="#191919", fg="#FFFFFF", selectcolor="#858585", borderwidth=0, highlightthickness=0)
    jpg_check.grid(column=1, row=3, sticky=W, padx=10)
    png_check.grid(column=1, row=4, sticky=W, padx=10)
    pdf_check.grid(column=1, row=5, sticky=W, padx=10)
    doc_check.grid(column=1, row=6, sticky=W, padx=10)
    docx_check.grid(column=2, row=3, sticky=W, padx=10)
    xls_check.grid(column=2, row=4, sticky=W, padx=10)
    xlsx_check.grid(column=2, row=5, sticky=W, padx=10)
    temp = jpg.get() + png.get() + pdf.get() + doc.get() + docx.get() + xls.get() + xlsx.get()
    if valid == 0 and temp == 0:
        jpg_check.configure(fg="#D64000")
        png_check.configure(fg="#D64000")
        pdf_check.configure(fg="#D64000")
        doc_check.configure(fg="#D64000")
        docx_check.configure(fg="#D64000")
        xls_check.configure(fg="#D64000")
        xlsx_check.configure(fg="#D64000")

    Label(info, text="Enter the Path of the", bg="#191919", fg="#FFFFFF").grid(column=0, row=7, sticky=W, padx=5)
    Label(info, text="Directory to check: ", bg="#191919", fg="#FFFFFF").grid(column=0, row=8, sticky=W, padx=5)
    dir_field = Entry(info, textvariable=directory)
    dir_field.grid(column=1, row=7, rowspan=2, columnspan=3, sticky=W, padx=5)

    if valid == 0 or valid == 2:
        if len(directory.get()) <= 0 or valid == 2:
            dir_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
            if valid == 2:
                Label(info, text="Path of Directory does not exist.", bg="#191919", fg="#D64000").grid(column=0, row=12, columnspan=3, sticky=NS, padx=5)
    if len(directory.get()) <= 0:
        if platform == "linux" or platform == "linux2":
            dir_field.insert(0, "/dev/sdb")
        elif platform == "darwin":
            dir_field.insert(0, "/dev/disk")
        elif platform == "win32":
            dir_field.insert(0, "\\\\.\\D:")

    Label(info, text="Enter amount of Threads ", bg="#191919", fg="#FFFFFF").grid(column=0, row=9, sticky=W, padx=5)
    Label(info, text="to work on recovery: ", bg="#191919", fg="#FFFFFF").grid(column=0, row=10, sticky=W, padx=5)
    threads_spinbox = Spinbox(info, width=5, from_=1, to=20, textvariable=num_threads, wrap=True)
    threads_spinbox.grid(column=1, row=9, rowspan=2, columnspan=3, sticky=W, padx=5)
    if valid == 0 or valid == 3:
        if valid == 3:
            Label(info, text="Minimum is 0 and maximum is 20.", bg="#191919", fg="#D64000").grid(column=0, row=12, columnspan=3, sticky=NS, padx=5)
        threads_spinbox.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")

    Label(info, text="Enter the End Sector: ", bg="#191919", fg="#FFFFFF").grid(column=0, row=11, sticky=W, padx=5)
    end_field = Entry(info, textvariable=endSector)
    end_field.grid(column=1, row=11, columnspan=3, sticky=NS, padx=5, pady=10)
    if valid == 0 and endSector.get() <= 0:
        end_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")

    if valid == 0:
        Label(info, text="Please fill-up all fields.", bg="#191919", fg="#D64000").grid(column=0, row=12, columnspan=3, sticky=NS, padx=5)

    Button(info, text="Submit", width=10, height=1, command=submitInfo, bg="#4B4BE2", fg="#FFFFFF").grid(column=0, row=13, columnspan=4, sticky=NS, padx=20, pady=20)


def createMenu():
    root.config(menu=menubar)

    file_menu = Menu(menubar, tearoff=False)
    file_menu.add_command(label='Home', command=reset)
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=root.destroy)
    menubar.add_cascade(
        label="File",
        menu=file_menu
    )


def proceed():
    global main, root
    main.destroy()
    createMenu()
    showForm(1)


def mainfunc():
    global menubar, main, root
    main.configure(bg="#191919")
    main.columnconfigure(0, weight=1)
    main.place(relx=.5, rely=.5, anchor="c")

    endSector.set(100000)

    Label(main, text="DATA CARVING TOOL", bg="#191919", fg="#FFFFFF", font=35).grid(column=0, row=0, sticky=EW, padx=10, pady=10)
    Label(main, text="Bernice Marie M. Betito  NSSECU3 - S11", bg="#191919", fg="#666666").grid(column=0, row=1, sticky=EW, padx=10, pady=10)
    proceed_btn = Button(main, text="Proceed", height=1, command=proceed, bg="#4B4BE2", fg="#FFFFFF")
    proceed_btn.grid(column=0, row=2, sticky=EW, padx=10, pady=10)

    menubar = Menu(root)


mainfunc()
root.mainloop()
