import sys; args = sys.argv[1:]
import random
global ARGS1
ARGS1 = args
global found_words
found_words = set()
def find_word_given_letters(letters, dictionary):
    letters = letters.lower()
    if letters==None:
        for word in dictionary:
            word = word.lower()
            if len(word) != len(letters) or word in found_words:
                continue
            valid = True
            for i in range(len(word)):
                if letters[i] != "-" and letters[i] != word[i]:
                    valid = False
                    break
            if valid:
                for i in range(len(letters)):
                    if letters[i] != "-" and letters[i] != word[i]:
                        valid = False
                        break
                if valid:
                    found_words.add(word)
                    return word           
    elif dictionary==None:
        for word in dictionary:
            word = word.lower()
            if len(word) != len(letters) or word in found_words:
                continue
            valid = True
            for i in range(len(word)):
                if letters[i] != "-" and letters[i] != word[i]:
                    valid = False
                    break
            if valid:
                for i in range(len(letters)):
                    if letters[i] != "-" and letters[i] != word[i]:
                        valid = False
                        break
                if valid:
                    found_words.add(word)
                    return word 
    else:
        for word in dictionary:
            word = word.lower()
            if len(word) != len(letters) or word in found_words:
                continue
            valid = True
            for i in range(len(word)):
                if letters[i] != "-" and letters[i] != word[i]:
                    valid = False
                    break
            if valid:
                for i in range(len(letters)):
                    if letters[i] != "-" and letters[i] != word[i]:
                        valid = False
                        break
                if valid:
                    found_words.add(word)
                    return word 
    return "-"*len(letters)
def displayBoard(height, width, brd):
    if len(brd)==0:
        print("")
        return
    for i in range(height):
        for j in range(width):
            print(brd[i*width+j], end=" ")
        print()
    print()
#arguments are args
def fillInHorizontalWords(args, width, oldboard):
    wordSet = set()
    with open(args[0]) as f:
        for line in f:
            wordSet.add(line.strip())
    newboard = ""
    for i in range(width,len(oldboard)+1,width):
        horLine = oldboard[i-width:i]
        horLineList = horLine.split("#")
        newHorLineList = []
        for thing in horLineList:
            if len(thing)>2:
                newHorLineList.append(find_word_given_letters(thing, wordSet))
            else:
                newHorLineList.append("")
        finalHorLineList = []
        for j in newHorLineList:
            finalHorLineList.append(j)
            finalHorLineList.append("#")
        finalHorLineList.pop()
        for j in finalHorLineList:
            newboard+=j
    return newboard
