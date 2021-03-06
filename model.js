{
  "dataset": {
    "model_rev": 1,
    "name": "iati",
    "label": "IATI Registry Transactions", 
    "description": "Transactional records from IATI activity files currently listed on IATI Registry.",
    "currency": "EUR",
    "temporal_granularity": "year"
  },
  "mapping": {
    "amount": {
      "type": "value",
      "label": "Amount",
      "description": "",
      "column": "amount",
      "datatype": "float"
    },
    "time": {
      "type": "value",
      "label": "Year",
      "description": "",
      "column": "transaction_date_iso",
      "datatype": "date"
    },
    "from": {
      "label": "Funding Organisation",
      "type": "entity",
      "facet": true,
      "description": "",
      "fields": [
        {"column": "activity_extending_org", "name": "label", "datatype": "string"},
        {"column": "activity_extending_org_type", "name": "type", "datatype": "string"},
        {"column": "activity_extending_org_ref", "name": "ref", "datatype": "string"},
        {"constant": "org", "name": "iati_role", "datatype": "constant"},
        {"constant": "yes", "name": "iati_funding", "datatype": "constant"}
      ]
    },
    "to": {
      "label": "Implementing Organisation",
      "type": "entity",
      "facet": true,
      "description": "",
      "fields": [
        {"column": "activity_implementing_org", "name": "label", "datatype": "string"},
        {"column": "activity_implementing_org_ref", "name": "ref", "datatype": "string"},
        {"column": "activity_implementing_org_type", "name": "type", "datatype": "string"},
        {"constant": "org", "name": "iati_role", "datatype": "constant"},
        {"constant": "yes", "name": "iati_implementing", "datatype": "constant"}
      ]
    },
    "actual_start_date": {
      "type": "value",
      "label": "Actual Start Date",
      "description": "",
      "column": "date_start_actual",
      "datatype": "date"
    },
    "planned_start_date": {
      "type": "value",
      "label": "Planned Start Date",
      "description": "",
      "column": "date_start_planned",
      "datatype": "date"
    },
    "actual_end_date": {
      "type": "value",
      "label": "Actual End Date",
      "description": "",
      "column": "date_end_actual",
      "datatype": "date"
    },
    "planned_end_date": {
      "type": "value",
      "label": "Planned End Date",
      "description": "",
      "column": "date_end_planned",
      "datatype": "date"
    },
    "recipient_region": {
      "label": "Recipient Region",
      "type": "classifier",
      "taxonomy": "iati-region",
      "description": "",
      "facet": true,
      "fields": [
        {"column": "activity_recipient_region", "name": "label", "datatype": "string"}
        {"column": "activity_recipient_country_code", "name": "code", "datatype": "string"}
      ]
    },
    "recipient_country": {
      "label": "Recipient Country",
      "type": "classifier",
      "taxonomy": "iati-country",
      "description": "",
      "facet": true,
      "fields": [
        {"column": "activity_recipient_country", "name": "label", "datatype": "string"}
      ]
    },
    "aid_type": {
      "label": "Aid Type",
      "type": "classifier",
      "taxonomy": "iati-aid-type",
      "description": "",
      "facet": true,
      "fields": [
        {"column": "aid_type", "name": "label", "datatype": "string"}
      ]
    },
    "finance_type": {
      "label": "Finance Type",
      "type": "classifier",
      "taxonomy": "iati-finance-type",
      "description": "",
      "fields": [
        {"column": "finance_type", "name": "label", "datatype": "string"},
        {"column": "finance_type_code", "name": "code", "datatype": "string"},
        {"constant": "finance-type", "name": "iati_function", "datatype": "string"}
      ]
    },
    "transaction_type": {
      "label": "Transaction Type",
      "type": "classifier",
      "taxonomy": "iati-tx-type",
      "description": "",
      "fields": [
        {"column": "transaction_type", "name": "label", "datatype": "string"},
        {"column": "transaction_type_code", "name": "code", "datatype": "string"},
        {"constant": "transaction-type", "name": "iati_function", "datatype": "string"}
      ]
    },
    "flow_type": {
      "label": "Flow Type",
      "type": "classifier",
      "taxonomy": "iati-flow-type",
      "description": "",
      "fields": [
        {"column": "flow_type", "name": "label", "datatype": "string"},
        {"column": "flow_type_code", "name": "code", "datatype": "string"},
        {"constant": "flow-type", "name": "iati_function", "datatype": "constant"}
      ]
    },
    "identifier": {
      "type": "value",
      "label": "IATI Identifier",
      "description": "",
      "column": "iati_identifier",
      "datatype": "string"
    },
    "title": {
      "type": "value",
      "label": "Title",
      "description": "",
      "column": "title",
      "datatype": "string"
    },
    "description": {
      "type": "value",
      "label": "Description",
      "description": "",
      "column": "description",
      "datatype": "string"
    },
    "status": {
      "type": "value",
      "label": "Status",
      "description": "",
      "column": "status",
      "datatype": "string"
    },
    "source_file": {
      "type": "value",
      "label": "Source File",
      "description": "URL of the registry entry",
      "column": "source_file",
      "datatype": "string"
    },
    "activity_website": {
      "type": "value",
      "label": "Activity website",
      "description": "URL of the activity",
      "column": "activity_website",
      "datatype": "string"
    },
    "tied_status": {
      "type": "value",
      "label": "Tied Status",
      "description": "",
      "column": "tied_status",
      "datatype": "string"
    }
  },
  "views": [
    {
      "entity": "dataset",
      "label": "Aid Type",
      "name": "default",
      "dimension": "dataset",
      "breakdown": "aid_type",
      "filters": {"name": "iati"}
    },
    {
      "entity": "dataset",
      "label": "Recipient Region",
      "name": "region",
      "dimension": "dataset",
      "breakdown": "recipient_region",
      "filters": {"name": "iati"}
    },
    {
      "entity": "classifier",
      "label": "Aid Type",
      "name": "default",
      "dimension": "recipient_region",
      "breakdown": "aid_type",
      "filters": {"taxonomy": "iati-region"}
    },
    {
      "entity": "classifier",
      "label": "Recipient Region",
      "name": "default",
      "dimension": "aid_type",
      "breakdown": "recipient_region",
      "filters": {"taxonomy": "iati-aid-type"}
    },
    {
      "entity": "classifier",
      "label": "Implementing Organization",
      "name": "implementing",
      "dimension": "recipient_region",
      "breakdown": "to",
      "filters": {"iati_role": "org"}
    },
    {
      "entity": "entity",
      "label": "Aid Type",
      "name": "default",
      "dimension": "to",
      "breakdown": "aid_type",
      "filters": {"iati_implementing": "yes"}
    },
    {
      "entity": "entity",
      "label": "Funding Organization",
      "name": "funding",
      "dimension": "to",
      "breakdown": "from",
      "filters": {"iati_implementing": "yes"}
    },
    {
      "entity": "entity",
      "label": "Transaction Type",
      "name": "txtype",
      "dimension": "to",
      "breakdown": "transaction_type",
      "filters": {"iati_implementing": "yes"}
    },
    {
      "entity": "entity",
      "label": "Aid Type",
      "name": "default",
      "dimension": "from",
      "breakdown": "aid_type",
      "filters": {"iati_funding": "yes"}
    },
    {
      "entity": "entity",
      "label": "Funded Organizations",
      "name": "funded",
      "dimension": "from",
      "breakdown": "from",
      "filters": {"iati_funding": "yes"}
    }
  ]
}
