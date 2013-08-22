#!/usr/bin/env python

from lxml import etree
from pprint import pprint
import csv
from lib import db
from lib.model import *
from sqlalchemy import *

db.models.metadata.create_all()

def get_related_activity(activity):
    related_activity = db.session.query(RelatedActivity
            ).filter(RelatedActivity.activity_id==activity.iati_identifier
            ).filter(RelatedActivity.reltype=='1'
            ).first()

    if related_activity:
        related_activity_details = db.session.query(Activity
                ).filter(Activity.iati_identifier==related_activity.relref
                ).first()

        # get parent activity details (should only be 1)
        if related_activity_details is not None:
            reladescription = related_activity_details.title
            relatitle = related_activity_details.description
            return relatitle, reladescription
    return '', ''

def notEmpty(value):
    if value is None:
        return False
    if value == '':
        return False
    return True

def get_values(out, transaction, activity, transaction_or_activity_fields):
    for field in transaction_or_activity_fields:
        trans = getattr(transaction, field)
        if notEmpty(trans):
            out[field] = trans
        else:
            out[field] = getattr(activity, field)
    return out

def valToString(val):
    if val is not None:
        return str(val)
    return ""

def getTransactionIdentifier(out, transaction, activity, rownumber):
    if notEmpty(activity.recipient_country_code):
        activity_location_identifier = activity.recipient_country_code
    elif notEmpty(activity.recipient_region_code):
        activity_location_identifier = activity.recipient_region_code
    else:
        activity_location_identifier = 'x'

    parts = [transaction.iati_identifier, 
             activity_location_identifier, 
             valToString(transaction.transaction_type_code), 
             valToString(transaction.transaction_date_iso), 
             str(rownumber)]

    out['rowid'] = "-".join(parts)
    return out

def getActivityRecipientLocation(out, activity):
    if notEmpty(activity.recipient_country_code):
        out["recipient_location"] = activity.recipient_country
        out["recipient_location_code"] = activity.recipient_country_code
    elif notEmpty(activity.recipient_region_code):
        out["recipient_location"] = activity.recipient_region
        out["recipient_location_code"] = activity.recipient_region_code
    else:
        out["recipient_location"] = ""
        out["recipient_location_code"] = ""
    return out

def generate_row(out,
                 activity, 
                 transaction, 
                 sector_value, 
                 sector_name, 
                 sector_code, 
                 sector_vocabulary):

    remaining_fields = [
        ('item_value', sector_value),
        ('item_sector', sector_name),
        ('item_sector_code', sector_code),
        ('item_sector_vocabulary', sector_vocabulary),
        ('activity_id', transaction.activity_id),
        ('iati_identifier', transaction.iati_identifier),
        ('transaction_type', transaction.transaction_type),
        ('transaction_type_code', transaction.transaction_type_code),
        ('provider_org', transaction.provider_org),
        ('provider_org_ref', transaction.provider_org_ref),
        ('provider_org_type', transaction.provider_org_type),
        ('receiver_org', transaction.receiver_org),
        ('receiver_org_ref', transaction.receiver_org_ref),
        ('receiver_org_type', transaction.receiver_org_type),
        ('transaction_description', transaction.description),
        ('transaction_date', transaction.transaction_date),
        ('transaction_date_iso', transaction.transaction_date_iso),
        ('transaction_disbursement_channel_code', transaction.disbursement_channel_code),
        ('package_id', activity.package_id),
        ('source_file', activity.source_file),
        ('activity_lang', activity.activity_lang),
        ('activity_last_updated', activity.last_updated),
        ('activity_reporting_org', activity.reporting_org),
        ('activity_reporting_org_ref', activity.reporting_org_ref),
        ('activity_reporting_org_type', activity.reporting_org_type),
        ('activity_funding_org', activity.funding_org),
        ('activity_funding_org_ref', activity.funding_org_ref),
        ('activity_funding_org_type', activity.funding_org_type),
        ('activity_extending_org', activity.extending_org),
        ('activity_extending_org_ref', activity.extending_org_ref),
        ('activity_extending_org_type', activity.extending_org_type),
        ('activity_implementing_org', activity.implementing_org),
        ('activity_implementing_org_ref', activity.implementing_org_ref),
        ('activity_implementing_org_type', activity.implementing_org_type),
        ('activity_recipient_region', activity.recipient_region),
        ('activity_recipient_region_code', activity.recipient_region_code),
        ('activity_recipient_country', activity.recipient_country),
        ('activity_recipient_country_code', activity.recipient_country_code),
        ('title', activity.title),
        ('date_start_actual', activity.date_start_actual),
        ('date_start_planned', activity.date_start_planned),
        ('date_end_actual', activity.date_end_actual),
        ('date_end_planned', activity.date_end_planned),
        ('status', activity.status),
        ('status_code', activity.status_code),
        ('contact_organisation', activity.contact_organisation),
        ('contact_telephone', activity.contact_telephone),
        ('contact_email', activity.contact_email),
        ('contact_mailing_address', activity.contact_mailing_address),
        ('activity_website', activity.activity_website)           
    ]
    for field, var in remaining_fields:
        out[field] = var
    return out