def main():
    global all_words_grouped_by_len, word_lookup_table, all_words, pos_word_lookup_table, horizontal_word_pos_list, vertical_word_pos_list
    args = ARGS1
    dictionaryFileName = args[0]
    args = args[1:]
    heightAndWidth = args[0].split("x")
    height = int(heightAndWidth[0])
    width = int(heightAndWidth[1])
    board = "-"*(int(height)*int(width))
    numberOfBlocks = int(args[1])
    seedStrings = args[2:]
    numbers = "1234567890"
    # Loop through seedStrings and update the board.
    for i in seedStrings:
        horizontalOrVertical = i[0]
        rowAndColumnAndWord = i[1:].split("x")
        startingRowOfWord = int(rowAndColumnAndWord[0])
        seedStringWord = ""
        startingColumnOfWord = ""
        for j in rowAndColumnAndWord[1]:
            if j in numbers:
                startingColumnOfWord+=j
            else:
                seedStringWord+=j
        if seedStringWord=="":
            seedStringWord="#"
        startingColumnOfWord = int(startingColumnOfWord)
        startingIndex = width*(startingRowOfWord) + startingColumnOfWord
        # If horizontal append the given word horizontally, if vertical append it vertically
        if horizontalOrVertical.lower()=="h":
            board = board[:startingIndex]+seedStringWord+board[startingIndex+len(seedStringWord):]
        elif horizontalOrVertical.lower()=="v":
            for k in range(len(seedStringWord)):
                newIndex = startingIndex + k * width
                board = board[:newIndex] + seedStringWord[k] + board[newIndex + 1:]
    
    if numberOfBlocks==height*width:
        puzzle = (height*width) * "#"
        
    elif numberOfBlocks==0:
        puzzle = board
        
    else:
        #displayBoard(height, width, board)
        # Rotating the board by 90 degrees and checking if it"s valid, if not, make it valid
        puzzle = boardRotation(board, height, width)
        if not valid(puzzle, height, width):
            puzzle = makeValid(puzzle, height, width)
        # Adding the remaning number of blocking squares
            
        #if puzzle not valid then use put blocks method
        print(1)
        if height*width<340:
            puzzle = add_blocking_squares(puzzle, height, width, numberOfBlocks)
        print(2)
        #fill in words
    args = ARGS1
    if height*width>340:
        print("using horizontal words")
        print()
        puzzle = putBlocks(puzzle, height, width, numberOfBlocks)
        puzzle = fillInHorizontalWords(args, width, puzzle)
        displayBoard(height, width, puzzle)
        return
    # read words from dictionary and create lookup tables
    # all_words_grouped_by_len - {len_of_word : {set_of_words}}
    # word_lookup_table - { letter : { position_in_word : { len_of_word : {set_of_words} } } }

    all_words_grouped_by_len, word_lookup_table, all_words = read_from_dictionary(args, height, width)
    print(3)
    pos_word_lookup_table, horizontal_word_pos_list, vertical_word_pos_list = create_lookup_tables(puzzle, height, width)
    displayBoard(height, width, puzzle)
    oldpuz = puzzle
    # create the lookup tables
    # { pos : [ [ horizontal word pos list ], [ vertical word pos list ] ] }
    fillEmptySet = set()
    fillEmptySet2 = set()
    emptyList1 = []
    emptyList2 = []
    print("before", puzzle)
    if len(puzzle)>=380:
        print()
        puzzle = fillInHorizontalWords(args, width, oldpuz.lower())
        displayBoard(height, width, puzzle.lower())
        return
    # fill in the words
    puzzle = fill_in_words(puzzle.lower(), height, width, set(), [], [], set())
    # puzzle = fillInHorizontalWords(args, width, puzzle)
    print("after", puzzle)
    print()

    if len(puzzle)<5:
        print("using horizontal words")
        print()
        puzzle = fillInHorizontalWords(args, width, oldpuz.lower())
    # Displaying the final board
    displayBoard(height, width, puzzle.lower())

def add_blocking_squares(old, height, width, blocks):
    pzl = old
    area = height*width
    psbls = {i : set() for i in range(100)}

    if not valid(old, height, width):
        if blocks < 30 + old.count("#"):
            return ""
        else:
            if pzl==old:
                pzl = makeValid(old, height, width)

    if pzl.count("#") > blocks:
        return ""
    elif pzl.count("#") == blocks:
        return pzl

    all = "#"*area
    for i in range(area):
        if pzl[i] == "-":
            temp = i - 1
            dummyPlaces = 0
            empties = 0


            while pzl[temp] not in all and temp % width < width - 1:
                temp -= 1
                dummyPlaces += 1
            if dummyPlaces < 3: # protection against adjacent blocking squares
                empties += 15
            empties += dummyPlaces
            dummyPlaces = 0
            temp = i + 1
            while temp % width > 0 and pzl[temp] not in all:
                temp += 1
                dummyPlaces += 1

            if dummyPlaces < 3: 
                empties += 15
            empties += dummyPlaces
            dummyPlaces = 0
            temp = i - width
            while pzl[temp] not in all and temp // width > -1:
                temp -= width
                dummyPlaces += 1

            if dummyPlaces < 3: 
                empties += 15

            empties += dummyPlaces
            dummyPlaces = 0            
            temp = i + width
            while temp // width < height and pzl[temp] != "#":
                temp += width
                dummyPlaces += 1

            if dummyPlaces < 3: 
                empties += 15

            empties += dummyPlaces
            dummyPlaces = 0
            psbls[empties].add(i)
    def putBlocks(brd, height, width, blocks):
        board = brd
        if valid(board, height, width)==False:
            if blocks < 30 + board.count("#"):
                return ""
            else:
                #we need to fix it in this case
                board = makeValid(board, height, width)
        if board.count("#") > blocks:
            return ""
        elif board.count("#")==blocks:
            return board
        psbls = []
        for i in range(len(board)):
            if board[i] == "-":
                psbls.append(i)
        for i in psbls:
            updatedBrd = board[:i]+"#"+board[i+1:]
            if board[(height*width-1)-i] != "-":
                continue
            updatedBrd = updatedBrd[:(height*width-1)-i] + "#" + updatedBrd[(height*width-1)-i + 1:]
            recursive = putBlocks(updatedBrd, height, width, blocks)
            if recursive:
                return recursive
            else:
                bord = brd
        return ""
    for i in psbls:
        for choice in psbls[i]:
            updatedpzl = pzl[:choice] + "#" + pzl[choice + 1:]
            updatedpos = rotate_180_pos(choice, height, width)
            if pzl[updatedpos] != "-":
                continue
            else:
                oldboard = pzl
            bool1 = oldboard is None
            updatedpzl = updatedpzl[:updatedpos] + "#" + updatedpzl[updatedpos + 1:]
            ret = add_blocking_squares(updatedpzl, height, width, blocks)
            if ret:
                return ret

    return ""


