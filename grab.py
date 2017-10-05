import urllib2
import os
import gzip
import glob
import subprocess
import argparse
import datetime

parser = argparse.ArgumentParser(description='Download RINEX files from NOAA CORS database')
parser.add_argument('-b', '--base', type=str, metavar='', required=True, help='base station ID')
parser.add_argument('-s', '--start', type=str, metavar='', required=True, help='Start Time in ISO8601 format')
parser.add_argument('-e', '--end', type=str, metavar='', required=True, help='End Time in ISO8601 format')
args = parser.parse_args()

#takes a time string and returns the associated letter e.g 00:00 - 00:59 will return a
def convertTime(t):
    t1 = datetime.datetime.strftime(t, "%H:%M")
    t1 = str(t1)
    if t1 >= '00:00' and t1 <= '00:59':
        return 'a'
    elif t1 >= '01:00' and t1 <= '01:59':
        return 'b'
    elif t1 >= '02:00' and t1 <= '02:59':
        return 'c'
    elif t1 >= '03:00' and t1 <= '03:59':
        return 'd'
    elif t1 >= '04:00' and t1 <= '04:59':
        return 'e'
    elif t1 >= '05:00' and t1 <= '05:59':
        return 'f'
    elif t1 >= '06:00' and t1 <= '06:59':
        return 'g'
    elif t1 >= '07:00' and t1 <= '07:59':
        return 'h'
    elif t1 >= '08:00' and t1 <= '08:59':
        return 'i'
    elif t1 >= '09:00' and t1 <= '09:59':
        return 'j'
    elif t1 >= '10:00' and t1 <= '10:59':
        return 'k'
    elif t1 >= '11:00' and t1 <= '11:59':
        return 'l'
    elif t1 >= '12:00' and t1 <= '12:59':
        return 'm'
    elif t1 >= '13:00' and t1 <= '13:59':
        return 'n'
    elif t1 >= '14:00' and t1 <= '14:59':
        return 'o'
    elif t1 >= '15:00' and t1 <= '15:59':
        return 'p'
    elif t1 >= '16:00' and t1 <= '16:59':
        return 'q'
    elif t1 >= '17:00' and t1 <= '17:59':
        return 'r'
    elif t1 >= '18:00' and t1 <= '18:59':
        return 's'
    elif t1 >= '19:00' and t1 <= '19:59':
        return 't'
    elif t1 >= '20:00' and t1 <= '20:59':
        return 'u'
    elif t1 >= '21:00' and t1 <= '21:59':
        return 'v'
    elif t1 >= '22:00' and t1 <= '22:59':
        return 'w'
    elif t1 >= '23:00' and t1 <= '23:59':
        return 'x'
    else:
        return '0'

#convert the input from the input into a array
def getInput():
    x = []
    x.append(args.base)
    x.append(datetime.datetime.strptime(args.start, "%Y-%m-%dT%H:%M:%SZ"))
    x.append(datetime.datetime.strptime(args.end, "%Y-%m-%dT%H:%M:%SZ"))
    return x

#takes the date and returns the day number of that particular year
def getDayNumber(date):
    temp = []
    temp.append(datetime.datetime.strftime(date, "%Y"))
    date = date.timetuple().tm_yday
    temp.append(date)
    return temp

#will download files from server and save to specified directory
def getFiles(arr):
    genericLink = "ftp://www.ngs.noaa.gov/cors/rinex/%s/%s/%s/%s%s%s.%so.gz"
    start = arr[1]
    end = arr[2]
    site = arr[0]
    fileList = []
    while start <= end:
        year, daynum = getDayNumber(start)
        timeletter = convertTime(start)
        url = genericLink%(year, daynum, site, site, daynum, timeletter, year.replace(' ', '')[-2:])
        fileName = "%s%s%s.%so.gz"%(site, daynum, timeletter, year.replace(' ', '')[-2:])
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = response.read()
        with open(fileName, 'wb') as fh:
            fh.write(data)
        fileList.append(fileName)
        start += datetime.timedelta(hours=1)
    return fileList

#sice files are G-Zipped, this function will unzip all the files which were downloaded
def unzipfiles(fileList):
    for files in fileList:
        f = gzip.open(files, 'rb')
        file_content = f.read()
        with open(files[:-3], 'wb') as gh:
            gh.write(file_content)
    f.close()
    for files in fileList:
        os.remove(files)
        print "removed"

#merge all the files with ."yearnum"o extension
def mergeFiles():
    filenames = []
    fileString = ""
    for file in glob.glob("*.*o"):
        fileString += file + " "
        filenames.append(file)
    print fileString

    callString = "teqc +obs + +nav +,+ -tbin 1d tbinoutput %s"
    send = callString % fileString
    subprocess.call(send)

    for i in filenames:
        os.remove(i)

def main():
    print args.base, args.start, args.end
    path = os.getcwd()
    x = getInput()
    filesList = getFiles(x)
    unzipfiles(filesList)
    mergeFiles()
    print "done"

if __name__ == "__main__":
    main()