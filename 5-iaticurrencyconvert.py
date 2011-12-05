import csv
import string
import pprint as pp

def run():
    # convert `item_value` based on `currency`
    print "Convert currencies in your IATI OpenSpending-CSV data file"
    print ""
    print "Starting up..."
    f=open("compiled/IATIdata_05122011.csv","r")
    sourcefile=csv.DictReader(f)
    outputfile=open("IATIdata_currency_standardised.csv","a")
    # first file:
    print "Processing data.csv ..."
    fieldnames = sourcefile.fieldnames    
    fieldnames.append("amount_USD")
    out = csv.DictWriter(outputfile, fieldnames=fieldnames)
    out.writerow(dict((fn,fn) for fn in fieldnames))
    for line in sourcefile:
         line["currency"] = (string.upper(line["currency"]))
         currency=line["currency"]
         amount_USD = 0
         amount_original = float(line["item_value"])

         #very crude currency conversion... just using 2010 average for GBP and EUR from OECD Stats

         if ((string.upper(currency)) == u'EUR'):
             amount_USD = (amount_original/0.755)
         elif ((string.upper(currency)) == u'GBP'):
             amount_USD = (amount_original/0.647)
         else:
             amount_USD = amount_original
         line["amount_USD"] =amount_USD	
         out.writerow(line)

    sourcefile.close()

if __name__ == '__main__':
    import sys
    run()
