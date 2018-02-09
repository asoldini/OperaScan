import sys
import csv
from pypdf2xml import pdf2xml
from bs4 import BeautifulSoup


if len(sys.argv) != 2:
    print """usage:
to see the output:
\tpdf2xml file.pdf
to write output to file:
\tpdf2xml file.pdf > outfile.xml
"""
else:
    docinfo = pdf2xml(open(sys.argv[1],'rb'))

soup = BeautifulSoup(docinfo, "lxml")

arr = []

for page in soup.find_all(width="612", height="792"):
	dic = {}
	name = page.find(top="182", left="72")
	dic["Name"] = name.get_text()
	amount = page.find(top="74", left="394")
	dic["Amount"] = amount.get_text()
	deg = page.find(top="182", left="394")
	dic["Degrees"] = deg.get_text()
	address1 = page.find(top="219", left="176")	
	if address1:
		address_1 = address1.get_text()
	else:
		address_1 = " "
	address2 = page.find(left="176", top="231")
	if address2:
		address_2 = address2.get_text()
	else:
		address_2 = " "
	address3 = page.find(left="176", top="243")
	if address3:
		address_3 = address3.get_text()
	else:
		address_3 = " "
	address4 = page.find(left="176", top="255")
	if address4:
		address_4 = address4.get_text()
	else:
		address_4 = " "
	dic["Address"] = address_1 + " " + address_2 + " " + address_3 + " " + address_4
	typ = page.find(top="296", left="420")
	dic["Type"] = typ.get_text()
	date = page.find(left="132", top="374")
	dic["Date"] = date.get_text()
	cred = page.find(left="132", top="568")
	dic["Credit Amount"] = cred.get_text()
	arr.append(dic)

keys = arr[0].keys()
with open('list.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(arr)
