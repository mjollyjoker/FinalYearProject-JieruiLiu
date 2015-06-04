# This method takes will crawl census data from government website
# Regex is used for match each of the attribute
# result information will then be stored to a csv file

import urllib.request
import re

# initializing regex expresstion for attributes
regexPopulation = re.compile(r"Census,\sthere\swere\s(.+)\speople\sin")
regexAge = re.compile(r"Areas\)\swas\s(.+)\syears\.")
regexUnemploy = re.compile(r"and\s(.+)\%\swere\sunemployed")
regexIncome = re.compile(r" Areas\)\swas\s\$(.+)\.")
regexPrimary = re.compile(r"Of\sthese,\s(.+)\%\swere\sin\sprimary")
regexSecondary = re.compile(r"primary\sschool,\s(.+)\%\sin\ssecondary")
regexTertiary = re.compile(r"secondary\sschool\sand\s(.+)\%\sin\sa\stertiary")

# read postcode information
hostfile = open("tempPost.txt","r", encoding="utf-8")
# output destination file
outputResult = open('censusData.csv','ab')
# information will be crawled according to postcode
for pCode in hostfile:
    urlString = "http://www.censusdata.abs.gov.au/census_services/getproduct/census/2011/quickstat/POA" + pCode[:-1] + "?opendocument&navpos=220"
    page = urllib.request.urlopen(urlString)
    pageString = page.read().decode("utf-8")
    try:
        population = regexPopulation.findall(pageString)[0].replace(",","")
    except IndexError:
        population = 'null'
    try:
        age = regexAge.findall(pageString)[0]
    except IndexError:
        age = 'null'
    try:
        unemploy = regexUnemploy.findall(pageString)[0].replace(",","")
    except IndexError:
        unemploy = 'null'
    try:
        income = regexIncome.findall(pageString)[0].replace(",","")
    except IndexError:
        income = 'null'
    try:
        primary = regexPrimary.findall(pageString)[0].replace(",","")
    except IndexError:
        primary = 'null'
    try:
        secondary = regexSecondary.findall(pageString)[0].replace(",","")
    except IndexError:
        secondary = 'null'
    try:
        tertiary = regexTertiary.findall(pageString)[0].replace(",","")
    except IndexError:
        tertiary = 'null'
    outString = population+","+age+","+unemploy+","+income+","+primary+","+secondary+","+tertiary+"\n"
    print (outString)
    outputResult.write(bytes(outString, 'UTF-8'))
