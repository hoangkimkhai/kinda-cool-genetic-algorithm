import string
import random
import math

popsize = 200;
target = ['t', 'O', 'b', 'e', 'O', 'R', 'N', 'o', 't', 'T', 'o', 'b', 'E', 'a', 'B', 'c']


class DNA(object):
    def __init__(self, target_length, target):
        self.target = target
        self.target_length = target_length
        self.fitness = 0
        self.genes = [None] * self.target_length
        for i in range(target_length):
            rnd = random.choice(string.ascii_letters)
            self.genes[i] = rnd

    def calcFitness(self):
        score = 0
        for i in range(self.target_length):
            if self.genes[i] == self.target[i]:
                score += 1
        score = score / len(self.genes)
        self.fitness = score

    def crossOver(self, partnerB):
        midpoint = random.randint(0, len(self.genes))
        child = DNA(self.target_length, self.target)
        for i in range(len(self.genes)):
            if i > midpoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partnerB.genes[i]

        return child

    def mutate(self, rate):
        for i in range(len(self.genes)):
            rnd = random.uniform(0, 1)
            if rnd < rate:
                self.genes[i] = random.choice(string.ascii_letters)

    def listToString(self):
        str1 = ""
        for ele in self.genes:
            str1 += ele
        return str1

    def __str__(self):
        return self.listToString()


class Population(object):
    def __init__(self, popsize, target):
        self.target = target
        self.pop = [None] * popsize
        self.matingPool = []
        self.maxFitness = 0
        self.maxFitnessIndex = 0
        self.popsize = popsize
        for i in range(popsize):
            self.pop[i] = DNA(len(target), target)

    def calcFitness(self):
        for i in range(popsize):
            self.pop[i].calcFitness()
            if self.pop[i].fitness >= self.maxFitness:
                self.maxFitness = self.pop[i].fitness
                self.maxFitnessIndex = i

    def naturalSelection(self):
        for i in range(popsize):
            current = self.pop[i]
            proportion = current.fitness / self.maxFitness
            n = math.floor(proportion)
            for k in range(n):
                self.matingPool.append(current)

    def generateNextGeneration(self):
        low = 0
        high = len(self.matingPool) - 1
        for i in range(self.popsize):
            a = random.randint(low, high)
            b = random.randint(low, high)
            partnerA = self.matingPool[a]
            partnerB = self.matingPool[b]
            child = partnerA.crossOver(partnerB)
            child.mutate(0.02)
            self.pop[i] = child

    def isFinished(self):
        return self.maxFitness >= 1

    def display(self):
        print(self.pop[self.maxFitnessIndex])


def main():
    geCount = 0
    pop = Population(popsize, target)
    pop.calcFitness()
    maxFit = 0
    print("Gen: {0}, maxFitness: {1}".format(geCount, pop.maxFitness))
    print(pop.isFinished())
    while not pop.isFinished():
        pop.naturalSelection()
        pop.generateNextGeneration()
        pop.calcFitness()
        if pop.maxFitness > maxFit:
            maxFit = pop.maxFitness
            print("Gen: {0}, maxFitness: {1}".format(geCount, pop.maxFitness))
            pop.display()
        geCount += 1
    pop.display()


main()
