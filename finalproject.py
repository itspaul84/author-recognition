# Basic text recognition to help determine authorship, given an idea as to who the author might be

import math

def clean_text(txt):
    """ takes a string of text txt and returns a list containing
    the words in txt after it has been cleaned
    """
    txt = txt.lower()
    txt = txt.replace('.', '')
    txt = txt.replace(',', '')
    txt = txt.replace('?', '')
    txt = txt.replace('!', '')
    txt = txt.replace(';', '')
    return txt

def sample_file_write(filename):
    """A function that demonstrates how to write a
        Python dictionary to an easily-readable file.
    """
    d = {'test': 1, 'foo': 42}   # Create a sample dictionary.
    f = open(filename, 'w')      # Open file for writing.
    f.write(str(d))              # Writes the dictionary to the file.
    f.close()                    # Close the file.

def sample_file_read(filename):
    """A function that demonstrates how to read a
       Python dictionary from a file.
    """
    f = open(filename, 'r')    # Open for reading.
    d_str = f.read()           # Read in a string that represents a dict.
    f.close()

    d = dict(eval(d_str))      # Convert the string to a dictionary.

    print("Inside the newly-read dictionary, d, we have:")
    print(d)

def stem(s):
    """ Accepts a string and returns the stem of s """
    if s[-1] == 's' and len(s) > 4:
        s = s[:-1]          #plural cases
    if s[-3:] == 'ing' and len(s) > 5:
        if s[-4] == s[-5]:
            if s[-4] == 'l':
                s = s[:-3]  #cases such as 'killing'
            else:
                s = s[:-4]  #cases such as 'stemming'
        else:
            s = s[:-3]      #cases such as 'playing'
    elif s[-3:] == 'ier' and len(s) > 5:
        s = s[:-3] + 'y'    #cases such as 'partier'
    elif s[-2:] == 'er' and len(s) > 4:
        if s[-3] == s[-4]:
            s = s[:-3]      #cases such as 'spammer'
        else:
            s = s[:-2]      #cases such as 'reader'
    elif s[-3:] == 'ies' and len(s) > 5:
        s = s[:-3] + 'y'    #cases such as 'parties'

    return s

def compare_dictionaries(d1, d2):
    """ takes two dictionaries and returns their log similarity score
    """
    score = 0
    total = 0
    for i in d1:
        total += d1[i]
    for j in d2:
        if j in d1:
            score += d2[j]*math.log(d1[j]/total)
        else:
            score += d2[j]*math.log(0.5/total)
    return score
    

