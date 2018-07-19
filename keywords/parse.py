from Load import *
#all string methods used for parsing the structural template is here

def split(s):
    #this little section ensures the phrase starts with a word and not a special character
    while not s[0].isalnum():
        s = s[1:]
    words = []
    symbols = []
    word = ""
    symbol = ""
    for i in s:
        #if not a symbol, it's the end of a symbol sequence
        if i not in " \t.-,&()/;:":
            symbols.append(symbol)
            symbol = ""
            word += i
        #if not alphanumeric, a word just ended
        else:
            words.append(word)
            word = ""
            symbol += i
    #append the last word and symbol sequence
    words.append(word)
    symbols.append(symbol)
    #remove duplicates
    words = [s for s in words if s != '']
    symbols = [s for s in symbols if s != '']
    return [words, symbols]


def parseWord(s, f):
    #s is the word, f is the flag (s = standard, u = upper, l = lower)
    if f == 's':
        return s[0].upper() + s[1:].lower()
    elif f == 'u':
        return s.upper()
    elif f == 'l':
        return s.lower()


def join(w, s):
    #w is the word list, s is the symbol list
    phrase = ""
    for i in range(len(w)):
        #note this function always assume the phrase starts with a word
        phrase += w[i]
        #in case the phrase ends with a word not a symbol
        phrase += s[i] if i < len(s) else ''
    return phrase


def parsePhrase(s, i):
    #parse the flags
    s = s.split('|')
    name = s[0]
    flag = s[1]
    concat = s[2]
    #return empty if the name is empty and just the string if it's default
    if name == '':
        return ''
    phrase = globals()[name][i]
    if phrase == '':
        return ''
    if flag == 'd':
        return phrase
    #separating the phrase into words and symbol lists
    words = split(phrase)[0]
    separators = split(phrase)[1]
    #parse each word
    words = [parseWord(word, flag) for word in words]
    #then join them back together
    if concat != '':
        return concat.join(words)
    else:
        return join(words, separators)


def parseField(t, i):
    #t is template, i is index
    if len(t) == 1:
        return parsePhrase(t[0], i)
    else:
        phrases = []
        for p in t[:-1]:
            s = parsePhrase(p,i)
            if s != '':
                phrases.append(s)
        if len(t[-1]) == 1:
            return t[-1][0].join(phrases)
        else:
            return join(phrases, t[-1])
