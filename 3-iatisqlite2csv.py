#!/usr/bin/env python

from lxml import etree
from pprint import pprint
import csv
from lib import db
from lib.model import *
from sqlalchemy import *

db.models.metadata.create_all()

# each transaction:
    # get transaction details
        # get activity details
            # get sectors
            # get parent activity details (if related_activity reltype = '1')
    # construct CSV to write
        # flow type, aid type, description, etc. => standardise / collect
        # also add title from parent activity
        # also get currency from parent activity if it's not in the transaction or activity
        # for each sector
            # multiply transaction value by sector percentage/100
            # get sector details
            # write that
    # write to CSV
def run():
    print ""
    print "IATI OpenSpending-CSV compiler"
    print "=============================="
    print ""
    rownumber = 1
    thisnumber = 0
    # get transactions
    transactions = db.session.query(Transaction)
    print "Found " + str(transactions.count()) + " transactions."
    print ""
    print "Processing..."
    print ""
    i = 0
    for transaction in transactions:
        #Some transactions are bound to fail :-(
        try:
            # get transaction's activity (should only be 1)
            try:
                activities = db.session.query(Activity).filter(Activity.iati_identifier==transaction.iati_identifier)
            except:
                pass
            for activity in activities:
                # get parent activity details (should only be 1)
                related_activities = db.session.query(RelatedActivity).filter(RelatedActivity.activity_id==activity.iati_identifier).filter(RelatedActivity.reltype=='1')
                reladescription = ''
                relatitle = ''
                for related_activity in related_activities:
                    # get the related activity's details
                    related_activity_details = db.session.query(Activity).filter(Activity.iati_identifier==related_activity.relref)
                    for related_activity_detail in related_activity_details:
                        relatitle = related_activity_detail.title
                        reladescription = related_activity_detail.description
                if ((reladescription) and (reladescription != '')):
		            thedescription = reladescription
                else:
                    thedescription = activity.description

                if ((transaction.value_currency) and (transaction.value_currency != '')):
                    thevalue_currency = transaction.value_currency
                else:
                    thevalue_currency = activity.default_currency
                # finance type
                # tied aid status

                if ((transaction.flow_type) and (transaction.flow_type!='')):
                    theflow_type = transaction.flow_type
                    theflow_type_code = transaction.flow_type_code
                else:
                    theflow_type = activity.flow_type
                    theflow_type_code = activity.flow_type_code

                if ((transaction.aid_type) and (transaction.aid_type!='')):
                    theaid_type = transaction.aid_type
                    theaid_type_code = transaction.aid_type_code
                else:
                    theaid_type = activity.aid_type
                    theaid_type_code = activity.aid_type_code

                if ((transaction.finance_type) and (transaction.finance_type!='')):
                    thefinance_type = transaction.finance_type
                    thefinance_type_code = transaction.finance_type_code
                else:
                    thefinance_type = activity.finance_type
                    thefinance_type_code = activity.finance_type_code

                if ((transaction.finance_type) and (transaction.finance_type!='')):
                    thefinance_type = transaction.finance_type
                    thefinance_type_code = transaction.finance_type_code
                else:
                    thefinance_type = activity.finance_type
                    thefinance_type_code = activity.finance_type_code

                if ((transaction.tied_status_code) and (transaction.tied_status_code!='')):
                    thetied_status_code = transaction.tied_status_code
                  # tied_status Text doesn't appear in WB or DFID transactions.
                    thetied_status = ''
                else:
                    thetied_status = activity.tied_status
                    thetied_status_code = activity.tied_status_code
                if (relatitle and relatitle != ''):
                    related_activity_title = relatitle
                else:
                    related_activity_title = ''   
                if (reladescription and reladescription != ''):
                    related_activity_description = reladescription
                else:
                    related_activity_description = ''     
                # get sectors
                sectors = db.session.query(Sector).filter_by(activity_iati_identifier=activity.iati_identifier)
                # will only write a transaction if it is in a sector!
                minitransaction_id = 1
                if (sectors.count()>0):
                    for sector in sectors:
                        # Sometimes there are multiple sectors, with 100% each. Partly an import error :(
                        if ((sector.percentage == 100) and ((sectors.count())>0)):
                            realsectorpercentage = (sector.percentage/sectors.count())
                        else:
                            realsectorpercentage = sector.percentage
                        try:
                           	thisectorvalue = (((float(realsectorpercentage))/100)*(transaction.value))
                        except TypeError:
                            pass
                        # write to CSV:
                        activity_location_identifier = ''
                        if (activity.recipient_country_code is not None):
                            activity_location_identifier = activity.recipient_country_code
                        elif (activity.recipient_region_code is not None):
                            activity_location_identifier = activity.recipient_region_code
                        else:
                            activity_location_identifier = 'x'
                        transaction_identifier = transaction.iati_identifier + "-" + activity_location_identifier + "-" + transaction.transaction_type_code + "-" + str(transaction.transaction_date_iso) + "-" + str(rownumber)
                        try:
                            if ((transaction.value_date == '') or (transaction.value_date == None)):
                                transactionvaluedate = transaction.transaction_date_iso
                            else:
                                transactionvaluedate = transaction.value_date
                        except:
                            pass
                        activity_recipient_location =''
                        activity_recipient_location_code =''
                        
                        if (activity.recipient_country is not None):
                            activity_recipient_location = activity.recipient_country
                        elif (activity.recipient_region is not None):
                            activity_recipient_location = activity.recipient_region
                        
                        if (activity.recipient_country_code is not None):
                            activity_recipient_location_code = activity.recipient_country_code
                        elif (activity.recipient_region_code is not None):
                            activity_recipient_location_code = activity.recipient_region_code
                        
                        transactiondata = {
                            'rowid':transaction_identifier,
		                    'transaction_id': transaction.id,
                            'item_value': thisectorvalue,
                            'item_sector': sector.name,
                            'item_sector_code': sector.code,
                            'item_sector_vocabulary': sector.vocabulary,
                            'activity_id': transaction.activity_id,
                            'iati_identifier': transaction.iati_identifier,
                            'value_date': transactionvaluedate,
                            'currency': thevalue_currency,
                            'description': thedescription,
                            'flow_type': theflow_type,
                            'flow_type_code': theflow_type_code,
                            'aid_type': theaid_type,
                            'aid_type_code': theaid_type_code,
                            'finance_type': thefinance_type,
                            'finance_type_code': thefinance_type_code,
                            'tied_status_code': thetied_status_code,
                            'tied_status': thetied_status,
                            'transaction_type': transaction.transaction_type,
                            'transaction_type_code': transaction.transaction_type_code,
                            'provider_org': transaction.provider_org,
                            'provider_org_ref': transaction.provider_org_ref,
                            'provider_org_type': transaction.provider_org_type,
                            'receiver_org': transaction.receiver_org,
                            'receiver_org_ref': transaction.receiver_org_ref,
                            'receiver_org_type': transaction.receiver_org_type,
                            'transaction_description': transaction.description,
                            'transaction_date': transaction.transaction_date,
                            'transaction_date_iso': transaction.transaction_date_iso,
                            'transaction.disbursement_channel_code': transaction.disbursement_channel_code,
                            'package_id': activity.package_id,
                            'source_file': activity.source_file,
                            'activity_lang': activity.activity_lang,
                            'activity_last_updated': activity.last_updated,
                            'activity_reporting_org': activity.reporting_org,
                            'activity_reporting_org_ref': activity.reporting_org_ref,
                            'activity_reporting_org_type': activity.reporting_org_type,
                            'activity_funding_org': activity.funding_org,
                            'activity_funding_org_ref': activity.funding_org_ref,
                            'activity_funding_org_type': activity.funding_org_type,
                            'activity_extending_org': activity.extending_org,
                            'activity_extending_org_ref': activity.extending_org_ref,
                            'activity_extending_org_type': activity.extending_org_type,
                            'activity_implementing_org': activity.implementing_org,
                            'activity_implementing_org_ref': activity.implementing_org_ref,
                            'activity_implementing_org_type': activity.implementing_org_type,
                            'activity_recipient_region': activity.recipient_region,
                            'activity_recipient_region_code': activity.recipient_region_code,
                            'activity_recipient_country': activity.recipient_country,
                            'activity_recipient_country_code': activity.recipient_country_code,
                            'activity_recipient_location':activity_recipient_location,
                            'activity_recipient_location_code':activity_recipient_location_code,
                            'title':activity.title,
                            'date_start_actual': activity.date_start_actual,
                            'date_start_planned': activity.date_start_planned,
                            'date_end_actual': activity.date_end_actual,
                            'date_end_planned': activity.date_end_planned,
                            'status': activity.status,
                            'status_code': activity.status_code,
                            'contact_organisation': activity.contact_organisation,
                            'contact_telephone': activity.contact_telephone,
                            'contact_email': activity.contact_email,
                            'contact_mailing_address': activity.contact_mailing_address,
                            'activity_website': activity.activity_website,
                            'related_activity_title': related_activity_title                      
                        }
                        thetransactions.append(transactiondata)
                        rownumber = rownumber +1
                else:
                    realsectorpercentage = '100'
                    thisectorvalue = (transaction.value)
                    # write to CSV:
                    try:
                        transaction_identifier = transaction.iati_identifier + "-" + transaction.transaction_type_code + "-" + str(transaction.transaction_date_iso) + "-" + str(rownumber)
                    except:
                        pass
                    # create default value date if one is not provided (based on transaction date)
                    try:
                        if ((transaction.value_date == '') or (transaction.value_date == None)):
                            transactionvaluedate = transaction.transaction_date_iso
                        else:
                            transactionvaluedate = transaction.value_date          
                    except:
                        pass      
                    activity_recipient_location =''
                    activity_recipient_location_code =''
                    
                    if (activity.recipient_country is not None):
                        activity_recipient_location = activity.recipient_country
                    elif (activity.recipient_region is not None):
                        activity_recipient_location = activity.recipient_region
                    
                    if (activity.recipient_country_code is not None):
                        activity_recipient_location_code = activity.recipient_country_code
                    elif (activity.recipient_region_code is not None):
                        activity_recipient_location_code = activity.recipient_region_code
                    
                    transactiondata = {
                        'rowid':transaction_identifier,
	                    'transaction_id': transaction.id,
                        'item_value': thisectorvalue,
                        'item_sector': 'Unknown',
                        'item_sector_code': 'unknown',
                        'item_sector_vocabulary': 'unknown',
                        'activity_id': transaction.activity_id,
                        'iati_identifier': transaction.iati_identifier,
                        'value_date': transactionvaluedate,
                        'currency': thevalue_currency,
                        'description': thedescription,
                        'flow_type': theflow_type,
                        'flow_type_code': theflow_type_code,
                        'aid_type': theaid_type,
                        'aid_type_code': theaid_type_code,
                        'finance_type': thefinance_type,
                        'finance_type_code': thefinance_type_code,
                        'tied_status_code': thetied_status_code,
                        'tied_status': thetied_status,
                        'transaction_type': transaction.transaction_type,
                        'transaction_type_code': transaction.transaction_type_code,
                        'provider_org': transaction.provider_org,
                        'provider_org_ref': transaction.provider_org_ref,
                        'provider_org_type': transaction.provider_org_type,
                        'receiver_org': transaction.receiver_org,
                        'receiver_org_ref': transaction.receiver_org_ref,
                        'receiver_org_type': transaction.receiver_org_type,
                        'transaction_description': transaction.description,
                        'transaction_date': transaction.transaction_date,
                        'transaction_date_iso': transaction.transaction_date_iso,
                        'transaction.disbursement_channel_code': transaction.disbursement_channel_code,
                        'package_id': activity.package_id,
                        'source_file': activity.source_file,
                        'activity_lang': activity.activity_lang,
                        'activity_last_updated': activity.last_updated,
                        'activity_reporting_org': activity.reporting_org,
                        'activity_reporting_org_ref': activity.reporting_org_ref,
                        'activity_reporting_org_type': activity.reporting_org_type,
                        'activity_funding_org': activity.funding_org,
                        'activity_funding_org_ref': activity.funding_org_ref,
                        'activity_funding_org_type': activity.funding_org_type,
                        'activity_extending_org': activity.extending_org,
                        'activity_extending_org_ref': activity.extending_org_ref,
                        'activity_extending_org_type': activity.extending_org_type,
                        'activity_implementing_org': activity.implementing_org,
                        'activity_implementing_org_ref': activity.implementing_org_ref,
                        'activity_implementing_org_type': activity.implementing_org_type,
                        'activity_recipient_region': activity.recipient_region,
                        'activity_recipient region_code': activity.recipient_region_code,
                        'activity_recipient_country': activity.recipient_country,
                        'activity_recipient_country_code': activity.recipient_country_code,
                        'activity_recipient_location':activity_recipient_location,
                        'activity_recipient_location_code':activity_recipient_location_code,
                        'title':activity.title,
                        'date_start_actual': activity.date_start_actual,
                        'date_start_planned': activity.date_start_planned,
                        'date_end_actual': activity.date_end_actual,
                        'date_end_planned': activity.date_end_planned,
                        'status': activity.status,
                        'status_code': activity.status_code,
                        'contact_organisation': activity.contact_organisation,
                        'contact_telephone': activity.contact_telephone,
                        'contact_email': activity.contact_email,
                        'contact_mailing_address': activity.contact_mailing_address,
                        'activity_website': activity.activity_website,
                        'related_activity_title': related_activity_title                      
                    }
                    thetransactions.append(transactiondata)
                    rownumber = rownumber +1
        except:
            pass
        i = i +1
	if ((i % 100) == 0):
            print "Collected " + str(i) + " rows"
        # write to CSV every 100,000 transactions)
	"""
        if (i >= 100,000):
            # write to CSV
            print "Writing to CSV..."
            filename = 'iatidata' + str(thisnumber) + '.csv'
            write_csv(thetransactions, filename)
            print "Written to CSV file iatidata" + str(thisnumber) + ".csv"
            print ""
            print ""    
            # reset counter
            i = 0
            # reset thetransactions
            del thetransactions[:]
            # create version number
            thisnumber = thisnumber +1
	"""
    # at end of loop, write remaining transactions.
    
    filename = 'iatidata.csv'
    print "Writing transactions to CSV..."
    write_csv(thetransactions, filename)
    print "Written to CSV file iatidata.csv"
    print ""
    print "Finished compiling IATI OpenSpending-CSV file"
                
def write_csv(transactions, filename):
    fh = open(filename, 'w')
    keys = []
    #print transactions
    for transaction in transactions:
        keys.extend(transaction.keys())
    writer = csv.DictWriter(fh, fieldnames=list(set(keys)))
    writer.writerow(dict([(k,k) for k in keys]))
    for transaction in transactions:
        try:
            row = dict([(k, unicode(v).encode('utf-8')) for (k, v) in transaction.items() if
                v is not None])
            writer.writerow(row)
        except:
            pass
    fh.close()
            

if __name__ == '__main__':
    import sys
    thetransactions = []
    run()