class TextModel:
    """ begins a TextModel class """
    def __init__(self, model_name):
        """ constructs a new TextModel object with model_name
        as a parameter
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.common = {}
        

    def __repr__(self):
        """ returns a string that includes the name of the model
        as well as the sizes of the dictionaries for each feature
        of the text
        """
        s = 'text model name: ' + self.name + '\n'
        s += ' number of words: ' + str(len(self.words)) + '\n'
        s += ' number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += ' number of stems: ' + str(len(self.stems)) + '\n'
        s += ' number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += ' number of common words: ' + str(len(self.common))
        return s

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model.
        """

        common_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that',
                        'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he',
                        'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by',
                        'from', 'they', 'we', 'say', 'her', 'she']
        
        
        
        sentences = s.replace('?', '.')
        sentences = sentences.replace('!', '.')
        sentences = sentences.split('.')
        for a in range(len(sentences)):
            if sentences[a] != '':
                j = sentences[a].split(' ')
                if len(j) not in self.sentence_lengths:
                    self.sentence_lengths[len(j)] = 1
                else:
                    self.sentence_lengths[len(j)] += 1
                
        
        # Add code to clean the text and split it into a list of words.
        # *Hint:* Call one of your other methods!
        word_list = clean_text(s)
        word_list = word_list.split(' ')

        # Template for updating the words dictionary.
        for w in word_list:
            # Update self.words to reflect w
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
            # either add a new key-value pair for w
            # or update the existing key-value pair.
            
            

        # Add code to update other feature dictionaries.
        for p in word_list:
            if len(p) not in self.word_lengths:
                self.word_lengths[len(p)] = 1
            else:
                self.word_lengths[len(p)] += 1

        for j in word_list:
            j = stem(j)
            if j not in self.stems:
                self.stems[j] = 1
            else:
                self.stems[j] += 1

        for h in word_list:
            if h in common_words:
                if h not in self.common:
                    self.common[h] = 1
                else:
                    self.common[h] += 1

        

    def add_file(self, filename):
        """ adds all of the text in the file to the model """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        self.add_string(str(f))

    def save_model(self):
        """ saves the TextModel object self by writing its various
        feature dictionaries to files
        """
        d = self.words
        f = open(self.name + '_words', 'w')
        f.write(str(d))
        f.close()
        
        g = self.word_lengths
        h = open(self.name + '_word_lengths', 'w')
        h.write(str(g))
        h.close()

        i = self.stems
        j = open(self.name + '_stems', 'w')
        j.write(str(i))
        j.close()

        k = self.sentence_lengths
        m = open(self.name + '_sentence_lengths', 'w')
        m.write(str(k))
        m.close()

        o = self.common
        p = open(self.name + '_common', 'w')
        p.write(str(o))
        p.close()

    def read_model(self):
        """ reads the stored dictionaries for the called TextModel
        object from their files and assigns them to the attributes
        of the called TextModel
        """
        f = open(self.name + '_words', 'r')
        d_str = f.read()
        f.close()

        d = dict(eval(d_str))
        self.words = d

        g = open(self.name + '_word_lengths', 'r')
        h_str = g.read()
        g.close()

        h = dict(eval(h_str))
        self.word_lengths = h

        i = open(sel.name + '_stems', 'r')
        j_str = i.read()
        i.close()

        j = dict(eval(j_str))
        self.stems = j

        k = open(self.name + '_sentence_lengths', 'r')
        m_str = k.read()
        k.close()

        m = dict(eval(m_str))
        self.sentence_lengths = m

        o = open(self.name + '_common', 'r')
        p_str = o.read()
        o.close()

        p = dict(eval(p_str))
        self.common = p

        s = 'text model name: ' + self.name + '\n'
        s += 'number of words: ' + str(len(self.words)) + '\n'
        s += 'number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += 'number of stems: ' + str(len(self.stems)) + '\n'
        s += 'number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += 'number of common words: ' + str(len(self.common))

    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores
        measuring the similarity of self and other
        """
        list = []
        word_score = compare_dictionaries(other.words, self.words)
        list.append(word_score)
        wl_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        list.append(wl_score)
        stems_score = compare_dictionaries(other.stems, self.stems)
        list.append(stems_score)
        sl_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        list.append(sl_score)
        common_score = compare_dictionaries(other.common, self.common)
        list.append(common_score)
        
        return list

    def classify(self, source1, source2):
        """ compares the called TextModel object to two other source
        TextModel objects and determines which is the more likely
        source
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for', source1.name, ': ', scores1)
        print('scores for', source2.name, ': ', scores2)
        sum1 = 0
        sum2 = 0
        for i in range(len(scores1)):
            sum1 += scores1[i]
        for j in range(len(scores2)):
            sum2 += scores2[j]
        if sum1 > sum2:
            print(self.name, 'is more likely to have come from ', source1.name)
        else:
            print(self.name, 'is more likely to have come from ', source2.name)


def test():
    """ tests the comparisons """ 
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)


def run_tests():
    """ Goes through the program """
    source1 = TextModel(Insert Name)
    source1.add_file('source1.txt')

    source2 = TextModel(Insert Name)
    source2.add_file('source2.txt')

    new1 = TextModel(Insert Name)
    new1.add_file('new1.txt')
    new1.classify(source1, source2)




    

    
            



        
