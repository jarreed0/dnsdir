#!/bin/python3

# domain, ip, cnames, registrar, issued, expires, ns, server, rectime, is_ns

from bs4 import BeautifulSoup
import csv
import datetime
import pydig
import requests
import signal
import socket
import urllib.parse
import whois

domain = "thechamps.co"

fetched = []

class TimeoutException(Exception): pass

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

def signal_handler(signum, frame):
    raise Exception("Timed out!")

def get_source(ip):
    r = requests.get("http://" + ip)
    text = r.text.lower()
    type = "unknown"
    if "nginx" in text:
     type = "nginx"
    elif "apache" in text:
     type = "apache"
    elif "azure" in text:
     type = "azure"
    return [r.status_code, type]

def get_source_clock(ip):
 signal.signal(signal.SIGALRM, signal_handler)
 signal.alarm(2)
 try:
  return get_source(ip)
 except (Exception):
  return ['NA', "unknown"]

def pull(domain, is_ns):
 print(domain)
 global fetched
 if domain in fetched:
  return None
 fetched.append(domain)

 who = whois.whois(domain)

 if domain != strip(domain):
  pull_clock(strip(domain), 0)

 ns = pydig.query(domain, 'NS')
 for n in ns:
  pull_clock(n, 1)

 cnames = pydig.query(domain, 'CNAME')
 for cname in cnames:
  pull_clock(cname, 0)

 ips = pydig.query(domain, 'A')
 server = []
 for ip in ips:
  server.append(get_source_clock(ip))

 # domain, ip, cnames, registrar, issued, expires, ns, rectime, is_ns
 data = [
  domain,
  ips,
  cnames,
  who.registrar,
  who.creation_date,
  who.expiration_data,
  ns,
  server,
  get_current_datetime(),
  is_ns
 ]

 print(data)
 update_recs(data)
 # return data

def pull_clock(domain, is_ns):
 signal.signal(signal.SIGALRM, signal_handler)
 signal.alarm(10)   # Ten seconds
 try:
  return pull(domain, is_ns)
 except (Exception):
  print("Timed out!")

def get_domain_names(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = [link.get('href') for link in soup.find_all('a')]
    domain_names = []
    domain_names = [*set(domain_names)]
    for u in urls:
        parsed_url = urllib.parse.urlparse(u)
        domain_names.append(parsed_url.netloc)
    return domain_names

def pull_from_url(url):
    if url == "" or url == None:
        exit()
    if "http" not in url:
        domains = get_domain_names("http://"+url)
    else:
        domains = get_domain_names(url)
    #domains = get_domain_names(url)
    domains = [*set(domains)]
    for domain in domains:
        #print(domain)
        if domain != None and domain != '' and type(domain) == str:
            if "http" not in domain:
                get_domain_names("http://"+domain)
            else:
                get_domain_names(domain)
            pull_clock(domain, 0)

# print(pull(domain))
load_recs()

pull_clock(domain, 0)
pull_clock("shadergrounds.com", 0)
pull_clock("reedmedia.net", 0)
pull_clock("indiecapsule.com", 0)
pull_clock("example.com", 0)
pull_clock("ns.freedomdns.net", 1)
pull_clock("ns2.example.org", 1)

pull_from_url("http://tornadovps.com")
pull_from_url("http://sharktech.net")

pull_from_url("http://reedmedia.net")
pull_from_url("http://godotbites.com")
pull_from_url("http://raylib.com") # uncomment me for a larger pull
pull_from_url("https://thechamps.co")
pull_from_url("https://github.com")
pull_from_url("https://youtube.com")
pull_from_url("https://reddit.com")
pull_from_url("https://facebook.com")
pull_from_url("https://tiktok.com")
pull_from_url("https://instagram.com")
pull_from_url("https://twitter.com")
pull_from_url("https://yahoo.com")
pull_from_url("https://hacker101.com")
pull_from_url("https://hackerone.com")
pull_from_url("http://ylimaf.com")
pull_from_url("http://linkly.ink")
pull_from_url("http://campsitelist.com/")
pull_from_url("http://wholesaletexastires.com")

with open('top-1m.csv', 'r') as read_obj:
    csv_reader = csv.reader(read_obj)
    for row in csv_reader:
        pull_from_url(row[1])

