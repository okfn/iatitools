from lxml import etree
from pprint import pprint
import csv

def nodecpy(out, node, name, attrs={}, convert=unicode):
    if node is None:
        return
    if node.text:
        out[name] = convert(node.text)
    for k, v in attrs.items():
        out[name + '_' + v] = node.get(k)

def parse_tx(tx, out):
    value = tx.find('value')
    if value is not None:
        out['date'] = value.get('value-date')
        out['value'] = float(value.text)
    nodecpy(out, tx.find('activity-type'),
            'transaction_type', {'code': 'code'})
    nodecpy(out, tx.find('transaction-type'),
            'transaction_type', {'code': 'code'})
    get_date(out, tx, 'transaction-date', 'date')
    if tx.findtext('transaction-date'):
        out['date_comment'] = tx.findtext('transaction-date')
    nodecpy(out, tx.find('disembursement-channel'),
            'disembursement_channel', {'code': 'code'})
    nodecpy(out, tx.find('provider-org'),
            'provider_org', {'ref': 'ref'})
    nodecpy(out, tx.find('receiver-org'),
            'receiver_org', {'ref': 'ref'})
    return out

def get_date(out, node, name, key):
    de = node.find('activity-date[type="%s"]' % name)
    if de is not None:
        out[key] = de.get('iso-date')

def parse_activity(activity, out):
    nodecpy(out, activity.find('reporting-org'),
            'reporting_org', {'ref': 'ref', 
                              'type': 'type'})
    
    out['identifier'] = activity.findtext('iati-identifier')
    if activity.findtext('activity-website'):
        out['website'] = activity.findtext('activity-website')
    out['title'] = activity.findtext('title')
    if activity.findtext('description'):
        out['description'] = activity.findtext('description')
    if activity.findtext('recipient-region'):
        out['recipient_region'] = activity.findtext('recipient-region')
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
            'aid_type', {})
    nodecpy(out, activity.find('activity-status'),
            'status', {})
    nodecpy(out, activity.find('legacy-data'),
            'legacy', {'name': 'name', 'value': 'value'})
    
    nodecpy(out, activity.find('participating-org[@role="Funding"]'),
            'funding_org', {'ref': 'ref', 'type': 'type'})
    nodecpy(out, activity.find('participating-org[@role="Extending"]'),
            'extending_org', {'ref': 'ref', 'type': 'type'})
    nodecpy(out, activity.find('participating-org[@role="Implementing"]'),
            'implementing_org', {'ref': 'ref', 'type': 'type'})
    
    get_date(out, activity, 'start-planned', 'start_planned')
    get_date(out, activity, 'start-actual', 'start_actual')
    get_date(out, activity, 'end-planned', 'end_planned')
    get_date(out, activity, 'end-actual', 'end_actual')
    
    nodecpy(out, activity.find('contact-info/organisation'),
            'contact_org', {})
    nodecpy(out, activity.find('contact-info/mailing-address'),
            'contact_address', {})
    nodecpy(out, activity.find('contact-info/telephone'),
            'contact_telephone', {})
    nodecpy(out, activity.find('contact-info/email'),
            'contact_email', {})
    
    # SLIGHTLY HACKY:
    for policy_marker in activity.findall('policy-marker'):
        nodecpy(out, policy_marker,
                'policy_marker_' + policy_marker.get('code'), 
                {'vocabulary': 'vocabulary', 'significance': 'significance'})

    transactions = []
    for tx in activity.findall("transaction"):
        transactions.append(parse_tx(tx, out.copy()))
    return transactions

def load_file(file_name, context=None):
    doc = etree.parse(file_name)
    if context is None:
        context = {}
    context['source_file'] = file_name
    transactions = []
    for activity in doc.findall("iati-activity"):
        transactions.extend(parse_activity(activity, context.copy()))
    return transactions

def load_registry(url='http://iatiregistry.org/api'):
    import ckanclient
    transactions = []
    registry = ckanclient.CkanClient(base_location=url)
    for pkg_name in registry.package_register_get():
        pkg = registry.package_entity_get(pkg_name)
        for resource in pkg.get('resources', []):
            print resource.get('url')
            transactions.extend(
                load_file(resource.get('url'),
                {'registry_package': pkg_name})
                )
    return transactions

def write_csv(transactions, filename='iati.csv'):
    fh = open(filename, 'w')
    keys = []
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
    #transactions = load_file(sys.argv[1])
    transactions = load_registry()
    write_csv(transactions)
    pprint(transactions)
