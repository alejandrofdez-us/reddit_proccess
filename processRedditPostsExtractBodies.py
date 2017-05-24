# coding=utf-8
import ijson
import collections
import csv
import subprocess
import calendar
from datetime import datetime, timedelta

import nltk
import nltk.data
import re
import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer


# import sys
# from bs4 import BeautifulSoup


# meter comas después de cada cierre de llave
# bash sed -ie 's/\}/\},/g' RC_2015-01   

# añadir [ al principio
# sed -ie '1s/^/[/' RC_2015-01   

# sustituir , final por ]
# sed -ie '$s/\(.*\),/\1]/' RC_2015-01

# sed -ie 's/\}/\},/g' 2016/RC_2016-06; sed -ie '1s/^/[/' 2016/RC_2016-06; sed -ie '$s/\(.*\),/\1]/' 2016/RC_2016-06


def crearSlots(nMin, fechaInicio, fechaFin):
    # 01 March, 2006 - 31 May, 2006
    slots = {}
    fechaIter = fechaInicio
    while fechaIter < fechaFin:
        slots[fechaIter] = [0]
        fechaIter = fechaIter + timedelta(minutes=nMin)

    return collections.OrderedDict(sorted(slots.items()))


def limpia(oracion):
    """
    Dada una oración, elimina caracteres no deseados, URL's, números...
    """
    # oracion = BeautifulSoup(oracion, "lxml").get_text()
    # oracion = re.sub(r"\[\[[^\|\]]*\|([^\]]*)\]\]", r"\1", oracion)  # [[X|Y]] por Y
    # oracion = re.sub(r"\[\[([^\]]*)\]\]", r"\1", oracion)  # [[X]] por X
    # oracion = re.sub(r"\{\{([^\}]*)\}\}", r" ", oracion)  # {{X}} por vacío
    #oracion = re.sub(r"http[s]?://([0-9a-zA-Z/\.\-\+_\?&;=%]+)(\s)?", r"URL\1", oracion)  # Asignar tokens a las URLS

    #oracion = re.sub(r"http[s]?://(\S)+", r"URL\1", oracion)  # Asignar tokens a las URLS
    # oracion = BeautifulSoup(oracion, "lxml").get_text()
    #oracion = re.sub(r"[^0-9a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]", " ", oracion)  # Repasar si falta algún carácter latino
    #oracion = re.sub(r"(\s)+[0-9]+(\s)+", r"DIGITO\1", oracion)

    oracion = re.sub(r"http[s]?://([0-9a-zA-Z/\.\-\+_\?&;=%]+)(\s)", r"URL", oracion)  # Asignar tokens a las URLS
    oracion = re.sub(r"&gt;", r" ", oracion)
    oracion = re.sub(r"\.com", r" ", oracion)
    oracion = re.sub(r"[^0-9a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]", " ", oracion)  # Repasar si falta algún carácter latino
    oracion = re.sub(r"(\s)([0-9\.]+)(\s)", r"\1DIGITO\3", oracion)

    return oracion


nMin = 60
year = 2009

# Initilize tools
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
stopws = set(stopwords.words("english"))
stopws.update(("deleted", "digito", "would"))

tags = set(("NP", "NN", "NNS", "V", "VBZ", "VBG", "VBD"))

# stemmer = SnowballStemmer('english')
# wordnet_lemmatizer = WordNetLemmatizer()




