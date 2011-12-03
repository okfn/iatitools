
International Aid Transparency Initiative OpenSpending Mapping
==============================================================

The scripts in this repository transform IATI data into an appropriate
shape for import into OpenSpending. This involves: 

* Traversing the IATI registry to get a list of all available activity
  record resources. 
* Downloading the activity files.
* Traversing each transaction with in and yielding a CSV row with data 
  from the transaction and the sourrounding activtiy. 
* Padding up the data and normalizing values. 

Scripts
-------

1-iatidownload.py - will download all files from the IATI Registry. This will take some time as there are quite a lot now!
Please note that the Netherlands data file linked to on the IATI Registry is not in XML, as it is zipped. You'll need to rename the activity file to a ZIP file and extract it.

Files will be downloaded to the subfolder /packages/YYYY-MM-DD (for today's date).

2-iati2sqlite.py - will parse all files in a given folder and put them into a simple SQLite database

You can give this file an argument if you want it to point at a particular folder within the /packages folder. For example, if you've placed the Netherlands data file into a subfolder called "/packages/Netherlands":
python 2-iati2sqlite.py Netherlands

Errors will be logged to log-YYYY-MM-DD.txt (for today's date)

3-iatisqlite2csv.py - will compile an OpenSpending CSV file from the SQLite data. This will not be normalised or reconciled. In order to make sure that the data is saved in case the script crashes (or the computer turns off), the CSV is generated every 1000 rows and saved as iatidata0.csv where 0 is the number of the CSV file. So you will end up with a lot of CSV files :)

4-iaticompile.py - will combine all of the CSV files that you place into a /csv subfolder. NB you have to move all the CSV files there as it will not work otherwise

Mapping 
-------

IATI_OpenSpending_model.json - file to map the dimensions of the IATI Data to OpenSpending. It should import successfully with no errors, but please let me know if this is not the case
IATI_OpenSpending_views.json - file to run the Views functionality of OpenSpending with some simple views - this file could definitely be improved.

The /mapping folder also contains:
ISO-DAC-Countries-Regions.csv - file to map countries to regions
spine-dac-crs.csv - file to map DAC/CRS Sector codes to a common "Spine" sector code
spine-wbsectors.csv - file to map World Bank Sector codes to a common "Spine" sector code
GOOGLE REFINE COMMANDS - which provides commands you could use to reconcile the data.


Issues
------

* Some publishers only release per-country or per-region data, we need
  to map from country to region to allow at one common facet.

Licensing
---------

Derived data can be reused under the same licensing conditions as the 
IATI source data or ODC ODbL. Code is GPLv3.

