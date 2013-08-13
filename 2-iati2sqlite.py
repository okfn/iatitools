from lxml import etree
from pprint import pprint
import csv
from lib import db
from lib.model import *
from sqlalchemy import *

db.models.metadata.create_all()

from datetime import date, datetime
import os

def nodecpy(out, node, name, attrs={}, convert=unicode):
    if ((node is None) or (node.text is None)):
        return
    if node.text:
        out[name] = convert(node.text)
    for k, v in attrs.items():
    	try:
            out[name + '_' + v] = node.get(k)
        except AttributeError:
            pass

def parse_tx(tx):
    out = {}
    value = tx.find('value')
    if value is not None:
        out['value_date'] = value.get('value-date')
        out['value_currency'] = value.get('currency')
        try:
            out['value'] = float(value.text)
        except TypeError:
            pass
    if tx.findtext('description'):
        out['description'] = tx.findtext('description')
    nodecpy(out, tx.find('activity-type'),
            'transaction_type', {'code': 'code'})
    nodecpy(out, tx.find('transaction-type'),
            'transaction_type', {'code': 'code'})
    nodecpy(out, tx.find('flow-type'),
            'flow_type', {'code': 'code'})
    nodecpy(out, tx.find('finance-type'),
            'finance_type', {'code': 'code'})
    nodecpy(out, tx.find('tied-status'),
            'tied_status', {'code': 'code'})
    nodecpy(out, tx.find('aid-type'),
            'aid_type', {'code':'code'})


    for date in tx.findall('transaction-date'):
        try:
            # for some (WB) projects, the date is not set even though the tag exists...
            if (date is not None):
                temp = {}
                nodecpy(temp, date,
                    'date',
                    {'iso-date': 'iso-date'})

                date_iso_date = date.get('iso-date')

                if (date_iso_date):
                    d = (date_iso_date)
                    out['transaction_date_iso'] = d
                elif (temp.has_key('date')):
                    d = (temp['date'])
                    out['transaction_date_iso'] = d

            else:
                print "No date!!"
           
        except ValueError:
            pass

    if not (out.has_key('transaction_date_iso')):
        out['transaction_date_iso'] = out['value_date']
    nodecpy(out, tx.find('disembursement-channel'),
            'disembursement_channel', {'code': 'code'})
    nodecpy(out, tx.find('provider-org'),
            'provider_org', {'ref': 'ref'})
    nodecpy(out, tx.find('receiver-org'),
            'receiver_org', {'ref': 'ref'})
    return out

def get_date(out, node, name, key):
    de = node.find('activity-date[@type="%s"]' % name)
    if de is not None:
        out[key] = de.get('iso-date')

