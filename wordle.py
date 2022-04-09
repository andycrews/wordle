#!python3

class Dictionary:
    fiveletterwords=[]
    #bigdictfile='/usr/share/dict/words'
    bigdictfile='wordledictionary'
    # words in the dictionary that I found wordle doesn't accept
    forbidden=set(['xurel','zerda','lapon','edder','heiau', 'kioea', 'ouabe','aalii','beice','blibe','yoick','zoism','zoist','writh','ville','zygal','zonar', 'acier','barie','bedin','bepen','besin','yinst','wisht','fusht','ululu','wheki','knezi','uneye','nmeme','neeze','babai','haire','twink','urled','sleer'])
    forbidden.add('plaga')
    forbidden.add('solen')
    forbidden.add('sewen')
    forbidden.add('artha')
    forbidden.add('barit')
    forbidden.add('carty')
    def LoadWords():
        if Dictionary.fiveletterwords:
            return
        f=open(Dictionary.bigdictfile)
        for line in f:
            dword=line.strip()
            if len(dword) != 5:
                continue
            if dword in Dictionary.forbidden:
                continue
            if dword[0].isupper():
                continue
            Dictionary.fiveletterwords.append(dword.lower())
        f.close()
        #WTF?
        Dictionary.fiveletterwords.append('cared')
        Dictionary.fiveletterwords.append('cares')
        Dictionary.fiveletterwords.append('rules')
        Dictionary.fiveletterwords.append('downs')
        Dictionary.fiveletterwords.append('germs')
        Dictionary.fiveletterwords.append('abuts')
        Dictionary.fiveletterwords.append('acids')
        Dictionary.fiveletterwords.append('acres')
        Dictionary.fiveletterwords.append('aeons')
        Dictionary.fiveletterwords.append('aeons')
        Dictionary.fiveletterwords.append('aides')
        Dictionary.fiveletterwords.append('alums')
        Dictionary.fiveletterwords.append('atoms')
        Dictionary.fiveletterwords.append('axles')
        Dictionary.fiveletterwords.append('avows')
        Dictionary.fiveletterwords.append('autos')
        Dictionary.fiveletterwords.append('aunts')
        Dictionary.fiveletterwords.append('backs')
        Dictionary.fiveletterwords.append('bakes')
        Dictionary.fiveletterwords.append('moxie')
        Dictionary.fiveletterwords.append('totes')
        Dictionary.fiveletterwords.append('tubes')
        Dictionary.fiveletterwords.append('tules')
        Dictionary.fiveletterwords.append('tunes')
        #for line in f:
        #    Dictionary.fiveletterwords.append(dword.lower())
        #print("%d words. removing dups" % (len(Dictionary.fiveletterwords)))
        Dictionary.fiveletterwords=set(Dictionary.fiveletterwords)
        Dictionary.fiveletterwords=list(Dictionary.fiveletterwords)
        Dictionary.fiveletterwords.sort()
        #print("%d words" % (len(Dictionary.fiveletterwords)))
        Dictionary.fiveletterwords.sort()


class Wordle:
    def __init__(self):
        # greenmatch is 0 or 1 letter per position
        self.greenmatches=[(),(),(),(),()]
        # yellowmatch is list of letters that are in use but not that position
        self.yellowmatches=[set(),set(),set(),set(),set()]
        # nomatch is list of letters not in the wordle
        self.nomatch=set()
        Dictionary.LoadWords()
        self.wordmatches=list(Dictionary.fiveletterwords)
        self.matchesutd=True # Matches Up To Date
    def AddMatch(self, matches):
        "takes list of (position, lower case letter)"
        for position, letter in matches:
            self.greenmatches[position] = letter
        if matches:
            self.matchesutd=False
    def AddYellowMatch(self, matches):
        "takes list of (position, lower case letter)"
        for position, letter in matches:
            self.yellowmatches[position].add(letter)
        if matches:
            self.matchesutd=False
    def AddNoMatch(self, matches):
        "takes list of lower case letters"
        for letter in matches:
            if letter in self.greenmatches:
                continue
            self.nomatch.add(letter)
        if matches:
            self.matchesutd=False
    def IsLegalLetter(self, letter, index, m):
        if m.ismatch():
            if letter in self.yellowmatches[index]:
                return False
        else:
            if letter == self.greenmatches[index]:
                return False
        return True
    def IsLegal(self, word, res):
        for index in range(len(res)):
            if not self.IsLegalLetter(word[index],index,res[index]):
                return False
        return True

    def WordMatches(self, word):
        index=0
        for index in range(5):
            if self.greenmatches[index]:
                if self.greenmatches[index]!=word[index]:
                    return False
            for y in self.yellowmatches[index]:
                if word[index] in y:
                    return False
        for index in range(5):
            for y in self.yellowmatches[index]:
                if y not in word:
                    return False
        if self.nomatch.intersection(word):
            return False
        return True

    def Matches(self):
        "Returns a list of possible words for the known and unknown"
        if self.matchesutd:
            return self.wordmatches
        matches=[]
        # use the previous list to find the new list
        for word in self.wordmatches:
            if self.WordMatches(word):
                matches.append(word)
        self.wordmatches=matches
        return self.wordmatches
    def __str__(self):
        matches=self.Matches()
        if len(matches)<93:
            return "%d matching words: %s" % (len(matches), matches)
        else:
            return "%d matching words" % (len(matches))

