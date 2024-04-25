##Calculating the initial state probabilities
##For each word, we take the first letter 
##If not in the dictionary, add it. If it is, increment the value.
def calculate_initial_state_probabilities(words):
    initial_state_probs = {}

    for word in words:
        first_letter = word[0]
        if first_letter not in initial_state_probs:
            initial_state_probs[first_letter] = 1
        else:
            initial_state_probs[first_letter] += 1

    ##Divide each value by the total number of words to get the probability
    total_words = len(words)
    for key in initial_state_probs:
        initial_state_probs[key] /= total_words

    return initial_state_probs


##Calculating the transition probabilities
##For each word, we look at each letter and the next letter
##If pair is not in the dictionary, add it. If it is, increment the value.
def calculate_transition_probabilities(words):
    transition_probs = {}

    for word in words:
        for i in range(len(word) - 1):
            current_letter = word[i]
            next_letter = word[i + 1]

            if current_letter not in transition_probs:
                transition_probs[current_letter] = {}
            if next_letter not in transition_probs[current_letter]:
                transition_probs[current_letter][next_letter] = 1
            else:
                transition_probs[current_letter][next_letter] += 1

    ##Divide each value by the total number of words to get the probability
    for key in transition_probs:
        ##Get the total number of transitions from the current letter
        total_transitions = sum(transition_probs[key].values())
        for key2 in transition_probs[key]:
            transition_probs[key][key2] /= total_transitions

    ## Add missing letter sequences with probability zero
    all_letters = set(''.join(words))
    for letter in all_letters:
        if letter not in transition_probs:
            transition_probs[letter] = {}
        for other_letter in all_letters:
            if other_letter not in transition_probs[letter]:
                transition_probs[letter][other_letter] = 0

    return transition_probs


##Calculating the emission probabilities
##For each word, we look at each letter and the corresponding OCR output
##If pair is not in the dictionary, add it. If it is, increment the value.
def calculate_emission_probabilities(actual_words, ocr_outputs):
    emission_probs = {}
    for i in range(len(actual_words)):
        word = actual_words[i]
        ocr_output = ocr_outputs[i]

        ##check that the word and OCR output are the same length to avoid errors
        if len(word) != len(ocr_output):
            print("Error: word and OCR output do not match in length")
            continue

        for j in range(len(word)):
            current_letter = word[j]
            ocr_letter = ocr_output[j]

            if current_letter not in emission_probs:
                emission_probs[current_letter] = {}
            if ocr_letter not in emission_probs[current_letter]:
                emission_probs[current_letter][ocr_letter] = 1
            else:
                emission_probs[current_letter][ocr_letter] += 1

    ##Divide each value by the total number of words to get the probability
    for key in emission_probs:
        total_emissions = sum(emission_probs[key].values())
        for key2 in emission_probs[key]:
            emission_probs[key][key2] /= total_emissions

    ## Add missing letter sequences with probability zero
    all_letters = set(''.join(actual_words))
    all_ocr_outputs = set(''.join(ocr_outputs))
    for letter in all_letters:
        if letter not in emission_probs:
            emission_probs[letter] = {}
        for ocr_output in all_ocr_outputs:
            if ocr_output not in emission_probs[letter]:
                emission_probs[letter][ocr_output] = 0

    return emission_probs



##Viterbi algorithm
def viterbi(ocr_reading, initial_probabilities, transition_probabilities, emission_probabilities):
    ##Initialize the dictionary for all possible letters, and the probability of the word inialized to 0
    
    currentWordsProb = {chr(letter): ["", 0] for letter in range(ord('A'), ord('Z') + 1)}

    ##Base case
    ##Probability of the first letter is the initial probability * the emission probability
    if len(ocr_reading) == 1:
        for currentLetter in currentWordsProb:
            currentWordsProb[currentLetter][0] = currentLetter
            currentWordsProb[currentLetter][1] = initial_probabilities[currentLetter] * emission_probabilities[currentLetter][ocr_reading]
        return currentWordsProb

    ##Recursive case
    previousDictionary = viterbi(ocr_reading[:-1], initial_probabilities, transition_probabilities, emission_probabilities)

    ##For each letter in the current word, find the previous letter that maximizes the probability
    ##The probability of the current letter is the probability of the previous letter * the transition probability * the emission probability
    for currentLetter in currentWordsProb:
        for previousLetter in currentWordsProb:
            probability = previousDictionary[previousLetter][1] * \
                           transition_probabilities[previousLetter][currentLetter] * \
                           emission_probabilities[currentLetter][ocr_reading[-1]]
            if probability > currentWordsProb[currentLetter][1]:
                currentWordsProb[currentLetter][0] = previousDictionary[previousLetter][0] + currentLetter
                currentWordsProb[currentLetter][1] = probability

    return currentWordsProb


def most_probable_word(dict):
    best_word = ''
    best_prob = 0
    for key in dict:
        if dict[key][1] > best_prob:
            best_word = dict[key][0]
            best_prob = dict[key][1]
    return best_word


##Read in the data, first 50,000 words are put into the training set, the rest are put into the test set
actual_words_estim = []
ocr_outputs_estim = []
actual_words_perform = []
ocr_outputs_perform = []

count = 0
with open('data_actual_words.txt', 'r') as file:
    for line in file:
        if count < 50000:
            actual_words_estim.append(line.strip())
        else:
            actual_words_perform.append(line.strip())
        count += 1

count = 0
with open('data_ocr_outputs.txt', 'r') as file:
    for line in file:
        if count < 50000:
            ocr_outputs_estim.append(line.strip())
        else:
            ocr_outputs_perform.append(line.strip())
        count += 1


##Calculate the probabilities
initial_state_probabilities = calculate_initial_state_probabilities(actual_words_estim)
transition_probabilities = calculate_transition_probabilities(actual_words_estim)
emission_probabilities = calculate_emission_probabilities(actual_words_estim, ocr_outputs_estim)


print("Initial state probabilities:")
sorted_keys = sorted(initial_state_probabilities.keys())
for key in sorted_keys:
    print(key, initial_state_probabilities[key])
print()

print("Transition probabilities:")
for key in sorted_keys:
    print(key, sorted(transition_probabilities[key].items()))
    print() 

print("Emission probabilities:")
for key in sorted_keys:
    print(key, sorted(emission_probabilities[key].items()))
    print()



##Test the performance of the algorithm
##For each word, find the most probable word and compare it to the actual word
##If they are different, print the word and the most probable word
mismatched = 0
total_letters = 0
print_if_true= False
for i in range(len(ocr_outputs_perform)):
    word = ocr_outputs_perform[i]
    actual_word = actual_words_perform[i]
    total_letters += len(word)

    dict = viterbi(word, initial_state_probabilities, transition_probabilities, emission_probabilities)
    best_word = most_probable_word(dict)
    ##Checks for everymismatched letter, even if the word is not fully corrected, 
    ##it will still be counted as a mismatch if at least a letter is corrected
    for j in range(len(word)):
        if word[j] != actual_word[j] and actual_word[j] == best_word[j]:
            mismatched += 1
            print_if_true = True
    if print_if_true:
        print("OCR output: ", word, " Corrected word:", best_word)
        print_if_true = False

print("Out of ", total_letters, " letters, ", mismatched, " were mismatched.")