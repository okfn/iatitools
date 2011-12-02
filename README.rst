
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

Issues
------

* Some publishers only release per-country or per-region data, we need
  to map from country to region to allow at one common facet.
* Multiple policy markers are set for a single transaction; we have 
  no way of expressing this in OpenSpending. 


Licensing
---------

Derived data can be reused under the same licensing conditions as the 
IATI source data or ODC ODbL. Code is GPLv3.

