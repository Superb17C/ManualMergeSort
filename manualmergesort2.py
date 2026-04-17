from os.path import isfile
from random import choice, shuffle


global numQuestionsAsked
numQuestionsAsked = 0


class MergePair:

    def __init__(self, unmerged1, unmerged2, mergedStart, mergedEnd):
        self.unmerged1 = unmerged1
        self.unmerged2 = unmerged2
        self.mergedStart = mergedStart
        self.mergedEnd = mergedEnd

    def makeMove(self):
        mergeFromEnd = randomBoolean()
        if mergeFromEnd:
            if firstRanksBetter(self.unmerged1[-1], self.unmerged2[-1]):
                self.mergedEnd.insert(0, self.unmerged2[-1])
                self.unmerged2 = self.unmerged2[:-1]
            else:
                self.mergedEnd.insert(0, self.unmerged1[-1])
                self.unmerged1 = self.unmerged1[:-1]
        else:
            if firstRanksBetter(self.unmerged1[0], self.unmerged2[0]):
                self.mergedStart.append(self.unmerged1[0])
                self.unmerged1 = self.unmerged1[1:]
            else:
                self.mergedStart.append(self.unmerged2[0])
                self.unmerged2 = self.unmerged2[1:]

    def isFinished(self):
        return len(self.unmerged1) == 0 or len(self.unmerged2) == 0

    def getResultingChain(self):
        return self.mergedStart + self.unmerged1 + self.unmerged2 + self.mergedEnd


def buildInitialChainsFromFile(filePath):
    if isfile(filePath):
        chains = []
        with open(filePath, "r") as f:
            for line in f:
                chains.append([line[:-1]])
        print(f"Successfully loaded {len(chains)} items to sort.")
        return chains
    else:
        raise Exception("File not found. Check file path name and try again.")


def randomBoolean():
    return choice([True, False])


def isEven(n):
    return n % 2 == 0


def firstRanksBetter(choice1, choice2):
    global numQuestionsAsked
    numQuestionsAsked += 1
    switchChoiceOrder = randomBoolean()
    if switchChoiceOrder:
        choiceNumbered1 = choice2
        choiceNumbered2 = choice1
    else:
        choiceNumbered1 = choice1
        choiceNumbered2 = choice2
    print("")
    print("Q" + str(numQuestionsAsked) + ".  Which should rank higher / appear first?")
    print("1.  " + choiceNumbered1)
    print("2.  " + choiceNumbered2)
    choice = input("Enter the number of your choice:  ")
    while choice != "1" and choice != "2":
        choice = input("Invalid choice. Try again:  ")
    return (choice == "1" and not switchChoiceOrder) or (choice == "2" and switchChoiceOrder)


def convertToPairs(chains):
    pairs = []
    if isEven(len(chains)):
        index = 0
    else:
        pairs.append(MergePair([], [], chains[0], []))
        index = 1
    while index + 1 < len(chains):
        pairs.append(MergePair(chains[index], chains[index + 1], [], []))
        index += 2
    return pairs


def convertToChains(pairs):
    chains = []
    for pair in pairs:
        chains.append(pair.getResultingChain())
    return chains


def printNumberedChain(chain):
    print("")
    print("Here is the ranked list, after " + str(numQuestionsAsked) + " comparisons:")
    for i in range (0, len(chain)):
        print(str(i + 1) + ".  " + str(chain[i]))


def manuallySort(filePath):
    chains = buildInitialChainsFromFile(filePath)
    while len(chains) > 1:
        shuffle(chains)
        pairs = convertToPairs(chains)
        areAllFinished = False
        while not areAllFinished:
            areAllFinished = True
            shuffle(pairs)
            for pair in pairs:
                if not pair.isFinished():
                    areAllFinished = False
                    pair.makeMove()
        chains = convertToChains(pairs)
    printNumberedChain(chains[0])
    return chains[0]


manuallySort("items.txt")