import string
import csv

def run():
    f=open("csv/iatidata0.csv")
    sourcefile=csv.DictReader(f)
    outputfile=open("IATIdata.csv","a")

    print "Compile your CSV files"
    print ""
    print "Starting up..."
    
    fieldnames = sourcefile.fieldnames
    out = csv.DictWriter(outputfile, fieldnames=fieldnames)
    out.writerow(dict((fn,fn) for fn in fieldnames))
    
    for line in sourcefile:
        out.writerow(line)
    
    for num in range(1,150):
        print "Processing iatidata"+str(num)+".csv ..."
        f = open("csv/iatidata"+str(num)+".csv")
        parsefile = csv.DictReader(f)
        for line in parsefile:
             out.writerow(line)
        f.close() # not really needed
        
    sourcefile.close()

if __name__ == '__main__':
    import sys
    run()