print "Starting processing year " + str(year)
for month in range(2, 3):
    print "===================================="
    print "Start processing month %d" % (month)
    filename = "LoadReddit-" + str(nMin) + "minutes-" + str(year) + "-" + "%02d" % (month,) + "-PLN.csv"
    fmt = '%Y-%m-%d %H:%M:%S'
    init, end = calendar.monthrange(year, month)
    fechaInicio = datetime.strptime(str(year) + '-' + str(month) + '-01 00:00:00', fmt)
    fechaFin = datetime.strptime(str(year) + '-' + str(month) + '-' + str(end) + ' 23:59:59', fmt)

    print fechaInicio
    print fechaFin
    # print (d2-d1).days * 24 * 60

    slotsTemporales = crearSlots(nMin, fechaInicio, fechaFin)

    # for key, value in slotsTemporales.items():
    #        print ([key, value])

    fileN = str(year) + '/RC_' + str(year) + '-' + "%02d" % (month,)
    compressedFileN = fileN + '.bz2'
    print "Processing file " + compressedFileN
    print "Uncompressing file"
    bzip = "bzip2 -k -d " + compressedFileN
    print "Running " + bzip
   # py2output = subprocess.check_output(bzip.split())

    print "Adding , between JSON objects"
    sed1 = "sed -ie s/\}/\},/g " + fileN
    print "Running " + sed1
 #   py2output = subprocess.check_output(sed1.split())
    print "Finished adding , ."

    print "Adding [ at the beginning"
    sed2 = "sed -ie 1s/^/[/ " + fileN
    print "Running " + sed2
   # py2output = subprocess.check_output(sed2.split())
    print "Finished adding [ ."

    print "Adding ] at the end"
    sed3 = "sed -ie $s/\(.*\),/" + "\\" + "1]/ " + fileN
    print "Running " + sed3
   # py2output = subprocess.check_output(sed3.split())
    print "Finished adding ] ."

    f = open(fileN)

    parser = ijson.parse(f)
    print "Parsing file " + fileN

    # initialize collections
    fdist = nltk.FreqDist([])

    fechaAnterior = fechaInicio

    textFilename = str(year)+"/Bodies/BodiesReddit-" + str(nMin) + "minutes-"


    text_file = open(textFilename+str(fechaInicio)+".txt", "w")

    for prefix, event, value in parser:

        if (prefix, event) == ('item.created_utc', 'string'):
            try:
                fechaLeida = datetime.fromtimestamp(int(value))
                # print fechaLeida.strftime(fmt)
                fechaCorrecta = fechaLeida - timedelta(minutes=60)
                # print fechaCorrecta.strftime(fmt)
                fechaGuapa = fechaCorrecta - timedelta(minutes=fechaCorrecta.minute % nMin)
                fechaGuapa = fechaGuapa.replace(second=0)
                # print fechaGuapa.strftime(fmt)
                # fechaGuapa = fechaCorrecta.replace(hour=0,minute=0,second=0)

                if (fechaAnterior < fechaGuapa):
                    # d[year].append(value)
                    fdist = nltk.FreqDist([])
                    text_file.close()
                    print "Saved bodies at:"+textFilename+str(fechaAnterior)+".txt"
                    text_file = open(textFilename +str(fechaGuapa)+".txt", "w")


                fechaAnterior = fechaGuapa
            except KeyError, e:
                print 'Oops, KeyError - reason "%s"' % str(e)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise
        if (prefix, event) == ('item.body', 'string'):
            text_file.write(value.encode("utf-8"))
            # TODO quitar enters y tabulaciones y grupos de espacios

            #TODO generar archivo de texto con formato: subreddit_name [TAB] body(sin enters, etc.) y agregar un enter

            #sentences = map(limpia, tokenizer.tokenize(value))
            #for sentence in sentences:
            #    words = [w for w in word_tokenize(sentence)]
            #    pos = nltk.pos_tag(words)
            #    pos_by_tags = [word for word, tag in pos if tag in tags and word not in stopws]
            #    fdist.update(nltk.FreqDist(pos_by_tags))  # print(fdist.most_common(50))



text_file.close()

# with open(filename, 'wb') as csv_file:
#     writer = csv.writer(csv_file)
#     for key, value in slotsTemporales.items():
#         writer.writerow([key, value])

print "Deleting uncompressed files"
rm = "rm " + fileN
print "Running " + rm
py2output = subprocess.check_output(rm.split())

rm = "rm " + fileN + "e"
print "Running " + rm
py2output = subprocess.check_output(rm.split())
