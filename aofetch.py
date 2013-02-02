#! /usr/bin/python
import sys
import base64
import suds
from xml.dom import minidom

def get_image(session, base, path):
    url = "http://ao.sa.dk/LAView/ImageServer/Service1.asmx?WSDL"
    client = suds.client.Client(url)
    response = client.service.getImage2(session, base + path)
    print ("Error Code: " + response.errorCode +
           "Network Load: " + str(response.networkLoad))
    if response.errorCode == "Ok":
        image64 = response.imageData
        image = base64.standard_b64decode(image64)
        filename = 'img/' + ( base + path ).replace("/", ".")
        file = open(filename, "wb")
        file.write(image)
        print ("Writing to file " + filename)
        file.close()

xmldoc = minidom.parse(sys.argv[1])

properties = xmldoc.firstChild.getElementsByTagName("property")

images = properties.item(1).getAttribute('value').split(",")

prefix = properties.item(0).getAttribute('value').lstrip("/")

session = properties.item(2).getAttribute('value')

for image in images:
    if image:
        get_image(session, prefix, image)