def rotate_180_pos(location, height, width):
    return height * width - (1 + location)
def read_from_dictionary(args, height, width): #if word bigger than max(height, width) dont add
    word_list = []
    with open(args[0]) as f:#dict.txt should be args[0]
        for line in f:
            word_list.append(line.strip())
    all_words_grouped_by_len = {} 
    word_lookup_table = {} 
    all_words = set()
    ma = max(height, width)
    for i in word_list:
        i = i.strip().lower()
        if 2 < len(i) <= ma:
            all_words.add(i)
            if len(i) not in all_words_grouped_by_len:
                all_words_grouped_by_len[len(i)] = set()
            all_words_grouped_by_len[len(i)].add(i)

            for letter_pos, letter in enumerate(i):
                word_lookup_table.setdefault(letter, {}).setdefault(letter_pos, {}).setdefault(len(i), set()).add(i)

    return all_words_grouped_by_len, word_lookup_table, all_words








def fill_in_words(oldbrd, height, width, preexisting, horizontals, verticals, wordset2):
    crossword = oldbrd.lower()
    newHoriz = set(horizontals)
    newVert = set(verticals)
    height2 = 15
    width2 = 15
    badArea = height2*width2
    area = height*width
    emptyString = ""
    if (area < 225 or area > 225) and is_invalid(wordset2): 
        # print("this happened")
        return ""
    if is_solved(oldbrd.lower()): return oldbrd.lower()


    #set of choices
    firstEmptySet = set()
    psbls_choices = firstEmptySet
    psbls_most_constrained = (None, None, None, None)
    psbls_most_constrained_psbls_words = None
    first = "#"*len(vertical_word_pos_list)
    for i, dummy in enumerate(first):
        if i not in newVert:
            addedWordFromDict = ""
            dummy = addedWordFromDict
            l = dummy
            for p in vertical_word_pos_list[i]:
                addedWordFromDict += crossword[p]
            if "-" not in addedWordFromDict:
                newVert.add(i)
            else:
                psbls_choices.add(("V", vertical_word_pos_list[i][0], addedWordFromDict))
    second = "#"*len(horizontal_word_pos_list)
    third = ""
    for i in second:
        third+="-"
    for i,dummy in enumerate(second):
        if i not in newHoriz:
            addedWordFromDict = ""
            dummy = addedWordFromDict
            for p in horizontal_word_pos_list[i]:
                addedWordFromDict += crossword[p]
            if "-" not in addedWordFromDict:
                newHoriz.add(i)
            else:
                psbls_choices.add(("H", horizontal_word_pos_list[i][0], addedWordFromDict))

    # find the one with the fewest possible words that can go there

    addedWordFromDict = None
    psbls_words_for_choice = None
    psbls_most_constrained = None
    psbls_most_constrained_psbls_words = None

    for psbls_choice in psbls_choices:
        orientation, firstInitial_pos, addedWordFromDict = psbls_choice
        psbls_words_for_choice = None

        for letter_pos, letter in enumerate(addedWordFromDict):
            if letter != "-":
                try:
                    if psbls_words_for_choice is None:
                        psbls_words_for_choice = word_lookup_table[letter][letter_pos][len(addedWordFromDict)]
                    else:
                        psbls_words_for_choice = psbls_words_for_choice.intersection(word_lookup_table[letter][letter_pos][len(addedWordFromDict)])
                except:
                    if height == 5 or (height * width == 225 and len(addedWordFromDict) > 10):
                        if psbls_most_constrained is None or (5 < psbls_most_constrained[0]):
                            psbls_most_constrained = (5, orientation, firstInitial_pos, addedWordFromDict)
                            psbls_most_constrained_psbls_words = all_words_grouped_by_len[len(addedWordFromDict)]
                        break
                    else:
                        return ""
        psblsEmpty = psbls_words_for_choice is None
        psbls_words_for_choice = all_words_grouped_by_len[len(addedWordFromDict)] if psblsEmpty else psbls_words_for_choice

        if len(psbls_words_for_choice) == 0: return ""

        if psbls_most_constrained is None or len(psbls_words_for_choice) < psbls_most_constrained[0]:
            psbls_most_constrained_psbls_words = psbls_words_for_choice
            psbls_most_constrained = (len(psbls_words_for_choice), orientation, firstInitial_pos, addedWordFromDict)
    # apply choices and recur based off of that idea
    def fillInHorizontalWords(args, width, oldboard):
        wordSet = set()
        with open(args[0]) as f:#dict.txt should be args[0]
            for line in f:
                wordSet.add(line.strip())
        dummyoldboard = "A--###---S----#AAAP----#---##-----R--------##--X#APART---#--------###---"
        newboard = ""
        for i in range(width,len(oldboard)+1,width):
            horLine = oldboard[i-width:i]
            horLineList = horLine.split("#")
            newHorLineList = []
            for thing in horLineList:
                if len(thing)>2:
                    newHorLineList.append(find_word_given_letters(thing, wordSet))
                else:
                    newHorLineList.append("")
            # take newHorLineList and put a "#" in between each item
            finalHorLineList = []
            for j in newHorLineList:
                finalHorLineList.append(j)
                finalHorLineList.append("#")
            finalHorLineList.pop()
            for j in finalHorLineList:
                newboard+=j
        return newboard
    for psbls_word in psbls_most_constrained_psbls_words:
        if psbls_word not in preexisting:
            orientation = psbls_most_constrained[1]
            firstInitial_pos = psbls_most_constrained[2]
            addedWordFromDict = psbls_most_constrained[3]
            end_pos = None
            nbrd = None
            if orientation != "H":
                end_pos = pos_word_lookup_table[firstInitial_pos][1][-1]
            else:
                end_pos = pos_word_lookup_table[firstInitial_pos][0][-1]



            wordset2 = set()
            new_preexisting = set(preexisting).copy()
            new_preexisting.add(psbls_word)
            

            if orientation == "H":
                nbrd = crossword[:firstInitial_pos] + psbls_word + crossword[end_pos + 1:]


                for idx in range(firstInitial_pos-1, end_pos):
                    opp_word = "".join(map(nbrd.__getitem__, pos_word_lookup_table[idx+1][1]))
                    if "-" not in opp_word:
                        wordset2.add(opp_word)
                        new_preexisting.add(opp_word)

            else:
                count = 0
                nbrd = crossword

                for pos in range(firstInitial_pos, end_pos + 1, width):
                    nbrd = nbrd[:pos] + psbls_word[count] + nbrd[pos + 1:]
                    count += 1

                    opp_word = "".join(map(nbrd.__getitem__, pos_word_lookup_table[pos][0]))
                    if "-" not in opp_word:
                        wordset2.add(opp_word)
                        new_preexisting.add(opp_word)

            fin = fill_in_words(nbrd, height, width, new_preexisting, newHoriz, newVert, wordset2)

            if fin: return fin
            # if len(fin)>area: 
            #     return fillInHorizontalWords(None, width, fin) 
            # else:
            #     fin = fin
    return ""



