import dns.resolver
import time
import requests
import csv
from datetime import datetime

class DNSLookup:
    def __init__(self, domain):
        self.domain = domain
        self.resolver = dns.resolver.Resolver()

    def get_records(self, record_type):
        try:
            answers = self.resolver.resolve(self.domain, record_type)
            return [str(rdata) for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout) as e:
            print(f"No {record_type} records found for {self.domain}: {e}")
            return []

    def retrieve_records(self, record_types):
        records = {}
        for record_type in record_types:
            records[record_type] = self.get_records(record_type)
        return records

domain = "lucwidmer.ch"
record_types = ["A", "NS"]

while True:
    dns_lookup = DNSLookup(domain)
    records = dns_lookup.retrieve_records(record_types)
    
    r = requests.get('https://lucwidmer.ch/')
    
    with open("server.csv", mode='a', newline='') as csvfile:
        fieldnames = ['IPv4', 'NameServer', "WebsiteStatus", 'Timestamp'] 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header only if the file is empty
        csvfile.seek(0, 2)
        if csvfile.tell() == 0:
            writer.writeheader()
        
        row = {
            "IPv4": ", ".join(records["A"]),
            "NameServer": ", ".join(records["NS"]),
            "WebsiteStatus": r.status_code,
            "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        writer.writerow(row)

    time.sleep(60*3)
