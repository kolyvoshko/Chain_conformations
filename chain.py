#!/usr/bin/python
import matplotlib
import numpy as np


class Angle(object):
    def __init__(self, a):
        self.__list = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        self.__index = 0
        self.angle = [1, 0]
        for i in [0, 1, 2, 3]:
            if a == self.__list[i]:
                self.__index = i
                self.angle = self.__list[i]

    def prev(self):
        if self.__index == 0:
            self.__index = 3
        else:
            self.__index -= 1

        self.angle = self.__list[self.__index]

    def next(self):
        if self.__index == 3:
            self.__index = 0
        else:
            self.__index += 1

        self.angle = self.__list[self.__index]


class Section(object):
    def __init__(self, n, p, a):
        self.number = n
        self.point = p
        self.angle = a

    def __str__(self):
        return "%d %s %d" % (self.number, self.point, self.angle)


class Chain(object):
    def __init__(self, maxLen):
        self.maxLen = maxLen
        self.count = 1
        self.chain = []
        self.chain.append(Section(self.count, [0, 0], 90))
        self.thisSection = self.chain[-1]
        self.len = self.chain[-1].number
        self.allow = True
        self.bad = False
        self.endPoint = []
        self.length = 1.0

    def __str__(self):
        i = 0
        str = ""
        while i < self.count:
            str += "%d %s\t %s\t\n" % (self.chain[i].number, self.chain[i].point, self.chain[i].angle)
            i += 1
        return str

    def next(self, angle):
        self.thisSection = self.chain[-1]
        nextSection = Section(self.count, [0, 0], angle)

        nextSection.point[0] = int(round(self.thisSection.point[0] + np.cos(self.thisSection.angle * np.pi / 180.)))
        nextSection.point[1] = int(round(self.thisSection.point[1] + np.sin(self.thisSection.angle * np.pi / 180.)))

        if self.thisSection.angle not in [0, 90, 180, 270]:
            print "Chain -> next: angle is bad"
            exit(0)

        if self.test(nextSection.point, nextSection.angle):
            self.count += 1
            nextSection.number = self.count
            self.chain.append(nextSection)
            self.len = nextSection.number
        else:
            self.allow = False

    def test(self, p, a):
        i = self.count - 1
        self.getEndPoint(p, a)

        if self.endPoint == self.chain[-1].point:
            self.bad = True

        while i >= 0:
            if self.chain[i].point == p:
                return False
                break

            if self.chain[i].point == self.endPoint:
                return False
                break
            i -= 1

        return True

    def plot(self):
        import matplotlib.pyplot as plt

        plt.grid(True)
        plt.xlim(-self.maxLen, self.maxLen)
        plt.ylim(-self.maxLen + 2, self.maxLen + 1)
        self.plotChain()
        plt.savefig("chain.png")

    def plotChain(self):
        i = 0
        x = []
        y = []
        while i < self.count:
            x.append(self.chain[i].point[0])
            y.append(self.chain[i].point[1])
            i += 1

        x.append(self.endPoint[0])
        y.append(self.endPoint[1])
        import matplotlib.pyplot as plt

        plt.plot(x, y, 'kx-', alpha=0.5)

    def genChain(self, style, list=None):
        if style == 'random': import random

        i = 0
        while i < self.maxLen - 1:
            if style == 'random': angle = random.randrange(0, 360, 90)
            if style == 'range': angle = 90
            if style == 'list': angle = list[i]
            self.next(angle)
            i += 1

    def getEndPoint(self, p, a):
        x = int(round(p[0] + np.cos(a * np.pi / 180.)))
        y = int(round(p[1] + np.sin(a * np.pi / 180.)))
        self.endPoint = [x, y]

    def getLength(self):
        self.length = np.sqrt(self.endPoint[0] ** 2 + self.endPoint[1] ** 2)


class ListConfigurations(object):
    def __init__(self, length):
        self.countConf = 0
        self.maxChainLength = length
        self.gapConfigurations = []
        self.allowConfigurations = []
        self.listConfigurations = []
        self.lengthArr = []

    def genConfigurations(self):
        import itertools

        for list in itertools.product(range(0, 360, 90), repeat=(self.maxChainLength - 1)):
            chain = Chain(self.maxChainLength)
            chain.genChain('list', list)

            if chain.allow:
                self.allowConfigurations.append(chain)
                lens = len(self.allowConfigurations)
                if lens%1000 is 0:
                    print lens
            else:
                if chain.bad == False:
                    self.gapConfigurations.append(0)

    def plot(self):
        import matplotlib.pyplot as plt

        plt.figure()
        plt.grid(True)
        plt.xlim(-self.maxChainLength, self.maxChainLength)
        plt.ylim(-self.maxChainLength + 2, self.maxChainLength + 1)
        i = 0
        while i < len(self.allowConfigurations):
            self.allowConfigurations[i].plotChain()
            i += 1
        plt.savefig("allChain.png")

    def getLength(self):
        i = 0
        length = 0
        while i < len(self.allowConfigurations):
            self.allowConfigurations[i].getLength()
            self.lengthArr.append(self.allowConfigurations[i].length)

            length += self.allowConfigurations[i].length
            i += 1

        print("Median length: %f" % (float(length)/len(self.allowConfigurations)))

        import matplotlib.pyplot as plt

        plt.figure()
        plt.grid(True)
        plt.xlim(0, self.maxChainLength + 0.5)
        plt.xlabel("Chain length")
        plt.ylabel("Number of chains")
        n, bins, patches = plt.hist(self.lengthArr, 1000, facecolor='black', alpha=0.5)
        print max(n)
        print(bins[np.where(n == max(n))])
        print n
        print bins
        plt.savefig("distHist.png")


obj = ListConfigurations(11)
obj.genConfigurations()
print(len(obj.allowConfigurations), len(obj.gapConfigurations))

obj.allowConfigurations[8502].plot()
obj.plot()

obj.getLength()


#print(obj2.allowConfigurations, obj2.gapConfigurations)