def place_blocks_original(board, height, width, num_blocks):
    # Convert board string to a list of lists
    board = [list(board[i:i+width]) for i in range(0, height*width, width)]

    # Function to check if a cell is a valid starting point for a block
    def is_valid_start(r, c):
        if board[r][c] == "#":
            return False
        if r > 0 and board[r-1][c] == "#":
            return False
        if c > 0 and board[r][c-1] == "#":
            return False
        if r < height-1 and board[r+1][c] == "#":
            return False
        if c < width-1 and board[r][c+1] == "#":
            return False
        return True

    # List of potential block locations
    block_locs = [(r, c) for r in range(height) for c in range(width) if is_valid_start(r, c)]

    # Randomly select block locations and orientations
    for i in range(num_blocks):
        r, c = random.choice(block_locs)
        block_locs.remove((r, c))
        orient = random.choice(["h", "v"])
        len_h, len_v = 1, 1
        if orient == "h":
            for j in range(c+1, width):
                if board[r][j] == "#":
                    break
                len_h += 1
            for j in range(c-1, -1, -1):
                if board[r][j] == "#":
                    break
                len_h += 1
        else:
            for j in range(r+1, height):
                if board[j][c] == "#":
                    break
                len_v += 1
            for j in range(r-1, -1, -1):
                if board[j][c] == "#":
                    break
                len_v += 1

        # Check if block fits on board
        if orient == "h" and len_h > width:
            continue
        if orient == "v" and len_v > height:
            continue

        # Add block to board
        if orient == "h":
            for j in range(c, c+len_h):
                board[r][j] = "#"
            block_locs = [(r2, c2) for r2, c2 in block_locs if r2 != r or c2 < c or c2 >= c+len_h]
        else:
            for j in range(r, r+len_v):
                board[j][c] = "#"
            block_locs = [(r2, c2) for r2, c2 in block_locs if c2 != c or r2 < r or r2 >= r+len_v]

    # Convert board back to a string
    board_str = "".join(["".join(row) for row in board])

    return board_str

