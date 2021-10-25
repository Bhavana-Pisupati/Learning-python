# import os
# f=open("chat.txt","r")
# text = f.read()
# print(text)
# lines=f.readlines()
# print(lines)
# f.close()

# print(os.listdir("C:\\Users\\Administrator\\Downloads"))
# print(os.path.exists("C:\\Users\\Administrator\\Downloads\\Project-2"))

import csv
f = open("ice-cream flavors.csv", "r")
reader = csv.reader(f)
data = [ ]
for row in reader:
    data.append(row)
# print(data)
f.close()

# data = [[ "chocolate", "mint chocolate",
# "peppermint" ],
# [ "vanilla", "matcha", "coffee" ],
# [ "strawberry", "mango", "cherry" ]]
# f = open("results.csv", "w", newline="")
# writer = csv.writer(f)
# for row in data:
#     writer.writerow(row)
# f.close()

# import json
# f = open("icecream.json", "r")
# j = json.load(f)
# print(j)
# f.close()

# d = { "vanilla" : 10,
#     "chocolate" : 27,
#     "other" : [ "strawberry", "matcha", "coffee" ]
# }
# f = open("results.json", "w")
# json.dump(d, f)
# f.close()

# import datetime
# c=datetime.datetime.now() 
# print(c)

# f = open("chat.txt", "r")
# text = f.read()
# f.close()
# people = [ ]
# for line in text.split("\n"):
#      start = line.find("From") + \
#      len("From")
#      line = line[start:]
#      end = line.find(" : ")
#      line = line[:end]
#      if "(Direct Message)" in line:
#         end = line.find("to")
#         line = line[:end]
#      line = line.strip()
#      people.append(line)
# print(people)

# Assume data is a 2D list parsed from the file
header = data[0]
header.pop(0) # remove the ID
header.append("# chocolate")
for row in range(1, len(data)):
    # data[row].pop(0) # remove the ID
    chocCount = 0 # count number of chocolate
    for col in range(len(data[row])):
        # Make all flavors lowercase
        data[row][col] = data[row][col].lower()
        if "chocolate" in data[row][col]:
            chocCount += 1
    # track chocolate count
    data[row].append(chocCount)
# print(data)

# # Header:
# # Semester,
# # #1 Orig, #2 Orig, #3 Orig,
# # #1 Cleaned, #2 Cleaned, #3 Cleaned,
# # #1 Category, #2 Category, #3 Category
# f = open("icecream.csv", "r")
# orig = list(csv.reader(f))
# data = []
# test = []
# for line in orig:
#     if line[0] != "Semester": # skip header
#         # only include coded classes
#         categories = line[7:10]
#         if line[0] == "S21":
#             test.append(categories)
#         else:
#             data.append(categories)
# f.close()

### LOAD DATA ###

# Header:
# Semester,
# #1 Orig,     #2 Orig,     #3 Orig,
# #1 Cleaned,  #2 Cleaned,  #3 Cleaned,
# #1 Category, #2 Category, #3 Category

import csv
f = open("all-icecream.csv", "r")
orig = list(csv.reader(f))
data = []
test = []
for line in orig:
    if line[0] != "Semester": # skip header
        # only include coded classes
        categories = line[7:10]
        if line[0] == "S21":
            test.append(categories)
        else:
            data.append(categories)
f.close()


### HELPER FUNCTIONS ###

def getAllFlavors(data):
    allFlavors = [ ]
    for line in data:
        print(line)
        if line[2] not in allFlavors:
            allFlavors.append(line[2])
    return allFlavors

def bestGuess(flavorProbs):
    bestFlavor = None
    bestProb = -1
    for flavor in flavorProbs:
        if flavorProbs[flavor] > bestProb:
            bestProb = flavorProbs[flavor]
            bestFlavor = flavor
    return bestFlavor


### NAIVE BAYES TRAINING ###

# Probability that a flavor is chosen
def getClassProb(data, flavor):
    count = 0
    for line in data:
        if line[2] == flavor:
            count += 1
    return count / len(data)

# Probability that 1st/2nd favorite is X given that 3rd favorite is C
def getCondProb(data, priorFlavor, thirdFlavor, priorIndex):
    count = 0
    total = 0
    for line in data:
        if line[2] == thirdFlavor:
            total += 1 # only count entries with third flavor
            if line[priorIndex] == priorFlavor:
                count += 1
    return count / total

# Format probabilities nicely
def prob(num):
    return str(round(num*100, 2)) + "%"

# Given 1st and 2nd favorites, what is the most likely 3rd?
def predict(data, first, second, showWork=False):
    flavorProbs = { }
    allFlavors = getAllFlavors(data) # possible flavors
    for flavor in allFlavors:
        flavorProb = getClassProb(data, flavor)
        firstProb = getCondProb(data, first, flavor, 0)
        secondProb = getCondProb(data, second, flavor, 1)
        overallProb = firstProb * secondProb * flavorProb
        if showWork:
            print(flavor, prob(overallProb), "-", prob(firstProb), prob(secondProb), prob(flavorProb))
        flavorProbs[flavor] = overallProb
    return bestGuess(flavorProbs) # find best value

print("PREDICTION:", predict(data, "chocolate", "vanilla", showWork=True))

### TEST ###

# Test each element in the test set based on the model
def runDataset(modelData, testData):
    guessedRight = 0
    for line in testData:
        predictFav = predict(modelData, line[0], line[1])
        actualFav = line[2]
        if predictFav == actualFav:
            guessedRight += 1
    return guessedRight/len(testData)

print("TESTING RESULT:", runDataset(data, test))

import csv
def readData(filename):
    f = open(filename, "r")
    # Semester, 3 orig, 3 cleaned, 3 categories
    data = list(csv.reader(f))
    return data

data = readData("all-icecream.csv")

def getFlavorCounts(data, flavor):
    counts = []
    start = data[0].index("#1 category")
    for i in range(1, len(data)):
        categories = data[i][start:start+3]
        count = categories.count(flavor)
        counts.append(count)
    return counts

print("Chocolate:", getFlavorCounts(data, "chocolate"))

#

def getIceCreamCounts(data):
    d = { }
    start = data[0].index("#1 cleaned")
    for i in range(1, len(data)):
        flavors = data[i][start:start+3]
        for flavor in flavors:
            if flavor not in d:
                d[flavor] = 0
            d[flavor] = d[flavor] + 1
    return d

counts = getIceCreamCounts(data)
for flavor in counts:
    print(flavor, counts[flavor])

import matplotlib.pyplot as plt

def combineUncommon(counts, cutoff):
    newCounts = { "other" : 0 }
    for flavor in counts:
        if counts[flavor] < cutoff:
            newCounts["other"] += counts[flavor]
        else:
            newCounts[flavor] = counts[flavor]
    return newCounts

counts = combineUncommon(getIceCreamCounts(data), 3)

flavors = []
flavorCounts = []
for flavor in counts:
    flavors.append(flavor)
    flavorCounts.append(counts[flavor])

plt.pie(flavorCounts, labels=flavors)

plt.show()