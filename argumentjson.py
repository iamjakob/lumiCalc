#!/usr/bin/env python

from optparse import OptionParser
from xml.dom.minidom import parseString

parser = OptionParser()

(options, args) = parser.parse_args()

jobNumbers = []

totalJobs = int(float(args[0])) + 1
source = file(args[1])


for x in range(1,totalJobs):
    jobNumbers.append(str(x))

#print jobNumbers

xmlStr = source.read()

source.close()

lumilist = dict()

dom = parseString(xmlStr)

jobTags = dom.getElementsByTagName('Job')

for tag in jobTags:
    process = False
    for i in range(tag.attributes.length):
        attr = tag.attributes.item(i)
        if attr.name == 'JobID' and attr.value in jobNumbers:
            process = True
            jobNumbers.remove(attr.value)
        elif attr.name == 'Lumis':
            xmlLumis = attr.value

    if not process:
        continue

    runLumiBlocks = xmlLumis.split(',')
        
    for block in runLumiBlocks:
        if '-' in block:
            ends = block.partition('-')
            run = ends[0].partition(':')[0]
            begin = int(ends[0].partition(':')[2])
            end = int(ends[2].partition(':')[2]) + 1
        else:
            run = block.partition(':')[0]
            begin = int(block.partition(':')[2])
            end = begin + 1

        if run not in lumilist:
            lumilist[run] = list()

        for l in range(begin, end):
            lumilist[run].append(l)

jsonTxt = "{"

runs = lumilist.keys()
runs.sort()

for run in runs:
    lumis = lumilist[run]
    if len(lumis) == 0:
        continue
    
    lumis.sort()

    jsonTxt += '"' + str(run) + '": [[' + str(lumis[0]) + ', '

    l = lumis[0] - 1
    for lumi in lumis:
        if lumi != l + 1:
            jsonTxt += str(l) + '], [' + str(lumi) + ', '

        l = lumi

    jsonTxt += str(lumis[len(lumis) - 1]) + ']], '

jsonTxt = jsonTxt.rstrip(', ')
jsonTxt += "}"

print jsonTxt
