#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Sorted and Grouped CSV BOM
# grouped Part Value, Footprint, Voltage, Toll
#

# Import the KiCad python helper module and the csv formatter

"""
    @package
Generate a comma delimited list (csv file type).
    Components are sorted by ref and grouped by:
        Value Footprint  Voltage Tolerance Temp Current
    Fields are (if exist)
    'Ref', 'Qnty', 'Value', 'Footprint', 
    'Manf#', 'Voltage', 'Tolerance', 'Power', 'Temp', 'Current', 'Description'
    version 3.3 - 06.2016  [bom_grouped_v33_ky.py]
"""

#maui
import logging
import textwrap
#maui
import bom_grouped_v33_ky
import shutil
import os
import ntpath

import csv
import sys


# logging.basicConfig(filename='example.log',level=logging.DEBUG)

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
#maui
net = bom_grouped_v33_ky.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    f = open(sys.argv[2], 'wb')
except IOError:
    print >> sys.stderr, __file__, ":", e
    f = stdout

# Create a new csv writer object to use as the output formatter
#out = csv.writer(f, delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)
#maui
out = csv.writer(f, delimiter=',', quotechar='\"')
#out = csv.writer(f, delimiter=',', quotechar='\"', escapechar='', quoting=csv.QUOTE_ALL)
#out = csv.writer(f, delimiter='\t', quotechar='\"', escapechar='', quoting=csv.QUOTE_NONE)

# Output a set of rows for a header providing general information
#maui
out.writerow(['In:', sys.argv[1]])

out.writerow(['Source:', net.getSource()])
out.writerow(['Date:', net.getDate()])
out.writerow(['Tool:', net.getTool()])
out.writerow(['Component Count:', len(net.components)])         
out.writerow(['Ref', 'Qnty', 'Value', 'Footprint', 'Manf#', 'Voltage', 'Tolerance', 'Power', 'Temp', 'Current', 'Description'])

#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')

# Get all of the components in groups of matching parts + values (see ky.py)
grouped = net.groupComponents()

# Output all of the component information
for group in grouped:
    refs = ""

    # Add the reference of every component in the group and keep a reference 
    # to the component so that the other data can be filled in once per group
    for component in group:
        #refs += component.getRef() + ", "
        if len(group)==1:
            refs += component.getRef()
        else :
            refs += component.getRef()+ " "
        c = component
        #maui
    refs=refs.rstrip(' ');
    #logging.warning(c.getFootprint())
    
    # Fill in the component groups common data
#    out.writerow([refs, len(group), c.getValue(), c.getLib() + "/" + c.getPart(), c.getDatasheet(),
#        c.getDescription(), c.getField("Vendor")])
    #out.writerow([refs, len(group), c.getValue(), c.getLib() + "/" + c.getFootprint(),
    #    c.getDescription(), c.getField("Voltage"), c.getField("Toll")])

    out.writerow([refs, len(group), c.getValue(), c.getFootprint(),
       c.getField('Manf#'), c.getField('Voltage'), c.getField('Tolerance'), c.getField('Power'), c.getField('Temp'), c.getField('Current'), c.getDescription()])  

#    out.writerow([("{0:30s}".format(c.getField("Value")), "{0:30s}".format(c.getField("Footprint")) )] )
        
#maui
#os.path.splitext(sys.argv[2])[0]
f.close()
#csv_file=ntpath.basename(sys.argv[2]).split('.')[0]+'.csv'
csv_file=os.path.splitext(sys.argv[2])[0]+'.csv'

shutil.copy (sys.argv[2], csv_file)  
#print sys.argv[2], "=>", ntpath.basename(sys.argv[2]).split('.')[0]+".csv      

res = []
max_len_element = [0,0,0,0,0,0,0,0,0,0,0,0]

with open(csv_file) as csvfile:
    file1 = csv.reader(csvfile, delimiter=',')
    line=''
    p=0
    for row in file1:
        k=0
        for element in row: 
            # print (len(element))
            len_element=len(element)
            k=k+1
            # print k
            if p>4:
                if len_element <50:
                    if len_element > max_len_element[k]:
                        max_len_element[k]=len_element
                else:
                    max_len_element[k]=50                
        p=p+1
    p=0

with open(csv_file) as csvfile:
    file2 = csv.reader(csvfile, delimiter=',')
    line=''
    p=0    
    for row in file2:
        k=0
        for element in row: 
            # print (len(element))
            len_element=len(element)
            k=k+1
            # print k
            #dif = 30- len_element
            dif=0
            if p>4:
                if len_element >= 50:
                    wrapped = textwrap.wrap(element, 50)
                    # for index, item in enumerate(wrapped):
                    #     print index, item
                    # print item[0]    
                    for line1 in wrapped:
                        #print line1
                        line +=line1+'\r\n'
                    line=line.rstrip('\n');
                    line=line.rstrip('\r');
                    index = line.find(line1)
                    line_space=''
                    for index2 in range(k-1):
                        line_space+=(max_len_element[k-1]+3)*' '
                    line_space=line_space[:len(line_space)-3]
                    line = line[:index] + line_space + line[index:]
                    dif = 50-len(line1)+3
                    line+=','.ljust(dif,' ')
                    #dif = max_len_element[k]-50+3
                    #line += element+ ','.ljust(dif,' ')+'\r\n'
                else:
                    dif = max_len_element[k]-len_element+3
                    line += element+ ','.ljust(dif,' ')
            else:
                line += element
        line += '\r\n'
        p=p+1
    res.append(line)

txt_file=os.path.splitext(sys.argv[2])[0]+'.txt'
# now, outside the loop, we can do this:
with open(txt_file, 'wb') as f:
    f.writelines(res)

