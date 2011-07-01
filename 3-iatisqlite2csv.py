from lxml import etree
from pprint import pprint
import csv
import sqlalchemy
from sqlalchemy import create_engine
engine = create_engine('sqlite:///iatidata_new.sqlite', echo=False)

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, UnicodeText, Date, Float
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
Session = sessionmaker()
session = Session()


Base = declarative_base()

Base.metadata.bind = engine
class Activity(Base):
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True)
    package_id = Column(UnicodeText)
    source_file = Column(UnicodeText)
    activity_lang = Column(UnicodeText)
    default_currency = Column(UnicodeText)
    hierarchy = Column(UnicodeText)
    last_updated = Column(UnicodeText)
    reporting_org = Column(UnicodeText)
    reporting_org_ref = Column(UnicodeText)
    reporting_org_type = Column(UnicodeText)
    funding_org = Column(UnicodeText)
    funding_org_ref = Column(UnicodeText)
    funding_org_type = Column(UnicodeText)
    extending_org = Column(UnicodeText)
    extending_org_ref = Column(UnicodeText)
    extending_org_type = Column(UnicodeText)
    implementing_org = Column(UnicodeText)
    implementing_org_ref = Column(UnicodeText)
    implementing_org_type = Column(UnicodeText)
    recipient_region = Column(UnicodeText)
    recipient_region_code = Column(UnicodeText)
    recipient_country = Column(UnicodeText)
    recipient_country_code = Column(UnicodeText)
    collaboration_type = Column(UnicodeText)
    collaboration_type_code = Column(UnicodeText)
    flow_type = Column(UnicodeText)
    flow_type_code = Column(UnicodeText)
    aid_type = Column(UnicodeText)
    aid_type_code = Column(UnicodeText)
    finance_type = Column(UnicodeText)
    finance_type_code = Column(UnicodeText)
    iati_identifier = Column(UnicodeText)
    title = Column(UnicodeText)
    description = Column(UnicodeText)
    date_start_actual = Column(UnicodeText)
    date_start_planned = Column(UnicodeText)
    date_end_actual = Column(UnicodeText)
    date_end_planned = Column(UnicodeText)    
    status_code = Column(UnicodeText)
    status = Column(UnicodeText)
    contact_organisation = Column(UnicodeText)
    contact_telephone = Column(UnicodeText)
    contact_email = Column(UnicodeText)
    contact_mailing_address = Column(UnicodeText)
    tied_status = Column(UnicodeText)
    tied_status_code = Column(UnicodeText)
    activity_website = Column(UnicodeText)
    #countryregion_id = Column(

class Transaction(Base):
    __tablename__ = 'atransaction'
    id = Column(Integer, primary_key=True)
    activity_id = Column(UnicodeText)
    value = Column(Float)
    iati_identifier = Column(UnicodeText)
    value_date = Column(UnicodeText)
    value_currency = Column(UnicodeText)
    transaction_type = Column(UnicodeText)
    transaction_type_code = Column(UnicodeText)
    provider_org = Column(UnicodeText)
    provider_org_ref = Column(UnicodeText)
    provider_org_type = Column(UnicodeText)
    receiver_org = Column(UnicodeText)
    receiver_org_ref = Column(UnicodeText)
    receiver_org_type = Column(UnicodeText)
    description = Column(UnicodeText)
    transaction_date = Column(UnicodeText)
    transaction_date_iso = Column(Date)
    flow_type = Column(UnicodeText)
    flow_type_code = Column(UnicodeText)
    aid_type = Column(UnicodeText)
    aid_type_code = Column(UnicodeText)
    finance_type = Column(UnicodeText)
    finance_type_code = Column(UnicodeText)
    tied_status_code = Column(UnicodeText)
    disbursement_channel_code = Column(UnicodeText)

# Put everything into sectors table, and link back to activity. This will create a new unique sector per activity, which is OK for then importing back into OS but obviously you would probably want an activities_sectors table to handle a relationship between unique activities and unique sectors.
 
class Sector(Base):
    __tablename__ = 'sector'
    id = Column(Integer, primary_key=True)   
    activity_iati_identifier = Column(UnicodeText)
    name = Column(UnicodeText)
    vocabulary = Column(UnicodeText)
    code = Column(UnicodeText)
    percentage = Column(Integer)

class RelatedActivity(Base):
    __tablename__ = 'relatedactivity'
    id = Column(Integer, primary_key=True)
    activity_id = Column(UnicodeText)
    reltext = Column(UnicodeText)
    relref = Column(UnicodeText)
    reltype = Column(UnicodeText)

Base.metadata.create_all()

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
    thisnumber = 0
    # get transactions
    transactions = session.query(Transaction)
    print transactions.count()
    i = 0
    for transaction in transactions:
        # get transaction's activity (should only be 1)
        activities = session.query(Activity).filter(Activity.iati_identifier==transaction.iati_identifier)
        for activity in activities:
            # get parent activity details (should only be 1)
            related_activities = session.query(RelatedActivity).filter(RelatedActivity.activity_id==activity.iati_identifier).filter(RelatedActivity.reltype=='1')
            reladescription = ''
            relatitle = ''
            for related_activity in related_activities:
                # get the related activity's details
                related_activity_details = session.query(Activity).filter(Activity.iati_identifier==related_activity.relref)
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
            sectors = session.query(Sector).filter_by(activity_iati_identifier=activity.iati_identifier)
            # will only write a transaction if it is in a sector!
            for sector in sectors:
                # Sometimes there are multiple sectors, with 100% each. Partly an import error :(
                if ((sector.percentage == 100) and ((sectors.count())>0)):
                    realsectorpercentage = (sector.percentage/sectors.count())
                else:
                    realsectorpercentage = sector.percentage
                thisectorvalue = (((float(realsectorpercentage))/100)*(transaction.value))
            # write to CSV:
                transactiondata = {
                    'transaction_id': transaction.id,
                    'item_value': thisectorvalue,
                    'item_sector': sector.name,
                    'item_sector_code': sector.code,
                    'item_sector_vocabulary': sector.vocabulary,
                    'activity_id': transaction.activity_id,
                    'iati_identifier': transaction.iati_identifier,
                    'value_date': transaction.value_date,
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
        i = i +1
        print i
        # write to CSV every 1000 transactions (there are ~40,000 from DFID and WB)
        if i == 1000:
            # create version number
            thisnumber = thisnumber +1
            # write to CSV
            filename = 'iatidata' + str(thisnumber) + '.csv'
            write_csv(thetransactions, filename)
            # reset counter
            i = 0
            # reset thetransactions
            del thetransactions[:]
            print "That was page " + str(thisnumber)
    # at end of loop, write remaining transactions.
    
    filename = 'iatidata' + str(thisnumber) + '.csv'
    write_csv(thetransactions, filename)
                
def write_csv(transactions, filename):
    fh = open(filename, 'w')
    keys = []
    print transactions
    for transaction in transactions:
        keys.extend(transaction.keys())
    writer = csv.DictWriter(fh, fieldnames=list(set(keys)))
    writer.writerow(dict([(k,k) for k in keys]))
    for transaction in transactions:
        row = dict([(k, unicode(v).encode('utf-8')) for (k, v) in transaction.items() if
            v is not None])
        writer.writerow(row)
    fh.close()
            

if __name__ == '__main__':
    import sys
    thetransactions = []
    run()
