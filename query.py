#!/bin/python3

import csv
#import socket

def find_ips_and_ns_for_domain(domain):
    ips = []
    ns = []
    with open('recs.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['domain'] == domain:
                ips.append(row['ip'])
                ns.append(row['ns'])
    print("Finding all IPs and nameservers for domain:", domain)
    print("IPs:", ips)
    print("Nameservers:", ns)

def get_domains_and_ns_for_ip(ip):
    domains = []
    ns = []
    with open('recs.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['ip'] == ip:
                domains.append(row['domain'])
                ns.append(row['ns'])
    print("Finding all domains and nameservers for IP:", ip)
    print("Domains:", domains)
    print("Nameservers:", ns)

def get_domains_for_ns(ns):
    domains = []
    with open('recs.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['ns'] == ns:
                domains.append(row['domain'])
    print("Finding all domains and nameservers for IP:", ns)
    print("Domains:", domains)

def get_ns_no_ip():
    ns = []
    with open('recs.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['is_ns'] == 1 or row['is_ns'] == "1":
                if row['ip'] == "" or row['ip'] == None:
                    domains.append(row['domain'])
    print("Finding NSs without IPs")
    print("NS:", ns)

find_ips_and_ns_for_domain("example.com")

get_domains_and_ns_for_ip("71.19.154.14")

get_domains_for_ns("ns2.example.org")

get_ns_no_ip()