def parse_activity(activity, out, package_filename):
    out['default_currency'] = activity.get("default-currency")
    nodecpy(out, activity.find('reporting-org'),
            'reporting_org', {'ref': 'ref', 
                              'type': 'type'})
    out['iati_identifier'] = activity.findtext('iati-identifier')
    if activity.findtext('activity-website'):
        out['activity_website'] = activity.findtext('activity-website')
    out['title'] = activity.findtext('title')
    if activity.findtext('description'):
        out['description'] = activity.findtext('description')
    if activity.findtext('recipient-region'):
        out['recipient_region'] = activity.findtext('recipient-region')
        out['recipient_region_code'] = activity.find('recipient-region').get('code')
    nodecpy(out, activity.find('recipient-country'),
            'recipient_country', {'code': 'code'})
    nodecpy(out, activity.find('collaboration_type'),
            'collaboration_type', {'code': 'code'})
    nodecpy(out, activity.find('default-flow-type'),
            'flow_type', {'code': 'code'})
    nodecpy(out, activity.find('default-finance-type'),
            'finance_type', {'code': 'code'})
    nodecpy(out, activity.find('default-tied-status'),
            'tied_status', {'code': 'code'})
    nodecpy(out, activity.find('default-aid-type'),
            'aid_type', {'code':'code'})
    nodecpy(out, activity.find('activity-status'),
            'status', {'code':'code'})
    out['status_code'] = activity.find('activity-status').get('code')
    nodecpy(out, activity.find('legacy-data'),
            'legacy', {'name': 'name', 'value': 'value'})
    
    nodecpy(out, activity.find('participating-org[@role="Funding"]'),
            'funding_org', {'ref': 'ref', 'type': 'type'})
    nodecpy(out, activity.find('participating-org[@role="Extending"]'),
            'extending_org', {'ref': 'ref', 'type': 'type'})
    nodecpy(out, activity.find('participating-org[@role="Implementing"]'),
            'implementing_org', {'ref': 'ref', 'type': 'type'})
    nodecpy(out, activity.find('participating-org[@role="funding"]'),
            'funding_org', {'ref': 'ref', 'type': 'type'})
    nodecpy(out, activity.find('participating-org[@role="extending"]'),
            'extending_org', {'ref': 'ref', 'type': 'type'})
    nodecpy(out, activity.find('participating-org[@role="implementing"]'),
            'implementing_org', {'ref': 'ref', 'type': 'type'})
    try:
        if (activity.find('reporting-org').get('ref')=='SE-6'):
            out['implementing_org'] = activity.find('participating-org[@role="Accountable"]').get('ref')
            out['implementing_org_ref'] = activity.find('participating-org[@role="Accountable"]').get('ref')
    except:
        pass
    for date in activity.findall('activity-date'):
        try:
            # for some (WB) projects, the date is not set even though the tag exists...
            if (date is not None):
                temp = {}
                nodecpy(temp, date,
                    'date',
                    {'type': 'type', 'iso-date': 'iso-date'})
                 
                date_type = date.get('type')
                date_iso_date = date.get('iso-date')
                # Sometimes the date is placed in the @iso-date attribute
                # Sometimes (DFID only?) the date is placed in the text
                # Sometimes the date tag is opened but then empty.
                if (date_type == 'start-actual'):
                    if (date_iso_date is not None):
                        d = (date_iso_date)
                        out['date_start_actual'] = d
                    elif (temp.has_key('date')):
                        d = (temp['date'])
                        out['date_start_actual'] = d
                if (date_type == 'start-planned'):
                    if (date_iso_date is not None):
                        d = (date_iso_date)
                        out['date_start_planned'] = d
                    elif (temp.has_key('date')):
                        d = (temp['date'])
                        out['date_start_planned'] = d
                
                if (date_type == 'end-actual'):
                    if (date_iso_date is not None):
                        d = (date_iso_date)
                        out['date_end_actual'] = d
                
                    elif (temp.has_key('date')):
                        d = (temp['date'])
                        out['date_end_actual'] = d
                
                if (date_type == 'end-planned'):
                    if (date_iso_date is not None):
                        d = (date_iso_date)
                        out['date_end_planned'] = d
                    elif (temp.has_key('date')):
                        d = (temp['date'])
                        out['date_end_planned'] = d
            else:
                print "No date!!"
           
        except ValueError:
            pass
    nodecpy(out, activity.find('contact-info/organisation'),
            'contact_organisation', {})
    nodecpy(out, activity.find('contact-info/mailing-address'),
            'contact_mailing_address', {})
    nodecpy(out, activity.find('contact-info/telephone'),
            'contact_telephone', {})
    nodecpy(out, activity.find('contact-info/email'),
            'contact_email', {})
    
    for sector in activity.findall('sector'):
        try:
            temp = {}
            nodecpy(temp, sector,
                'sector',
                {'vocabulary': 'vocabulary', 'percentage': 'percentage', 'code': 'code'})
            try: 
                vocab = temp['sector_vocabulary'] if temp['sector_vocabulary'] else 'DAC'
            except:
                try:
                    vocab = sector.get('vocabulary')
                except:
                    vocab = 'DAC'
            activityiatiid = activity.findtext('iati-identifier')
            try:
                getpercentage = temp['sector_percentage']
                percentage = 0
                # if getpercentage doesn't exist, or it's blank, or it's None, do this:
                if (not(getpercentage) or (getpercentage == '') or (getpercentage is None)):
                    percentage = 100
                else:
                # if getpercentage exists, it's not blank, and it's not none
                    percentage = getpercentage            
            except:
                try:
                    percentage = sector.get('percentage')
                except:
                    percentage = 100
            if (percentage == None):
                percentage = 100
            try:
                temp['sector']
            except:
                temp['sector'] = ''
            try:
                temp['sector_code']
            except:
                try:
                    temp['sector_code'] = sector.get('code')
                except:
                    temp['sector_code'] = ''
            tsector = {
                'activity_iati_identifier': activityiatiid,
                'name': temp['sector'],
                'code': temp['sector_code'],
                'percentage': int(percentage),
                'vocabulary': vocab
            }
            missingfields(sector, Sector, package_filename)
            s = Sector(**tsector)
            db.session.add(s)
        except ValueError:
            pass
            
    for ra in activity.findall('related-activity'):
        try:
            activityiatiid = activity.findtext('iati-identifier')
            related_activity = {
                'activity_id': activityiatiid,
                'relref': ra.get('ref'),
                'reltype': ra.get('type')                    
                }
            missingfields(related_activity, RelatedActivity, package_filename)
            rela = RelatedActivity(**related_activity)
            db.session.add(rela)
        except ValueError:
            pass
             
    for tx in activity.findall("transaction"):
        transaction = parse_tx(tx)
        transaction['iati_identifier'] = out['iati_identifier']
        missingfields(transaction, Transaction, package_filename)
        t = Transaction(**transaction)
        db.session.add(t)
    missingfields(out, Activity, package_filename)
    x = Activity(**out) 
    db.session.add(x)
    return (out)