class MType:
    ism=2
    isy=1
    def __init__(self, mt):
        self.mt=mt
    def mtype(self):
        return mt
    def ismatch(self):
        return self.mt==self.ism
    def isyellow(self):
        return self.mt==self.isy
    def isnomatch(self):
        return not self.ismatch() and not self.isyellow()
    def __str__(self):
        if self.ismatch():
            return "match"
        if self.isyellow():
            return "yellow"
        return "nomatch"

class WordleResult:
    def __init__(self, wordle, word, res):
        " args are wordle, word, [myptes]"
        import copy
        self.wordle=copy.deepcopy(wordle)
        self.res=res
        index=0
        if len(res):
            for index in range(len(res)):
                l=word[index]
                m=self.res[index]
                if m.ismatch():
                    self.wordle.AddMatch([(index,l)])
                elif m.isyellow():
                    self.wordle.AddYellowMatch([(index,l)])
                else:
                    self.wordle.AddNoMatch(l)
        else:
            # assume no matches
            self.wordle.AddNoMatch(word)
    def result(self):
        return self.wordle
    def __str__(self):
        return "self.wordle is %s" % (self.wordle)



class WordleSolver:
    def __init__(self, wordle):
        self.wordle=wordle
    def GuessWords(self,words=[]):
        results=[]
        index=0
        if not words:
            # find results for 0 or 1 yellow in all words
            searchresults = [[MType(0),MType(0),MType(0),MType(0),MType(0)]]
            searchresults.append([MType(1),MType(0),MType(0),MType(0),MType(0)])
            searchresults.append([MType(0),MType(1),MType(0),MType(0),MType(0)])
            searchresults.append([MType(0),MType(0),MType(1),MType(0),MType(0)])
            searchresults.append([MType(0),MType(0),MType(0),MType(1),MType(0)])
            searchresults.append([MType(0),MType(0),MType(0),MType(0),MType(1)])
            words=Dictionary.fiveletterwords
        else:
            # find all possible result sets
            allmtypes=[MType(0),MType(1),MType(2)]
            searchresults=[]
            for m0 in allmtypes:
                for m1 in allmtypes:
                    for m2 in allmtypes:
                        for m3 in allmtypes:
                            for m4 in allmtypes:
                                searchresults.append([m0,m1,m2,m3,m4])
        # evauate a list of words. return largest possible set
        best=()
        bestword=''
        bestresult=()
        lastword='zzzz'
        for word in words:
            largest=()
            largestword=''
            largestresult=()
            if lastword[0]!=word[0]:
                print('Trying %s' % (word))
            lastword=word
            for res in searchresults:
                if not self.wordle.IsLegalLetter(word[0],0,res[0]):
                    continue
                if not self.wordle.IsLegalLetter(word[1],1,res[1]):
                    continue
                if not self.wordle.IsLegalLetter(word[2],2,res[2]):
                    continue
                if not self.wordle.IsLegalLetter(word[3],3,res[3]):
                    continue
                if not self.wordle.IsLegalLetter(word[4],4,res[4]):
                    continue
                wr=WordleResult(self.wordle,word,res)
                w=wr.result()
                if not largest or len(w.Matches())>len(largest.Matches()):
                    #print("found new largest")
                    #print(w,word,res[0],res[1],res[2],res[3],res[4])
                    largest=w
                    largestword=word
                    largestresult=res
            # pick the word that give the smallest largest
            m=largest.Matches()
            if best:
                b=best.Matches()
            if not best or len(m)<len(b):
                print("found new best: %s" % largestword)
                print(largest,largestresult[0],largestresult[1],largestresult[2],largestresult[3],largestresult[4])
                best=largest
                bestword=largestword
                bestresult=largestresult
            elif len(m)==len(b):
                print("found equal word: %s" % largestword)
                print(largest,largestresult[0],largestresult[1],largestresult[2],largestresult[3],largestresult[4])
            elif word=='lager':
                print(largest,largestresult[0],largestresult[1],largestresult[2],largestresult[3],largestresult[4])
        results.append((bestword,best,bestresult))
        return results