def run(filename):
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
        out = {}

        activity = db.session.query(Activity
            ).filter(Activity.iati_identifier==transaction.iati_identifier
            ).first()

        related_activity_title, related_activity_description = get_related_activity(activity)

        if notEmpty(related_activity_description):
            out['description'] = related_activity_description
        else:
            out['description'] = activity.description

        if ((transaction.value_currency) and (transaction.value_currency != '')):
            out['value_currency'] = transaction.value_currency
        else:
            out['value_currency'] = activity.default_currency

        transaction_or_activity_fields = {'flow_type', 
                                          'flow_type_code', 
                                          'aid_type',
                                          'aid_type_code',
                                          'finance_type',
                                          'finance_type_code',
                                          'tied_status',
                                          'tied_status_code'}

        get_values(out, transaction, activity, transaction_or_activity_fields)

        getTransactionIdentifier(out, transaction, activity, rownumber)

        if notEmpty(transaction.value_date):
            out['value_date'] = transaction.value_date
        else:
            out['value_date'] = transaction.transaction_date_iso

        getActivityRecipientLocation(out, activity)

        sectors = db.session.query(Sector
                ).filter_by(activity_iati_identifier=activity.iati_identifier
                )

        minitransaction_id = 1
        if (sectors.count()>0):
            for sector in sectors:

                if ((sector.percentage == 100) and ((sectors.count())>0)):
                    realsectorpercentage = (sector.percentage/sectors.count())
                else:
                    realsectorpercentage = sector.percentage
                try:
                   	sector_value = (((float(realsectorpercentage))/100)*(transaction.value))
                except TypeError:
                    sector_value = ""

                generate_row(out,
                             activity, 
                             transaction, 
                             sector_value, 
                             sector.name, 
                             sector.code, 
                             sector.vocabulary)
                
                thetransactions.append(out)
                rownumber = rownumber +1
        else:
            sector_value = (transaction.value)
            generate_row(out,
                         activity, 
                         transaction, 
                         sector_value, 
                         "Unknown", 
                         "unknown", 
                         "unknown")

            thetransactions.append(out)
            rownumber = rownumber +1
        i = i +1
	if ((i % 100) == 0):
            print "Collected " + str(i) + " rows"

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
    
    print "Writing transactions to CSV..."
    write_csv(thetransactions, filename)
    print "Written to CSV file iatidata.csv"
    print ""
    print "Finished compiling IATI OpenSpending-CSV file"
                
def write_csv(transactions, filename):
    fh = open(filename, 'w')
    keys = []

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
    filename = 'iatidata.csv'
    run(filename)
