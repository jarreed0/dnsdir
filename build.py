#!/bin/python3

# domain,cname,registrar,issued,expires,ip,ns,rectime,is_ns

from bs4 import BeautifulSoup
import csv
import datetime
import pydig
import requests
import socket
import urllib.parse
import whois

domain = "thechamps.co"

fetched = []

def update_recs(data):
    with open("recs.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def load_recs():
    global fetched
    with open('recs.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            fetched.append(row['domain'])

def get_current_datetime():
    return str(datetime.datetime.now())

def strip(subdomain):
 return ".".join(subdomain.split(".")[-2:])

def pull(domain, is_ns):
 global fetched
 if domain in fetched:
  return None
 fetched.append(domain)

 who = whois.whois(domain)

 if domain != strip(domain):
  pull(strip(domain), 0)

 ns = pydig.query(domain, 'NS')
 for n in ns:
  pull(n, 1)

 data = [
  domain,
  pydig.query(domain, 'A'),
  pydig.query(domain, 'CNAME'),
  who.registrar,
  who.creation_date,
  who.expiration_data,
  pydig.query(domain, 'A'),
  ns,
  get_current_datetime(),
  is_ns
 ]
 print(data)
 update_recs(data)
 # return data

def get_domain_names(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = [link.get('href') for link in soup.find_all('a')]
    domain_names = []
    for u in urls:
        parsed_url = urllib.parse.urlparse(u)
        domain_names.append(parsed_url.netloc)
    return domain_names

def pull_from_url(url):
    domains = get_domain_names(url)
    for domain in domains:
        if domain != None and domain != '':
            if "http" not in domain:
                get_domain_names("http://"+domain)
            else:
                get_domain_names(domain)
            pull(domain, 0)

# print(pull(domain))
load_recs()

pull(domain, 0)
pull("shadergrounds.com", 0)
pull("reedmedia.net", 0)
pull("indiecapsule.com", 0)
pull("example.com", 0)
pull("ns.freedomdns.net", 1)
pull("ns2.example.org", 1)

pull_from_url("http://reedmedia.net")
pull_from_url("http://godotbites.com")
# pull_from_url("http://raylib.com") # uncomment me for a larger pull