wordle=Wordle()
print("Total five letter words: %d" % (len(Dictionary.fiveletterwords)))
#print("Matching words: %d" % (len(wordle.Matches())))

def ShowHelp():
    print("""Commands:
1 or m: enter match 
2 or y: enter yellowmatch
3 or n: enter nomatch
4 or w: show matching words
5 or x: find best next word
""")

def ShowMain():
    print("""Select:
1. enter match, yellowmatch and nomatch data so far
2. run scenario 1
3. find best first word
""")

ShowMain()
x=input()
if x=='2':
    # hard code some scenario here for debugging it
    yellowmatch=[(3,'e')]
    wordle.AddYellowMatch(yellowmatch)
    print("adding yellowmatches: %s" % (yellowmatch))
    matches=[(2,'i')]
    wordle.AddMatch(matches)
    print("adding matches: %s" % (matches))
    nomatch='adu'
    print("adding nomatches: %s" % (nomatch))
    wordle.AddNoMatch(nomatch)
    print(wordle)

    yellowmatch=[(3,'r'),(4,'n')]
    wordle.AddYellowMatch(yellowmatch)
    print("adding yellowmatches: %s" % (yellowmatch))
    nomatch='sco'
    print("adding nomatches: %s" % (nomatch))
    wordle.AddNoMatch(nomatch)
    print(wordle)
    print(wordle.Matches())

    yellowmatch=[(0,'r'),(1,'e')]
    wordle.AddYellowMatch(yellowmatch)
    print("adding yellowmatches: %s" % (yellowmatch))
    print(wordle)
    nomatch='s'
    print("adding nomatches: %s" % (nomatch))
    wordle.AddNoMatch(nomatch)
    print(wordle)

elif x!='3':
    while True:
        ShowHelp()
        print(wordle)
        x=input()
        if x=='1' or x=='m':
            try:
                print("Enter position [0-4]")
                p=int(input())
                print("Enter letter [a-z]")
                l=input().lower()
                wordle.AddMatch([(p,l)])
            except:
                print('oops')

        if x=='2' or x=='y':
            try:
                print("Enter position [0-4]")
                p=int(input())
                print("Enter letter [a-z]")
                l=input().lower()
                wordle.AddYellowMatch([(p,l)])
            except:
                print('oops')

        if x=='3' or x=='n':
            print('Enter letter(s)')
            l=input().lower()
            wordle.AddNoMatch(l)
        if x=='5' or x=='x':
            # first guess all words. after that, pick one word to guess that might match
            ws=WordleSolver(wordle)
            bestn=len(Dictionary.fiveletterwords)+1
            best=[]
            for word,w,r in ws.GuessWords(wordle.Matches()):
                n=len(w.Matches())
                if n and n<bestn:
                    best=[(word,w,r)]
                    bestn=n
                elif n==bestn:
                    best.append((word,w,r))

            for b in best:
                (l0,l1,l2,l3,l4)=b[2]
                print("Best %d: %s,%s,(%s,%s,%s,%s,%s)" % (bestn, b[0],b[1],l0,l1,l2,l3,l4))
else:
    # find best 5 letter first word
    ws=WordleSolver(wordle)
    bestn=len(Dictionary.fiveletterwords)+1
    best=[]
    print("Generating Wordle data structures for all %d words" % len(Dictionary.fiveletterwords))
    for word,w,r in ws.GuessWords():
        n=len(w.Matches())
        if n and n<bestn:
            best=[(word,w,r)]
            bestn=n
            print("%s: %d matches" % (word, n))
        elif n==bestn:
            best.append((word,w,r))
            print("%s: %d matches" % (word, n))
        elif n*0.9 < bestn:
            print("     %s: %d matches" % (word, n))

    print("Found %d best words:" % (len(best)))
    for b in best:
        #print(b)
        #print(len(b))
        if len(b[2])==5:
            (l0,l1,l2,l3,l4)=b[2]
            print("Best %d: %s,%s,(%s,%s,%s,%s,%s)" % (bestn, b[0],b[1],l0,l1,l2,l3,l4))
            #print("%s" % (b[1].Matches()))
        else:
            print("Best %d %s,%s" %(bestn, b[0],b[1]))
