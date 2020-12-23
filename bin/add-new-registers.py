#!/usr/bin/env python3

import csv
import requests
from datetime import datetime, date
from digital_land.register import hash_value
from digital_land.collection import Collection

# Digital Land Google Sheet with new registers ..

sheet="brownfield-land"
key="1e1UUs34KITLANgJGGHNV1Hh_UzkKU_7ROApzOdzhGAU"
CSV_URL='https://docs.google.com/spreadsheets/d/%s/gviz/tq?tqx=out:csv&sheet={%s}' % (key, sheet)


def entry_date(entry, field):
    value = entry.get(field, "")
    if value:
        # wrong for a timestamp ..
        value = datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
    return value


def does_entry_exist(register, entry):
    return entry["endpoint"] in register.records and \
           any(row == entry for row in register.records[entry["endpoint"]])


session = requests.Session()
download = session.get(CSV_URL)
content = download.content.decode('utf-8')

collection = Collection()
collection.load()

for entry in csv.DictReader(content.splitlines()):

    if entry["collection"] != sheet:
        continue

    endpoint_hash = hash_value(entry["endpoint-url"])
    entry["endpoint"] = endpoint_hash
    endpoint_entry = {
            "endpoint": entry["endpoint"],
            "endpoint-url": entry["endpoint-url"],
            "plugin": entry.get("plugin", ""),
            "parameters": entry.get("parameters", ""),
            "entry-date": entry_date(entry, "entry-date"),
            "start-date": entry_date(entry, "start-date"),
            "end-date": entry_date(entry, "end-date"),
        }

    source_entry = {
        "endpoint": entry["endpoint"],
        "collection": entry["collection"],
        "pipelines": entry.get("pipelines", entry["collection"]),
        "organisation": entry.get("organisation", ""),
        "documentation-url": entry.get("documentation-url", ""),
        "licence": entry.get("licence", ""),
        "attribution": entry.get("attribution", ""),
        "entry-date": entry_date(entry, "entry-date"),
        "start-date": entry_date(entry, "start-date"),
        "end-date": entry_date(entry, "end-date"),
    }

    if not does_entry_exist(collection.endpoint, endpoint_entry):
        collection.endpoint.add_entry(endpoint_entry)

    if not does_entry_exist(collection.source, source_entry):
        collection.source.add_entry(source_entry)

collection.save_csv()
