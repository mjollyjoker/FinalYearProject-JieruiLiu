import pickle

sn1 = pickle.load(open("../serverbackup-05-04/screenNames1.p","rb"))
sn2 = pickle.load(open("../serverbackup-05-04/screenNames2.p","rb"))
sn3 = pickle.load(open("../serverbackup-05-04/screenNames3.p","rb"))
sn4 = pickle.load(open("../serverbackup-05-04/screenNames4.p","rb"))

allSN = list(set(sn1)|set(sn2)|set(sn3)|set(sn4))

singleLength = (round(len(allSN)/8))

pickle.dump(allSN[:singleLength],open("../screenNameDistribute/screenNames5.p","wb"))
allSN = allSN[singleLength:]
pickle.dump(allSN[:singleLength],open("../screenNameDistribute/screenNames6.p","wb"))
allSN = allSN[singleLength:]
pickle.dump(allSN[:singleLength],open("../screenNameDistribute/screenNames7.p","wb"))
allSN = allSN[singleLength:]
pickle.dump(allSN[:singleLength],open("../screenNameDistribute/screenNames8.p","wb"))
allSN = allSN[singleLength:]
pickle.dump(allSN[:singleLength],open("../screenNameDistribute/screenNames9.p","wb"))
allSN = allSN[singleLength:]
pickle.dump(allSN[:singleLength],open("../screenNameDistribute/screenNames10.p","wb"))
allSN = allSN[singleLength:]
pickle.dump(allSN[:singleLength],open("../screenNameDistribute/screenNames11.p","wb"))
allSN = allSN[singleLength:]
pickle.dump(allSN,open("../screenNameDistribute/screenNames12.p","wb"))

