def run():
    print "Compile your CSV files"
    print ""
    print "Starting up..."
    fout=open("IATIdata.csv","a")
    # first file:
    print "Processing iatidata0.csv ..."
    for line in open("csv/iatidata0.csv"):
        fout.write(line)
    # now the rest:    
    for num in range(1,73):
        print "Processing iatidata"+str(num)+".csv ..."
        f = open("csv/iatidata"+str(num)+".csv")
        f.next() # skip the header
        for line in f:
             fout.write(line)
        f.close() # not really needed
    fout.close()

if __name__ == '__main__':
    import sys
    run()
