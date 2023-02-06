#!/usr/bin/env python3

import json 
import random
import sys
import copy
import os
from getpass import getpass
from alive_progress import alive_bar
from str2bool import str2bool
from string import ascii_letters,digits,punctuation
from difflib import SequenceMatcher

def prompt(query):
    sys.stdout.write("%s [y/N]: " % query)
    val = input()
    try:
        answer = str2bool(val)
    except ValueError:
        sys.stdout.write("Please answer with y/n")
        return prompt(query)
    return answer

numCandidates = 20
candidates = []
isRoot = prompt("Is this password being created for a root user?")
minimumLength = 16
maximumLength = 19
nWords = 3
if isRoot:
    maximumLength = 24
    nWords = 4

def pass_phrase(num_words):
    #Choose 4 random, unique letters from the alphabet
    alphabet = ascii_letters[0:26]
    kLetters = random.sample(alphabet,k=num_words)
    match = SequenceMatcher(None,alphabet,"".join(kLetters)).find_longest_match()

    #Ensure that chosen letters aren't in alphabetical order and don't contain ordered substrings
    while match.size > 2:
        kLetters = random.sample(alphabet,k=num_words)
        match = SequenceMatcher(None,alphabet,"".join(kLetters)).find_longest_match()

    kWords = []

    #For each letter, randomly select a word starting with that letter from the corresponding JSON file
    for letter in kLetters:
        fname = letter + ".json"
        fh = open(fname)
        wordlist = json.load(fh)
        word = random.choice(list(wordlist.keys()))
        fh.close()
        #Remove hyphens
        word = word.replace('-',' ')
        wordSplit = word.split()
        #If the word is a phrase (contains spaces), only use the first word of the phrase
        if len(wordSplit) > 1: 
            word = wordSplit[0]

        #Capitalize first letter and append to list of three words
        kWords.append(word.capitalize())
    if len("".join(kWords)) >= maximumLength:
        return pass_phrase(num_words) 
    return kWords

def add_symbols(chosenPhrase,minimumLength,maximumLength):
    passPhrase = copy.copy(chosenPhrase)
    digitsUsed = 0
    punctuationUsed = 0
    
    phraseLength = len("".join(passPhrase))
    passLength = random.randrange(phraseLength,maximumLength)
    if passLength < minimumLength:
        passLength = random.randrange(minimumLength,maximumLength)         

    numSymbols = passLength - phraseLength
    if numSymbols < 3:
        numSymbols = 3

    insertionMethods = ['between','random','end','exchange']
    #insertionMethods = ['between','end']
    exchangeBuffer = []
    randomBuffer = []
    asciiSymbols = [digits,punctuation]
    methods = random.choices(insertionMethods,weights=[0.35, 0.1, 0.45, 0.1],k=numSymbols)
    #methods = random.choices(insertionMethods,k=numSymbols)
    for n in range(numSymbols):
        if n == numSymbols -1:
            if digitsUsed == 0:
                symbolType = digits
            elif punctuationUsed == 0:
                symbolType = punctuation
        else:
            symbolType = random.choice(asciiSymbols)
        
        if symbolType == digits:
            digitsUsed+=1
        
        elif symbolType == punctuation:
            punctuationUsed+=1

        symbol = random.choice(symbolType)

        method = methods[n]
        if method == 'between':
            idx = random.randrange(1,len(passPhrase))
            passPhrase.insert(idx,symbol)
        
        elif method == 'end':
            passPhrase.append(symbol)

        elif method == 'random':
            randomBuffer.append(symbol)

        elif method == 'exchange':
            exchangeBuffer.append(symbol)

    passwordBuffer = list("".join(passPhrase))

    if exchangeBuffer:
        for symbol in exchangeBuffer:
            idx = random.randrange(1,len(passwordBuffer))
            passwordBuffer[idx] = symbol

    if randomBuffer:
        for symbol in randomBuffer:
            idx = random.randrange(1,len(passwordBuffer))
            passwordBuffer.insert(idx,symbol)

    password = "".join(passwordBuffer)

    if len(password) < minimumLength:
        return(add_symbols(passPhrase,minimumLength,maximumLength))

    return password

def generate_phrases():
    print("Generating secret phrases...")
    with alive_bar(numCandidates) as bar:
        for i in range(numCandidates):
            secretPhrase = pass_phrase(nWords)
            candidates.append(secretPhrase)
            bar()

    print("\n")

    for i,candidate in enumerate(candidates,start=1):
        print(f'[{i}] '+"".join(candidate))

    query = "Please select a secret phrase from the list provided, or enter 0 to generate a new list: "
    error_mesg = "Invalid input! Please select a valid option from the list provided: "
    chosenPhrase = prompt_selection(query,error_mesg,'generate_phrases()')
    candidates.clear()
    return chosenPhrase

def prompt_selection(query,error_mesg,func):
    val = int(input(query))
    try:
        if val == 0:
            candidates.clear()
            return eval(func)
        else:
            answer = candidates[val-1]
    except ValueError:
        sys.stdout.write(error_mesg)
        return prompt_selection(query,error_mesg)
    return answer


def generate_passwords(chosenPhrase,minimumLength,maximumLength):
    print("Generating secure passwords...")
    for i in range(numCandidates):
        passwordVariation = add_symbols(chosenPhrase,minimumLength,maximumLength)
        candidates.append(passwordVariation)
        print(passwordVariation)

    print("\n")

    for i,candidate in enumerate(candidates,start=1):
        print(f'[{i}] {candidate}')

    query = "Please select a password from the options provided or enter 0 to generate a new list: "
    error_mesg = "Invalid input! Please select a valid option from the list provided: "
    chosenPassword = prompt_selection(query,error_mesg,'generate_passwords(chosenPhrase,minimumLength,maximumLength)')
    return chosenPassword


def practice(error_mesg,response=None):
    passwd = getpass()
    if passwd == chosenPassword:
        if response:
            print(response)
    else:
        print(error_mesg)
        return practice(response,error_mesg)


chosenPhrase = generate_phrases()
print("".join(chosenPhrase))
print(len("".join(chosenPhrase)))
chosenPassword = generate_passwords(chosenPhrase,minimumLength,maximumLength)
print(f'Your new password is \"{chosenPassword}\". Now let\'s practice entering your new password before we finish up!')
error_mesg = "Whoops! That didn't match your the new password you selected, try again..."
firstRound = practice(error_mesg,"Good job! Now just enter your new password one more time to move to the last step.")
secondRound = practice(error_mesg)
good2go = prompt("Do you want to this new password to be applied to your system?")
if good2go and isRoot:
    os.system("sudo passwd root")
elif good2go:
    os.system("sudo passwd $USER")
else:
    print("Ok, exiting without making any changes.")
    exit()