def missingfields(dict_, obj, package):
    missing = [ k for k in dict_ if k not in obj.__table__.c.keys() ]
    if missing:
        logtext = "Missing fields in package " + package + ": " + str(obj.__name__) + " " + str(missing) + "\n"
        log(logtext)
    for m in missing:
        del dict_[m]

def log(logtext):
    inp=file('log-' + str(date.today()) + '.txt', 'a')
    inp.write(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " " + logtext)
    inp.close()

def load_file(file_name, context=None):
    doc = etree.parse(file_name)
    if context is None:
        context = {}
    context['source_file'] = file_name
    print "Parsing ", file_name
    for activity in doc.findall("iati-activity"):
        out = parse_activity(activity, context.copy(), file_name)
    print "Writing to database..."
    db.session.commit()
    print "Written to database."

def load_package():
    if (len(sys.argv) > 1):
        packagedir = sys.argv[1]
    else:
        packagedir = 'packages/'+str(date.today())
        print "No package folder defined (you can supply the argument YYYY-MM-DD for a particular date of packages), so using today's date\n"
        logtext = "No package folder defined, so reverting to today's date\n"
        log(logtext)
    
    path = packagedir
    listing = os.listdir(path)
    totalfiles = len(listing)
    print "Found", totalfiles, "files."
    filecount = 1
    for infile in listing:
        try:            
            print ""
            print "Loading file", filecount, "of", totalfiles, "(", round(((float(filecount)/float(totalfiles))*100),2), "%)"
            filecount = filecount +1
            load_file(path + '/' + infile)
        except Exception, e:
            print 'Failed:', e
            logtext = "Error in file: " + infile + " - " + str(e) + "\n"
            log(logtext)
	    pass

if __name__ == '__main__':
    import sys
    try:
        load_package()
    except Exception, e:
        print 'Failed:', e
        logtext = "Couldn't load package: " + str(e) + "\n"
        log(logtext)
    print db.session.query(Activity).count()
    print db.session.query(Transaction).count()
