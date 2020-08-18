# Maura Choudhary
# June 29, 2020
# Read in a text file and export as a formatted csv
import ipaddress
import csv

class Address:
    def __init__(self, vlan, address, subnetMask, tenant, vrf, status = "Active", cidrAddress = "Default"):
        self.vlan = vlan
        self.address = address
        self.cidrAddress = cidrAddress
        self.subnetMask = subnetMask
        self.tenant = tenant
        self.vrf = vrf
        self.status = status
    def Convertcidr(self):
        myString = self.address + "/" + self.subnetMask
        network = ipaddress.IPv4Network(unicode(myString), strict=False)
        netmaskBits = str(network.prefixlen)
        networkAddress = str(network.network_address)
        self.cidrAddress = networkAddress + "/" + netmaskBits
        #print(self.tenant)
        #print(self.cidrAddress)
# Reading in nondeliminated data
rawDataFile = open("rawdata.txt", "r")
rawdata = []
line = rawDataFile.readline()
rawdata.append(line)
while line:
    line = rawDataFile.readline()
    rawdata.append(line)

# add delimiter
for x in range(len(rawdata)-1):
    rawdataLine = rawdata[x].split()
    #print(rawdataLine)
    rawdata[x] = rawdataLine[0] + ", " + rawdataLine[1] + ", " + rawdataLine[2] + ", "
    for y in range(3, len(rawdataLine)):
        if (y < (len(rawdataLine)-1)):
            rawdata[x] = rawdata[x] + rawdataLine[y] + " "
        else:
            rawdata[x] = rawdata[x] + rawdataLine[y] + "\n"

# write to file
newData = open("data.txt", "w")
newData.writelines(rawdata)
newData.close()


# Reading in the data
dataFile = open("data.txt", "r")
data = []
line = dataFile.readline()
data.append(line)
while line:
    line = dataFile.readline()
    data.append(line)
#test
#for x in range(len(data)):
#    print data[x]

#create objects
vrf = raw_input("Enter a vrf for this data: ")
myAddresses = []
for x in range(len(data)-1):
    splitData = data[x].split(', ')
    #print(splitData)
    #remove quotes and newlines
    if(len(splitData[3]) > 2):
        myString = splitData[3]
        splitData[3] = myString[1:(len(myString)-2)]
    
    vlan = splitData[0]
    address = splitData[1]
    subnetMask = splitData[2]
    tenant = splitData[3]
    address = Address(vlan, address, subnetMask, tenant, vrf)
    myAddresses.append(address)

# convert to cidr notation
for x in range(len(myAddresses)):
    myAddresses[x].Convertcidr()

# write to csv
with open('csvfile.csv', 'w') as f:
    thewriter = csv.writer(f)

    thewriter.writerow(['address', 'status', 'vrf', 'tenant'])

    for x in range(len(myAddresses)):
        address = myAddresses[x].cidrAddress
        status = myAddresses[x].status
        vrf = myAddresses[x].vrf
        tenant = myAddresses[x].tenant
        thewriter.writerow([address, status, vrf, tenant])

