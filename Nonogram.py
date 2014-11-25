import BaseNonogram
import itertools

class Nonogram(BaseNonogram.Nonogram):
    def _copy(self):
        n = Nonogram(self.getNumRows(), self.getNumColumns(),
                     self.getRowClues(), self.getColumnClues())
        array = []
        for x in range(0, self.getNumRows()):
            array.append(self.getRow(x))
        n._array = array[:]
        return n

    def _validSegment(self, first, second):
        if (len(first) != len(second)):
            return False
        for x in range(0, len(first)):
            if (first[x] == 1 and second[x] != 1):
                return False
            if (first[x] == "X" and second[x] == 1):
                return False
        return True
            
    def _booleanAnd(self, first, second):
        if (len(first) != len(second)):
            raise Exception("Different size, can't perform AND.")
        result = []
        for x in range(0, len(first)):
            if ((first[x] == 1 or second[x] == 1) and first[x] != "X" and second[x] != "X"):
                result.append(1)

    def _generatePossibleSegments(self, current, clues):
        possible = []
        length = len(current)
        numClues = len(clues)

        if (self._getPrintFlag()):
            print "\tCreating iterater."
        args = []
        for c in current:
            if (c == 0):
                args.append([0,1])
            elif (c == 1):
                args.append([1])
            elif (c == "X"):
                args.append([0])
        #iterater = itertools.product([0,1],repeat=length)
        iterater = itertools.product(*args)
        if (self._getPrintFlag()):
            print "\tIterater created."
        for seg in iterater:
            l = list(seg)
            if (self._validSegment(current, l)):
                if (self._sum(l) == sum(clues)):
                    listStr = "".join(map(str,l))
                    listStr.replace("X","0")
                    isValid = True
                    for clue in clues:
                        clueSeg = self._makeSegment(clue)
                        try:
                            index = listStr.index("1")
                        except:
                            isValid = False
                            break
                        listStr = listStr[index:]
                        if (listStr[:len(clueSeg)-1] != clueSeg[:-1]):
                            isValid = False
                            break
                        else:
                            if (len(listStr) < len(clueSeg)-1 and listStr[len(clueSeg)] == "1"):
                                isValid = False
                                break
                        listStr = listStr[len(clueSeg):]
                    if (isValid):
                        possible.append(l)
        return possible
    
    def inputRowCommon(self, rowNumber):
        row = self.getRow(rowNumber)
        clues = self.getRowClue(rowNumber)
        length = len(row)-1

        leftPointer = 0
        rightPointer = 0

        #Truncate completed
        while (len(row) > 0 and row.count(0) != 0 and row[0] != 0):
            if (row[0] == "X"):
                row.pop(0)
                leftPointer += 1
            elif (row[0] == 1):
                segment = self._makeSegment(clues[0], True)
                for y in range(0, clues[0]):
                    if (row[y] == 0):
                        self.setSpot(rowNumber, y+leftPointer, segment[y])
                    elif (str(row[y]) != segment[y]):
                        if (self._getPrintFlag()):
                            print row[y]
                            print segment[y]
                            print type(row[y])
                            print type(segment[y])
                            print row[y] != segment[y]
                        raise Exception("Not solvable. (Potential mistake)")
                if (clues[0]+leftPointer < self.getNumColumns()):
                    self.setSpot(rowNumber, clues[0]+leftPointer, "X")
                for y in range(0, clues[0]):
                    row.pop(0)
                    leftPointer += 1
                clues.pop(0)

        #print "leftPointer1:",leftPointer

        row.reverse()
        clues.reverse()
        while (len(row) > 0 and row.count(0) != 0 and row[0] != 0):
            if (row[0] == "X"):
                row.pop(0)
                rightPointer += 1
            elif (row[0] == 1):
                segment = self._makeSegment(clues[0], True)
                for y in range(0, clues[0]):
                    if (row[y] == 0):
                        self.setSpot(rowNumber, length-y-rightPointer, segment[y])
                    elif (str(row[y]) != segment[y]):
                        raise Exception("Not solvable. (Potential mistake)")
                if (length-clues[0]-rightPointer > 0):
                    self.setSpot(rowNumber, length-clues[0]-rightPointer, "X")
                for y in range(0, clues[0]):
                    row.pop(0)
                    rightPointer += 1
                clues.pop(0)
        row.reverse()
        clues.reverse()
        #print "leftPointer2:",leftPointer

        #Find common for the resultant
        if ((leftPointer + rightPointer + len(row)) != self.getNumColumns()):
            raise Exception("Issue.")

        if (len(clues) == 0):
            for y in range(0, len(row)):
                if (self.getSpot(rowNumber, y) == 0):
                    self.setSpot(rowNumber, y, "X")
        if (row.count(0) == 0):
            return

        rowSpotSum = sum(clues) + len(clues) - 1
        rowLength = len(row)
        remainder = rowLength-rowSpotSum

        lPointer = leftPointer
        for clue in clues:
            for y in range(lPointer+remainder, lPointer+clue):
                self.setSpot(rowNumber, y, 1)
            lPointer += clue + 1

        if (sum(self.getRowClue(rowNumber)) == self._sum(self.getRow(rowNumber))):
            for y in range(0, self.getNumColumns()):
                if (self.getSpot(rowNumber, y) == 0):
                    self.setSpot(rowNumber, y, "X")

            
        if (self._getPrintFlag()):
            print "Row:",row
            print "Clues:",clues
            print "Full Row:",self.getRow(rowNumber)
            print "Full Clues:",self.getRowClue(rowNumber)
            print "LeftPointer:",leftPointer

        if (row.count("X") == 0 or len(clues) == 0):
            return
        #Edge Stuff
        index = row.index("X")
        part = row[:index]
        if (clues[0] > len(part)):
            for y in range(0, len(part)):
                """
                print ""
                print part
                print row
                print clues
                print leftPointer
                print y
                print ""
                """
                self.setSpot(rowNumber, leftPointer+y, "X")
        row.reverse()
        clues.reverse()
        index = row.index("X")
        part = row[:index]
        if (clues[0] > len(part)):
            for y in range(0, len(part)):
                self.setSpot(rowNumber, length-rightPointer-y, "X")
      
    def inputColumnCommon(self, columnNumber):
        column = self.getColumn(columnNumber)
        clues = self.getColumnClue(columnNumber)
        length = len(column) - 1
        
        topPointer = 0
        bottomPointer = 0

        #Truncate completed
        while (len(column) > 0 and column.count(0) != 0 and column[0] != 0):
            if (column[0] == "X"):
                column.pop(0)
                topPointer += 1
            elif (column[0] == 1):
                segment = self._makeSegment(clues[0], True)
                for x in range(0, clues[0]):
                    if (column[x] == 0):
                        self.setSpot(x+topPointer, columnNumber, segment[x])
                    elif (str(column[x]) != segment[x]):
                        if (self._getPrintFlag()):
                            print x
                            print column[x]
                            print column
                            print segment[x]
                            print segment
                            print type(str(column[x]))
                            print type(segment[x])
                            print str(column[x]) != segment[x]
                            print ""
                            print self
                        raise Exception("Not solvable. (Potential mistake)")
                if (clues[0]+topPointer < self.getNumRows()):
                    self.setSpot(clues[0]+topPointer, columnNumber, "X")
                #print clues[0]+topPointer
                for x in range(0, clues[0]):
                    column.pop(0)
                    topPointer += 1
                clues.pop(0)

        column.reverse()
        clues.reverse()
        while (len(column) > 0 and column.count(0) != 0 and column[0] != 0):
            if (column[0] == "X"):
                column.pop(0)
                bottomPointer += 1
            elif (column[0] == 1):
                segment = self._makeSegment(clues[0], True)
                for x in range(0, clues[0]):
                    if (column[x] == 0):
                        self.setSpot(length-x-bottomPointer, columnNumber, segment[x])
                    elif (str(column[x]) != segment[x]):
                        raise Exception("Not solvable. (Potential mistake)")
                if (length-clues[0]-bottomPointer > 0):
                    self.setSpot(length-clues[0]-bottomPointer, columnNumber, "X")
                #print length-clues[0]-bottomPointer
                #print length
                #print clues[0]
                #print bottomPointer
                for x in range(0, clues[0]):
                    column.pop(0)
                    bottomPointer += 1
                clues.pop(0)
        column.reverse()
        clues.reverse()

        #Find common for the resultant
        if ((topPointer + bottomPointer + len(column)) != self.getNumRows()):
            raise Exception("Issue.")
            
        if (len(clues) == 0):
            for x in range(0, len(column)):
                if (self.getSpot(x, columnNumber) == 0):
                    self.setSpot(x, columnNumber, "X")
            return
        if (column.count(0) == 0):
            return
        
        columnSpotSum = sum(clues) + len(clues) - 1
        columnLength = len(column)
        remainder = columnLength - columnSpotSum
        
        if (self._getPrintFlag()):
            print "Column: ",column
            print "Clues: ",clues
            print "Top Pointer: ",topPointer
            print "Remainder: ",remainder

        tPointer = topPointer
        for clue in clues:
            for x in range(tPointer+remainder, tPointer+clue):
                self.setSpot(x, columnNumber, 1)
            tPointer += clue + 1
            
        if (sum(self.getColumnClue(columnNumber)) == self._sum(self.getColumn(columnNumber))):
            for x in range(0, self.getNumRows()):
                if (self.getSpot(x, columnNumber) == 0):
                    self.setSpot(x, columnNumber, "X")

        if (self._getPrintFlag()):
            print column
            print clues

        if (column.count("X") == 0 or len(clues) == 0):
            return
        #Edge Stuff
        index = column.index("X")
        part = column[:index]
        if (clues[0] > len(part)):
            for x in range(0, len(part)):
                """
                print ""
                print part
                print column
                print clues
                print topPointer
                print x
                print ""
                """
                if (topPointer+x < self.getNumRows()):
                    self.setSpot(topPointer+x, columnNumber, "X")
        column.reverse()
        clues.reverse()
        index = column.index("X")
        part = column[:index]
        if (clues[0] > len(part)):
            for x in range(0, len(part)):
                self.setSpot(length-bottomPointer-x, columnNumber, "X")

    def markFromRowEdges(self, rowNumber):
        row = self.getRow(rowNumber)
        clues = self.getRowClue(rowNumber)
        length = len(row)-1

        if (row.count(0) == 0):
            return

        pointers = [0,0]

        #Reduce edges
        for x in range(0,2):
            while (row[0] != 0):
                if (row[0] == "X"):
                    row.pop(0)
                    pointers[x] += 1
                elif (row[0] == 1):
                    count = 0
                    while (row[0] == 1):
                        row.pop(0)
                        pointers[x] += 1
                        count += 1
                    if (clues[0] != count):
                        """
                        print clues[0]
                        print count
                        print self.getRow(rowNumber)
                        print row
                        print self.getRowClue(rowNumber)
                        print clues
                        """
                        break
                        #raise Exception("Clues not equal to count.")
                    clues.pop(0)
            row.reverse()
            clues.reverse()

        if (len(clues) == 0):
            return

        if (self._getPrintFlag()):
            print row
            print clues
        
        leftPointer = pointers[0]
        rowStr = "".join(map(str,row))
        clueSeg = self._makeSegment(clues[0], True)
        while (clueSeg in rowStr and clues.count(clues[0]) == 1):
            index = rowStr.index(clueSeg)
            if (self._getPrintFlag()):
                print ""
                print "ClueSeg:",clueSeg
                print "RowStr:",rowStr
                print "Pointer:",leftPointer
                print "Clues[0]:",clues[0]
                print "Index:",index
                print (rowStr[index-1] == "X" or clues[0] > index)
            if (index != 0):
                if (rowStr[index-1] == "X" or clues[0] > index):
                    for y in range(0, index):
                        #print leftPointer+y
                        self.setSpot(rowNumber, leftPointer+y, "X")
                else:
                    break
            clues.pop(0)
            if (len(clues) == 0):
                break
            rowStr = rowStr[index+len(clueSeg):]
            clueSeg = self._makeSegment(clues[0])

        row.reverse()
        clues.reverse()

        if (len(clues) == 0):
            return
        
        rightPointer = pointers[1]
        rowStr = "".join(map(str,row))
        clueSeg = self._makeSegment(clues[0], True)
        #print ""
        #print "ClueSeg:",clueSeg
        #print "RowStr:",rowStr
        #print "clueSeg in rowStr:",clueSeg in rowStr
        #print ""
        while (clueSeg in rowStr and clues.count(clues[0]) == 1):
            index = rowStr.index(clueSeg, True)
            if (index != 0):
                if (rowStr[index-1] == "X" or clues[0] > index):
                    for y in range(0, index):
                        self.setSpot(rowNumber, length-rightPointer-y, "X")
                else:
                    break
            clues.pop(0)
            if (len(clues) == 0):
                break
            rowStr = rowStr[index+len(clueSeg):]
            clueSeg = self._makeSegment(clues[0])
                    
    def markFromColumnEdges(self, columnNumber):
        column = self.getColumn(columnNumber)
        clues = self.getColumnClue(columnNumber)
        length = len(column)-1

        if (column.count(0) == 0):
            return

        pointers = [0,0]

        #Reduce edges
        for x in range(0,2):
            while (column[0] != 0):
                if (column[0] == "X"):
                    column.pop(0)
                    pointers[x] += 1
                elif (column[0] == 1):
                    count = 0
                    while (column[0] == 1):
                        column.pop(0)
                        pointers[x] += 1
                        count += 1
                    if (clues[0] != count):
                        """
                        print clues[0]
                        print count
                        print self.getColumn(columnNumber)
                        print column
                        print self.getColumnClue(columnNumber)
                        print clues
                        break
                        """
                        break
                        #raise Exception("Clues not equal to count.")
                    clues.pop(0)
            column.reverse()
            clues.reverse()

        if (len(clues) == 0):
            return

        if (self._getPrintFlag()):
            print "Column:",column
            print "Clues:",clues
            print "Full Column:",self.getColumn(columnNumber)
            print "Full Clues:",self.getColumnClue(columnNumber)
        
        topPointer = pointers[0]
        columnStr = "".join(map(str,column))
        clueSeg = self._makeSegment(clues[0], True)
        while (clueSeg in columnStr and clues.count(clues[0]) == 1):
            index = columnStr.index(clueSeg, True)
            if (self._getPrintFlag()):
                print ""
                print "ClueSeg:",clueSeg
                print "ColumnStr:",columnStr
                print "Pointer:",topPointer
                print "Clues[0]:",clues[0]
                print "Index:",index
                print (columnStr[index-1] == "X" or clues[0] > index)
            if (index != 0):
                if (columnStr[index-1] == "X" or clues[0] > index):
                    for x in range(0, index):
                        self.setSpot(topPointer+x, columnNumber, "X")
                else:
                    break
            clues.pop(0)
            if (len(clues) == 0):
                break
            columnStr = columnStr[index+len(clueSeg):]
            clueSeg = self._makeSegment(clues[0])

        column.reverse()
        clues.reverse()

        if (len(clues) == 0):
            return
        
        bottomPointer = pointers[1]
        columnStr = "".join(map(str,column))
        clueSeg = self._makeSegment(clues[0], True)
        while (clueSeg in columnStr and clues.count(clues[0]) == 1):
            index = columnStr.index(clueSeg, True)
            if (index != 0):
                if (columnStr[index-1] == "X" or clues[0] > index):
                    for x in range(0, index):
                        self.setSpot(length-bottomPointer-x,columnNumber, "X")
                else:
                    break
            clues.pop(0)
            if (len(clues) == 0):
                break
            columnStr = columnStr[index+len(clueSeg):]
            clueSeg = self._makeSegment(clues[0])

    def markOffRowImpossible(self, rowNumber):
        row = self.getRow(rowNumber)
        clues = self.getRowClue(rowNumber)
        length = len(row)

        if (row.count(0) == 0):
            return

        pointers = [0,0]

        #Reduce edges
        for i in range(0,2):
            while (len(row) > 0 and row.count(0) != 0 and row[0] != 0):
                if (row[0] == "X"):
                    row.pop(0)
                    pointers[i] += 1
                elif (row[0] == 1):
                    count = 0
                    while (row[0] == 1):
                        row.pop(0)
                        pointers[i] += 1
                        count += 1
                    if (clues[0] != count):
                        #print ""
                        #print "clues[0] - count:",clues[0] - count
                        for y in range(0, clues[0] - count):
                            if (i == 0):
                                row.pop(0)
                                self.setSpot(rowNumber, pointers[i]+y, 1)
                            elif (i == 1):
                                row.pop(0)
                                self.setSpot(rowNumber, length-pointers[i]-y, 1)
                        pointers[i] += (clues[0] - count)
                        #print clues[0]
                        #print count
                        #print self.getRow(rowNumber)
                        #print row
                        #print self.getRowClue(rowNumber)
                        #print clues
                        #break
                        #raise Exception("Clues not equal to count.")
                    clues.pop(0)
            row.reverse()
            clues.reverse()
        #print row
        #print clues

        leftPointer = pointers[0]
        rightPointer = pointers[1]

        if (row.count(0) > self._getMaxPermSize()):
            if (self._getPrintFlag()):
                print "Skipping permutations because of size."
            return

        if (self._getPrintFlag()):
            print "Starting generation.."
            print "Full Row: ",self.getRow(rowNumber)
            print "Row: ",row
            print "Full Clues: ",self.getRowClue(rowNumber)
            print "Clues: ",clues
        possible = self._generatePossibleSegments(row, clues)
        if (self._getPrintFlag()):
            print "Finished generation..\n"
            print "Number Possible:",len(possible)
            print "Possible:"
            for p in possible:
                print "\t",p
            print ""
            
        changes = []
        for x in range(0, len(row)):
            changes.append("X")

        for seg in possible:
            for x in range(0, len(row)):
                if (changes[x] == "X" and seg[x] == 1):
                    changes[x] = 1
                if (changes[x] == 1 and seg[x] == 0):
                    changes[x] = 0
        for seg in possible:
            for x in range(0, len(row)):
                if (changes[x] == "X" and seg[x] == 1):
                    changes[x] = 1
                if (changes[x] == 1 and seg[x] == 0):
                    changes[x] = 0

        if (self._getPrintFlag()):
            print "Row:\t",row
            print "Changes:",changes
            print "LeftPointer:",leftPointer
            #print row
            #print changes
        for y in range(0, len(changes)):
            if (changes[y] == 0):
                continue
            self.setSpot(rowNumber, leftPointer+y, changes[y])

    def markOffColumnImpossible(self, columnNumber):
        column = self.getColumn(columnNumber)
        clues = self.getColumnClue(columnNumber)
        length = len(column)

        if (column.count(0) == 0):
            return

        pointers = [0,0]

        #Reduce edges
        for i in range(0,2):
            while (len(column) > 0 and column.count(0) != 0 and column[0] != 0):
                if (column[0] == "X"):
                    column.pop(0)
                    pointers[i] += 1
                elif (column[0] == 1):
                    count = 0
                    while (column[0] == 1):
                        column.pop(0)
                        pointers[i] += 1
                        count += 1
                    if (clues[0] != count):
                        #print ""
                        #print "clues[0] - count:",clues[0] - count
                        for x in range(0, clues[0] - count):
                            if (i == 0):
                                column.pop(0)
                                self.setSpot(pointers[i]+x, columnNumber, 1)
                            elif (i == 1):
                                column.pop(0)
                                self.setSpot(length-pointers[i]-x, columnNumber, 1)
                        pointers[i] += (clues[0] - count)
                        #print clues[0]
                        #print count
                        #print self.getColumn(columnNumber)
                        #print column
                        #print self.getColumnClue(columnNumber)
                        #print clues
                        #break #does this break things?
                        #raise Exception("Clues not equal to count.")
                    clues.pop(0)
            column.reverse()
            clues.reverse()
        #print column
        #print clues

        topPointer = pointers[0]
        bottomPointer = pointers[1]

        if (column.count(0) > self._getMaxPermSize()):
            if (self._getPrintFlag()):
                print "Skipping permutations because of size."
            return

        if (self._getPrintFlag()):
            print "Starting generation.."
            print "Full Column: ",self.getColumn(columnNumber)
            print "Column: ",column
            print "Full Clues: ",self.getColumnClue(columnNumber)
            print "Clues: ",clues
        possible = self._generatePossibleSegments(column, clues)
        if (self._getPrintFlag()):
            print "Finished generation..\n"
            print "Number Possible:",len(possible)
            print "Possible:",possible
            print ""
            
        changes = []
        for x in range(0, len(column)):
            changes.append("X")

        for seg in possible:
            for x in range(0, len(column)):
                if (changes[x] == "X" and seg[x] == 1):
                    changes[x] = 1
                if (changes[x] == 1 and seg[x] == 0):
                    changes[x] = 0
        for seg in possible:
            for x in range(0, len(column)):
                if (changes[x] == "X" and seg[x] == 1):
                    changes[x] = 1
                if (changes[x] == 1 and seg[x] == 0):
                    changes[x] = 0

        if (self._getPrintFlag()):
            print "Column:",column
            print "Changes:",changes
            print "TopPointer:",topPointer
        for x in range(0, len(changes)):
            if (changes[x] == 0):
                continue
            #print ""
            #print "Changes:",changes
            #print "TopPointer:",topPointer
            #print "X:",x
            #print "ColumnNumber:",columnNumber
            #print "Column:",column
            #print "ColumnNumber:",columnNumber
            #print "Full Column:", self.getColumn(columnNumber)
            #print "Clues:",self.getColumnClue(columnNumber)
            self.setSpot(topPointer+x, columnNumber, changes[x])
        
    def solve(self, prnt = False):
        impossibleMarked = False
        passes = 1
        if (prnt):
            print "Starting solve."
        while (not self.isSolved()):
            if (prnt):
                print ""
                print self
                print ""
            #print passes
            passes += 1
            if (self.isSolved()):
                break
            copy = self._copy()
            for x in range(0, self.getNumRows()):
                if (self._getPrintFlag()):
                    print ""
                    print "Input Row Common: #" + str(x)
                self.inputRowCommon(x)
                if (self._getPrintFlag()):
                    print ""
                    print "Mark From Row Edges: #" + str(x)
                self.markFromRowEdges(x)
            for y in range(0, self.getNumColumns()):
                if (self._getPrintFlag()):
                    print ""
                    print "Input Column Common: #" + str(y)
                self.inputColumnCommon(y)
                if (self._getPrintFlag()):
                    print ""
                    print "Mark From Column Edges: #" + str(y)
                self.markFromColumnEdges(y)
            for x in range(0, self.getNumRows()):
                if (self._getPrintFlag()):
                    print ""
                    print "Mark Row Impossible: #" + str(x)
                self.markOffRowImpossible(x)
            for y in range(0, self.getNumColumns()):
                if (self._getPrintFlag()):
                    print ""
                    print "Mark Column Impossible: #" + str(y)
                self.markOffColumnImpossible(y)
            if (self.equal(copy)):
                if (self._getMaxPermSize() > self.getNumRows()):
                    break
                elif (self._getMaxPermSize() > self.getNumColumns()):
                    break
                else:
                    self._setMaxPermSize(self._getMaxPermSize()+1)
            
