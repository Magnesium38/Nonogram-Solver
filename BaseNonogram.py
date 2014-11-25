class Nonogram:
    def __init__(self, rows, columns, rowNums, columnNums):
        self._setNumRows(rows)
        self._setNumColumns(columns)
        self._setRowClues(rowNums)
        self._setColumnClues(columnNums)
        self._array = []
        for x in range(0, self.getNumRows()):
            tmpList = []
            for y in range(0, self.getNumColumns()):
                tmpList.append(0)
            self._array.append(tmpList)
        self._setPrintFlag(False)
        self._setMaxPermSize(1)

    def __str__(self):
        rows = []
        for x in range(0, self.getNumRows()):
            # Rows are a combination of ints and strs
            # .join doesn't like ints in there
            # So use the map to make everything a string first
            rows.append(" ".join(map(str, self.getRow(x))))
        return "\n".join(rows)#.replace("0", " ")

    def _sum(self, sequence):
        #Copy sequence first to avoid issues
        s = sequence[:] #Odd copy syntax still
        while (s.count("X") > 0):
            s.remove("X")
        return sum(s)
    
    def _copy(self):
        n = Nonogram(self.getNumRows(), self.getNumColumns(),
                     self.getRowClues(), self.getColumnClues())
        array = []
        for x in range(0, self.getNumRows()):
            array.append(self.getRow(x))
        n._array = array
        return n

    def _populate(self, array):
        self._array = array[:]

    def _setPrintFlag(self, printFlag):
        self._printFlag = printFlag

    def _getPrintFlag(self):
        return self._printFlag

    def _setMaxPermSize(self, size):
        self._maxPermSize = size

    def _getMaxPermSize(self):
        return self._maxPermSize

    def _setNumRows(self, rows):
        self._numRows = rows

    def _setNumColumns(self, columns):
        self._numColumns = columns
    
    def getNumRows(self):
        return self._numRows

    def getNumColumns(self):
        return self._numColumns

    def equal(self, other):
        if (self.getNumRows() != other.getNumRows()):
            #print "Different number of rows."
            return False
        if (self.getNumColumns() != other.getNumColumns()):
            #print "Different number of columns."
            return False
        if (self.getRowClues() != other.getRowClues()):
            #print "Different row clues."
            return False
        if (self.getColumnClues() != other.getColumnClues()):
            #print "Different column clues."
            return False
        if (self._array != other._array):
            #print "Different array."
            return False
        return True

    def getSpot(self, rowNum, columnNum):
        return self._array[rowNum][columnNum]

    def setSpot(self, rowNum, columnNum, spot):
        if (rowNum < 0 or columnNum < 0):
            return
        if (rowNum < self.getNumRows() and columnNum < self.getNumColumns()):
            if (type(spot) == str and spot != "X"):
                spot = int(spot)

            if (self.getSpot(rowNum, columnNum) == spot):
                return
             
            if (self._getPrintFlag()):
                print "Row num: ",rowNum
                print "Col num: ",columnNum
                print "Set to:  ",str(spot)
                print ""
                
            if (self.getSpot(rowNum, columnNum) == 1 and spot == "X"):
                print "rowNum:",rowNum
                print "columnNum:",columnNum
                raise Exception("Attempt to overwrite 1 with X.")
            if (self.getSpot(rowNum, columnNum) == "X" and spot == 1):
                print "rowNum:",rowNum
                print "columnNum:",columnNum
                raise Exception("Attempt to overwrite X with 1.")
            self._array[rowNum][columnNum] = spot
        else:
            print "Row num: ",rowNum
            print "Col num: ",columnNum
            raise Exception("Invalid coords.")

    def _makeSegment(self, length, EndNotSpot=False):
        s = "1"
        es = "0"
        if (EndNotSpot):
            es = "X"
        seg = ""
        for x in range(0, length):
            seg += s
        return seg + es

    def getRowClues(self):
        return self._rowClues[:] #Odd syntax to force a copy

    def _setRowClues(self, rowNums):
        self._rowClues = rowNums

    def getRowClue(self, rowNumber):
        if (rowNumber < self.getNumRows()):
            return self.getRowClues()[rowNumber][:] #Odd syntax to force a copy
        else:
            raise Exception("Invalid row number.")

    def getColumnClues(self):
        return self._columnClues[:] #Odd syntax to force a copy

    def _setColumnClues(self, columnNums):
        self._columnClues = columnNums

    def getColumnClue(self, columnNumber):
        if (columnNumber < self.getColumnClues()):
            return self.getColumnClues()[columnNumber][:] #Odd syntax to force a copy
        else:
            raise Exception("Invalid column number.")

    def getRow(self, rowNumber):
        if (rowNumber < self.getNumRows()):
            l = []
            for y in range(0, self.getNumColumns()):
                l.append(self.getSpot(rowNumber, y))
            return l
        else:
            raise Exception("Invalid row number.")

    def getColumn(self, columnNumber):
        if (columnNumber < self.getNumColumns()):
            l = []
            for x in range(0, self.getNumRows()):
                l.append(self.getSpot(x, columnNumber))
            return l
        else:
            raise Exception("Invalid column number.")

    def isSolved(self):
        for x in range(0, len(self._array)):
            for y in range(0, len(self._array[x])):
                if (self._array[x][y] == 0):
                    return False
        for x in range(0, self.getNumRows()):
            row = self.getRow(x)
            clues = self.getRowClue(x)
            if (self._sum(row) > sum(clues)):
                print "Row:",row
                print "Row Number:",x
                print "Clues:",clues
                raise Exception("Too many marks in row.")
            if (self._sum(row) != sum(clues)):
                return False
        for y in range(0, self.getNumColumns()):
            column = self.getColumn(y)
            clues = self.getColumnClue(y)
            if (self._sum(column) > sum(clues)):
                print "Column:",column
                print "Column Number:",x
                print "Clues:",clues
                raise Exception("Too many marks in Column.")
            if (self._sum(column) != sum(clues)):
                return False
        return True
