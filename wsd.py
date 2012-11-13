import re
import os
from util import *
from wsddata import *

from EditDistance import edist

# simpleEFeatures(w) takes a word (in English) and generates relevant
# features.  At the very least, this should include the word identity
# as a feature.  You should also make it include prefix (two
# characters) and suffix (two characters) features.
def simpleEFeatures(w, wprob):
    feats = Counter()     # features are a mapping from strings (names) to floats (values)

    # generate a single feature with the word identity, called
    # w_EWORD, and value 1
    feats['w_' + w] = 1

    # generate a feature called wlogprob whose value is log(wprob)
    feats['wlogprob'] = log(wprob)

    # generate a feature corresponding to the two character prefix of
    # this word and a second feature for the two character suffix.
    # for example, on the word "happiness", generate "pre_ha" and
    # "suf_ss" as features.
    ### TODO: YOUR CODE HERE

    
    feats['pre_' + w[:2]]  = 1
    feats['suf_' + w[-2:]] = 1

    return feats

# simpleFFeatures(doc, i, j) asks for features about the French word
# in sentence i, position j of doc (i.e., at doc[i][j]).
def simpleFFeatures(doc, i, j):
    w = doc[i][j]

    feats = Counter()

    # generate a single feature with the (french) word identity
    feats[w] = 1

    # generate a feature corresponding to the two character prefix of
    # this word and a second feature for the two character suffix; same
    # deal about pre_ and suf_
    ### TODO: YOUR CODE HERE
    #util.raiseNotDefined()

    feats['pre_' + w[:2]]  = 1
    feats['suf_' + w[-2:]] = 1

    # generate features corresponding to the OTHER words in this
    # sentence.  for some other word "w", create a feature of the form
    # sc_w, where sc means "sentence context".  if a single word (eg.,
    # "the") appears twice in the context, the feature sc_the should
    # have value two.
    ### TODO: YOUR CODE HERE
    #


    for idx in range(len(doc[i])):
        word = doc[i][idx]
        # word != w ? what if it apears with itself?
        if idx == j: continue

        feat_name = 'sc_' + word

        if feat_name not in feats:
            feats[feat_name] = 1
        else:
            feats[feat_name] += 1

    return feats

# simplePairFeatures(doc, i, j, ew, wprob) -- the first three are the
# same as for simpleFFeatures, the last two are the same as for
# simpleEFeatures.  we return features that are functions of both the
# french word (doc[i][j] and the english word w.
def simplePairFeatures(doc, i, j, ew, wprob):
    fw = doc[i][j]

    feats = Counter()

    # we have just one feature that asks if the fw and ew are
    # identical; this is really only useful for example on proper
    # nouns
    if fw == ew:
        feats['w_eq'] = 1

    return feats

def complexEFeatures(w, wprob):
    feats = Counter()

    # Simple Features
    feats['w_' + w] = 1
    feats['wlogprob'] = log(wprob)
    feats['pre_' + w[:2]]  = 1
    feats['suf_' + w[-2:]] = 1

    # Check for particular suffixes
    #
    # 1 letter
    one = w[-1]
    if one in ['s', 'd']:
        feats['1_suf_' + one ] = 1

    # 2 letter
    two = w[-2:]
    if two in ['es', 'ed', 'ly']:
        feats['2_suf_' + two] = 1

    # 3 letter
    three = w[-3:]
    if three in ['ing', 'ity', 'ize', 'ies']:
        feats['3_suf_' + three] = 1

    # 4 letter
    four = w[-4:]
    if four in ['ment', 'tion', 'ness']:
        feats['f_suf_' + four] = 1





    return feats

def complexFFeatures(doc, i, j, tree=None):
    feats = Counter()

    # Simple Features
    w = doc[i][j]

    feats[w] = 1
    feats['pre_' + w[:2]]  = 1
    feats['suf_' + w[-2:]] = 1

    for idx in range(len(doc[i])):
        word = doc[i][idx]
        if idx == j: continue
        feat_name = 'sc_' + word
        if feat_name not in feats:
            feats[feat_name] = 1
        else:
            feats[feat_name] += 1

    #ctxtRange = 10
    # Document Context: For every word in the document, the feature is the number of times
    #   that word appears
    for sentence_idx in range(len(doc)-1):
        if sentence_idx < 0 or sentence_idx >= len(doc) or sentence_idx == i:
            continue
        for w in doc[sentence_idx]:
            feat_name = 'dc_' + w
            if feat_name not in feats:
                feats[feat_name] = 1
            else:
                feats[feat_name] += 1


    # Neighbor Context Feature: Word immediately to left and right
    if (j - 1) > 0:
        left_word = doc[i][j-1]
        feat_name = 'ln_' + left_word
        feats[feat_name] = 1

    if (j + 1) < len(doc[i]):
        right_word = doc[i][j+1]
        feat_name = 'rn_' + right_word
        feats[feat_name] = 1

    return feats

def complexPairFeatures(doc, i, j, ew, wprob, tree=None):
    fw = doc[i][j]
    feats = Counter()

    # Simple Features
    if fw == ew:
        feats['w_eq'] = 1

    # Edit Distance:
    editDist = edist(ew, fw)
    if editDist != 0:
        feats['edist'] = 1 / editDist
    else:
        feats['edist'] = 1



    return feats

if __name__ == "__main__":
    (train_acc, test_acc, test_pred) = runExperiment('Science.tr', 'Science.de', complexFFeatures, complexEFeatures, complexPairFeatures, quietVW=True)
    print 'training accuracy =', train_acc
    print 'testing  accuracy =', test_acc
    h = open('wsd_output', 'w')
    for x in test_pred:
        h.write(str(x[0]))
        h.write('\n')
    h.close()
