myRDP = { 'Actinobacter': 'GATCGA...TCA', 'subtilus sp.': 'ATCGATT...ACT' }
myNames = { 'Actinobacter': '8924342' }

rdpSet = set(myRDP)
namesSet = set(myNames)

for name in rdpSet.intersection(namesSet):
    print (name, myNames[name])