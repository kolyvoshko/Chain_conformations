__author__ = 'Eugene Kolivoshko'


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


class Chain(object): # TODO add plot functional
    def __init__(self, maxLen):
        self.maxLen = maxLen
        self.chain = []
        self.__count = 1
        self.chain.append(Section(self.__count, [0, 0], [0, 1]))
        self._endPoint = [0, 1]
        self.__thisSection = self.chain[-1]
        self.allow = True
        self.__thisPoint = [0, 1]
        self.length = 1.0

    def genChain(self, style, list=None):
        if style == 'random': import random
        i = 0
        while i < self.maxLen - 1:
            if style == 'random': rotate = random.randrange(-1, 2)
            if style == 'range': rotate = [0, 1]
            if style == 'list': rotate = list[i]
            self.__next(rotate)

            if self.allow == False:
                break
            i += 1

    def __next(self, rotate):
        self.__thisSection = self.chain[-1]
        angle = Angle(self.__thisSection.angle)
        nextSection = Section(self.__count, [0, 0], rotate)

        if rotate == -1:
            angle.prev()

        if rotate == 1:
            angle.next()

        nextSection.point[0] = self.__thisSection.point[0] + self.__thisSection.angle[0]
        nextSection.point[1] = self.__thisSection.point[1] + self.__thisSection.angle[1]
        nextSection.angle = angle.angle

        if self._test(nextSection):
            self.__count += 1
            nextSection.number = self.__count
            self.chain.append(nextSection)

    def _test(self, section):
        self._getEndPoint(section)
        i = 0
        while i < self.__count:
            if self.chain[i].point == section.point or self.chain[i].point == self._endPoint:
                self.allow = False
                return False
                break
            i += 1
        return True

    def _getEndPoint(self, section):
        self._endPoint[0] = section.point[0] + section.angle[0]
        self._endPoint[1] = section.point[1] + section.angle[1]

    def getLength(self):
        import numpy as np
        self.length = np.sqrt(self.endPoint[0] ** 2 + self.endPoint[1] ** 2)


class ListConfigurations(object): # TODO add plot functional
    def __init__(self, length):
        self.maxChainLength = length
        self.gapConfigurations = 0
        self.allowConfigurations = 0
        self.lengthArr
        self._genConfigurations()

    def _genConfigurations(self):
        import itertools

        for list in itertools.product(range(-1, 2), repeat=(self.maxChainLength - 1)):
            chain = Chain(self.maxChainLength)
            chain.genChain('list', list)
            chain.getLength()

            if chain.allow:
                self.allowConfigurations += 1
                self.length += chain.length
            else:
                self.gapConfigurations += 1

            print("Average length: %f" % (float(self.length)/len(self.allowConfigurations)))

obj2 = ListConfigurations(11)
print(obj2.allowConfigurations, obj2.gapConfigurations)