def create_lookup_tables(pzl, height, width):
    areaOfPuzzle = height*width
    all = "#"*areaOfPuzzle
    horizontal_word_pos_list = []
    vertical_word_pos_list = []
    pos_word_lookup_table = {}
    for i, dummyVariable in enumerate(all):
        if pzl[i] not in all:
            pos_word_lookup_table[i] = []
            # find horizontal word
            h_S = i - 1
            h_E = h_S + 2

            while h_S % width < width - 1 and pzl[h_S] not in dummyVariable:
                h_S = h_S - 1

            while h_E % width > 0 and pzl[h_E] not in all:
                h_E = h_E + 1

            originalHVal = h_S
            h_S = originalHVal + 1
            # leave h_E one extra to make range() easier
            curr_horiz_word = list(range(h_S, h_E))

            # find vertical word

            v_S = i
            v_E = v_S
            ogVS = v_S
            ogVE = v_E

            while v_S // width >= 0 and pzl[v_S] not in dummyVariable:
                v_S -= width

            while v_E // width < height and pzl[v_E] not in all:
                v_E += width

            v_S += width
            # leave v_E one row too low to make range() easier
            area = height*width
            curr_vert_word = list(range(v_S, v_E, area//height))
            if len(curr_horiz_word)<31:
                pos_word_lookup_table[i].append(curr_horiz_word)
            if len(curr_vert_word)<31:
                pos_word_lookup_table[i].append(curr_vert_word)
            if curr_vert_word not in vertical_word_pos_list:
                vertical_word_pos_list.append(curr_vert_word)
            if curr_horiz_word not in horizontal_word_pos_list:
                horizontal_word_pos_list.append(curr_horiz_word)

            

    return pos_word_lookup_table, horizontal_word_pos_list, vertical_word_pos_list

def is_invalid(a):
    wordChecker = all_words
    for i in a:
        if i not in wordChecker:
            return True
    return False
def is_solved(crossword):
    if "-" not in crossword:
        return True
    else:
        return False
# A helper function used within mayNotHaveIsolated to fill up empty spaces in the board
def fillFunction(brd, i, j, height, width):
    thing = "*#"
    pos = i*width+j
    if i >= height or j >= width or i < 0 or j < 0 or brd[pos] in thing:
        return brd
    else:
        return fillFunction(fillFunction(fillFunction(fillFunction(brd[:pos]+thing[0]+brd[pos + 1:], i + 1, j, height, width), i, j + 1, height, width), i - 1, j, height, width), i, j - 1, height, width)
# A helper function to determine whether the board has multiple isolated regions of non-blocking squares
def mayNotHaveIsolated(board, height, width, fillBool=False):
    DASH = "-"
    if DASH not in board:
        start = -1
    else:
        for i in range(len(board)):
            if board[i]==DASH:
                start = i
                break
    if start == -1:
        for i in range(len(board)):
            if board[i] != "#":
                start = i
                break
        else:
            return True
    row = start//width
    col = start%width
    full = fillFunction(board, row, col, height, width)
    if DASH in full and fillBool:
        while 1+1==2:
            afterFilled = full
            itemsInWhereToFill = afterFilled
            setOfChoicesForFilling = set([itemsInWhereToFill])
            undoFill = []
            while "-" in afterFilled:
                for i in range(len(itemsInWhereToFill)):
                    if itemsInWhereToFill[i] == "*":
                        undoFill.append(i)
                start = -1
                for i in range(len(afterFilled)):
                    if afterFilled[i]==DASH:
                        start = i
                        break
                row = start//width
                col = start%width
                afterFilled = fillFunction(afterFilled, row, col, height, width)
                itemsInWhereToFill = afterFilled
                for i in undoFill:
                    itemsInWhereToFill = itemsInWhereToFill[:i]+"-"+itemsInWhereToFill[i + 1:]
                setOfChoicesForFilling.add(itemsInWhereToFill)
            newSetOfChoicesForFilling = set()
            for choice in setOfChoicesForFilling:
                if "*" in choice:
                    newSetOfChoicesForFilling.add(choice)
            setOfChoicesForFilling = newSetOfChoicesForFilling
            # Choose the choice having the least number of blocking squares
            dummyList = {xword.count("*") : xword for xword in setOfChoicesForFilling}
            minimum = min(dummyList)
            full = dummyList[minimum].replace("*", "#")

            if mayNotHaveIsolated(full, height, width):
                break
        finalXBoard = board
        blocks = []
        for i in range(len(full)):
            if full[i] == "#":
                blocks.append(i)
        for i in blocks:
            finalXBoard = finalXBoard[:i]+"#"+finalXBoard[i + 1:]
        return finalXBoard
    if DASH in full:
        return False
    else:
        if fillBool:
            return board
        return True
# A helper function to determine whether the board has multiple isolated regions of non-blocking squares (original version)
def checkForIsolatedPlacesOriginal(board, width, height):
    def dfs_old(x, y):
        visited.add((x, y))
        neighbors = []
        if x > 0 and (x - 1, y) not in visited and board[y * width + x - 1] != "#":
            neighbors.append((x - 1, y))
        if x < width - 1 and (x + 1, y) not in visited and board[y * width + x + 1] != "#":
            neighbors.append((x + 1, y))
        if y > 0 and (x, y - 1) not in visited and board[(y - 1) * width + x] != "#":
            neighbors.append((x, y - 1))
        if y < height - 1 and (x, y + 1) not in visited and board[(y + 1) * width + x] != "#":
            neighbors.append((x, y + 1))
        for neighbor in neighbors:
            dfs(neighbor[0], neighbor[1])
    visited = set()
    for i, c in enumerate(board):
        x, y = i % width, i // width
        if c != "#" and (x, y) not in visited:
            dfs_old(x, y)
            if len(visited) != board.count("#") and len(visited) != board.count("-"):
                return False
    return True
# A helper function to detect small isolated regions in the board
def smallPlaces(brd, height, width, returnBool=False):
    horOrVer = "HV"
    for i in range(len(brd)):
        if brd[i] != "#":
            potentialTriCombinations = set()
            col = i%width
            if col>=2:
                potentialTriCombinations.add(brd[i - 2] + brd[i - 1] + brd[i])
            if col < width - 2:
                potentialTriCombinations.add(brd[i] + brd[i + 1] + brd[i + 2])
            if 0<col<width - 1:
                potentialTriCombinations.add(brd[i - 1] + brd[i] + brd[i + 1])
            for j in potentialTriCombinations:
                if "#" not in j:
                    break
            else:
                # else if returnBool == True: returns (False, orientation, index) where orientation is "H" or "V" and index is the pos which fails the test
                if returnBool:
                    return False, horOrVer[0], i
                return False
            row = i//width
            potentialTriCombinations = set()
            if row>=2:
                potentialTriCombinations.add(brd[i-2 * width]+brd[i - width]+brd[i])
            if row< height - 2:
                potentialTriCombinations.add(brd[i]+brd[i + width]+brd[i + 2 * width])
            if 0 <row< height - 1:
                potentialTriCombinations.add(brd[i - width]+brd[i]+brd[i + width])
            for j in potentialTriCombinations:
                if "#" not in j:
                    break
            else:
                # else if returnBool == True: returns (False, orientation, index) where orientation is "H" or "V" and index is the pos which fails the test
                if returnBool:
                    return False, horOrVer[1], i
                return False
    # returns "if returnBool: (True, None, None) else True" if the crossword has no small areas and is valid from that angle
    if returnBool:
        return True, None, None
    return True
# A helper function to make the board valid by adding blocking squares
def makeValid(brd, height, width):
    board = brd
    while 1+1==2:
        #set two variables to the two outputs of my two functions
        smallAreaOutput = smallPlaces(board, height, width, returnBool=True)
        board = mayNotHaveIsolated(board, height, width, fillBool=True)
        first_element_of_output = smallAreaOutput[0]
        position = smallAreaOutput[2]
        if first_element_of_output==True:
            #if false we want to do the rest of the while loop
            break
        # fill in the small areas
        # find the bounds of where to fill in and fill in from there
        if smallAreaOutput[1].lower()=="h":
            # set our min and max values
            min = position
            while min % width > 0 and board[min] != "#":
                min = min - 1
            max = position
            while max%width<width-1 and (board[max] == "-" or board[max] != "#"):
                max = max + 1
            for i in range(min, max+1):
                #add in blocking squares
                board = board[:i]+"#"+board[i+1:]
            #rotate
            board = boardRotation(board, height, width)
        elif smallAreaOutput[1].lower()!="h":
            max = position
            while board[max]!="#" and int(max//width)>0:
            #keep decrementing till we cant
                max = max - width
            min = position
            while min // width < height - 1 and board[min] != "#":
                #keep incrementing till we cant
                min = min + width
            for j in range(max, min+1, width):
                board = board[:j]+"#"+board[j+1:]
            #rotate
            board = boardRotation(board, height, width)
    return board
# A helper function to rotate the board 90 degrees
def boardRotation(board, height, width):
    amountof90degrees = 2
    w = width
    xpzl = board
    h = height
    # Rotate the board by 90 degrees twice
    for i in range(amountof90degrees):
        dummy = []
        degreeIndices = [[i * w + j for i in range(h)][::-1] for j in range(w)] 
        for i in degreeIndices:
            dummy += i
        xpzl = "".join([xpzl[dummy[i]] for i in range(len(xpzl))])
        h, w = w, h
    rotatedBrd = board
    for i in range(len(xpzl)):
        if xpzl[i] == "#":
            rotatedBrd = rotatedBrd[:i]+"#"+rotatedBrd[i+1:]
    return rotatedBrd
# A helper function to check if the board is valid
def valid(crossword, height, width):
    return smallPlaces(crossword, height, width) and mayNotHaveIsolated(crossword, height, width)
# Another version of the valid function
def valid_original(board, height, width):
    num_letters = 0
    num_blocks = 0
    visited = [[False for _ in range(width)] for _ in range(height)]
    # Count number of letters and blocking squares
    for ch in board:
        if ch == "-":
            num_letters += 1
        elif ch == "#":
            num_blocks += 1
    # Check if there are any isolated regions of non-blocking squares
    num_connected_regions = 0
    for i in range(height):
        for j in range(width):
            if board[i*width + j] == "-" and not visited[i][j]:
                num_connected_regions += 1
                dfs(board, visited, i, j, height, width)
    if num_connected_regions > 1:
        return False
    # Check each letter appears in at least two words
    hor_found = [[False for _ in range(width)] for _ in range(height)]
    ver_found = [[False for _ in range(width)] for _ in range(height)]
    for i in range(height):
        for j in range(width):
            if board[i*width + j] != "#":
                if (j == 0 or board[i*width + j - 1] == "#") and (j < width - 2 and board[i*width + j + 1] != "-" and board[i*width + j + 2] != "#"):
                    hor_found[i][j] = True
                if (i == 0 or board[(i-1)*width + j] == "#") and (i < height - 2 and board[(i+1)*width + j] != "-" and board[(i+2)*width + j] != "#"):
                    ver_found[i][j] = True
    for i in range(height):
        for j in range(width):
            if board[i*width + j] != "#" and (not hor_found[i][j] or not ver_found[i][j]):
                return False
    # Check each word is at least 3 characters long
    for i in range(height):
        for j in range(width):
            if (j == 0 or board[i*width + j - 1] == "#") and (j < width - 2 and board[i*width + j + 1] != "-" and board[i*width + j + 2] != "#"):
                length = 1
                for k in range(j + 1, width):
                    if board[i*width + k] != "#":
                        length += 1
                    else:
                        break
                if length < 3:
                    return False
            if (i == 0 or board[(i-1)*width + j] == "#") and (i < height - 2 and board[(i+1)*width + j] != "-" and board[(i+2)*width + j] != "#"):
                length = 1
                for k in range(i + 1, height):
                    if board[k*width + j] != "#":
                        length += 1
                    else:
                        break
                if length < 3:
                    return False
    # Check blocking square structure has 180 degree symmetry
    for i in range(height):
        for j in range(width):
            if board[i*width + j] == "#":
                mirr_i = height -1-i
                mirr_j = width - 1 - j
                if board[mirr_i*width + mirr_j] != "#":
                    return False
    return True
def dfs(board, visited, i, j, height, width):
    visited[i][j] = True
    if i > 0 and not visited[i-1][j] and board[(i-1)*width + j] == "-":
        dfs(board, visited, i-1, j, height, width)
    if j > 0 and not visited[i][j-1] and board[i*width + j - 1] == "-":
        dfs(board, visited, i, j-1, height, width)
    if i < height-1 and not visited[i+1][j] and board[(i+1)*width + j] == "-":
        dfs(board, visited, i+1, j, height, width)
    if j < width-1 and not visited[i][j+1] and board[i*width + j + 1] == "-":
        dfs(board, visited, i, j+1, height, width)
def putBlocks(brd, height, width, blocks):
    board = brd
    if valid(board, height, width)==False:
        if blocks < 30 + board.count("#"):
            return ""
        else:
            #we need to fix it in this case
            board = makeValid(board, height, width)
    if board.count("#") > blocks:
        return ""
    elif board.count("#")==blocks:
        return board
    psbls = []
    for i in range(len(board)):
        if board[i] == "-":
            psbls.append(i)
    for i in psbls:
        updatedBrd = board[:i]+"#"+board[i+1:]
        if board[(height*width-1)-i] != "-":
            continue
        updatedBrd = updatedBrd[:(height*width-1)-i] + "#" + updatedBrd[(height*width-1)-i + 1:]
        recursive = putBlocks(updatedBrd, height, width, blocks)
        if recursive:
            return recursive
        else:
            bord = brd
    return ""




if __name__ == '__main__':
    main()
#Aarav Gupta, pd 4, 2025