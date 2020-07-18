from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from collections import OrderedDict
import hashlib
from os import listdir
from os.path import isfile, join
import sys
import csv

def extractFirstPageContent(extractedText):
    po_start = keys_start = False
    current_group = ''
    po_dict = {}
    x=0
    keyholder = []
    # Cycle through all the lines
    for line in extractedText.split("\n"):
        #print(line)
        line = line.strip()
        if(line == 'DV PROTECTIVE'):
            #This needs to be in its own if because we want to capture it into the array
            keys_start = True
        if(line in ('DV PROTECTIVE','JUVENILE PEACE','PEACE')):
            # Set the current group variable
            # Add the current group as an eventual key when we save the data. There is probably a better way to do this.
            # Then create a new sub array in or overall po_dict with the current group as the key.
            current_group = line
            keyholder.append(line)
            po_dict[current_group] = OrderedDict()
        elif(line == 'Count'):
            # Means Switch from keys to values
            # It also means we need to switch to a new current_group.
            po_start = True
            keys_start = False
            current_group = keyholder[x]
            x+=1
        elif(line == 'Total All:'):
            # End of keys
            po_start = False
        elif(po_start == True):
            #I feel like there's a better way to do this.
            # Cycle through the keys in the ordered dictionary for the current group. If the value is a None then we replace it with the value.
            # This is how we go one by one.
            for key, value in po_dict[current_group].items():
                if(value == None):
                    po_dict[current_group][key] = line
                    break;
        elif(line == 'Sex'):
            continue
        elif(keys_start == True):
            po_dict[current_group][line] = None
    return po_dict

def getTextFromFirstPage(filename):
    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    extracted_text = ''
    po = None
    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()
        break
    fp.close()
    return extracted_text

def appendToCSV(dvdata,county,year,month):
    # TODO: Right now you need to have the csvs already made. It'd be nice if it checked and created csvs if they don't exist.
    # This is built so there are three seperate csvs that are filled one at a time
    dvtypes = ('DV PROTECTIVE','JUVENILE PEACE','PEACE')
    path = ''
    for dvtype in dvtypes:
        if(dvtype in dvdata.keys()):
            with open(path +dvtype + '.csv','a',newline='\n') as fd:
                csvwriter = csv.writer(fd, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
                total = int(dvdata[dvtype].setdefault('MALE',0)) + int(dvdata[dvtype].setdefault('FEMALE',0)) + int(dvdata[dvtype].setdefault('UNKNOWN',0))
                writeinfo = [year,county,month,dvdata[dvtype].setdefault('MALE',0),dvdata[dvtype].setdefault('FEMALE',0),dvdata[dvtype].setdefault('UNKNOWN',0),total]
                csvwriter.writerow(writeinfo)


if __name__ == '__main__':
    counties = (
    'Allegany',
    'Carroll',
    'Harford',
    'Saint_Marys',
    'Anne_Arundel',
    'Cecil',
    'Howard',
    'Somerset',
    'Baltimore_City',
    'Charles',
    'Kent',
    'Talbot',
    'Baltimore',
    'Dorchester',
    'Montgomery',
    'Washington',
    'Calvert',
    'Frederick',
    'Prince_Georges',
    'Wicomico',
    'Caroline',
    'Garrett',
    'Queen_Annes',
    'Worcester'
    )
    x = 0
    for county in counties:
        path = '' + county #If files not stored in same directory of python file
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        for filename in onlyfiles:
            print(filename)
            month = filename[-6:-4].strip("_")
            year = filename.split('_')[-2]
            # The format changed starting in 2017 and my parser only works for 2018 and above.
            if(int(year) >= 2018):
                text = getTextFromFirstPage(path + "\\" + filename)
                po=extractFirstPageContent(text)
                appendToCSV(po,county,year,month)



