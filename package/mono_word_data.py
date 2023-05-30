vowels = list('аяоёуюыиэеАЯОЁУЮЫИЭЕ')


def get_syll_type(word):
    if word[-1] in vowels:
        return 'open'
    else:
        return 'closed'


def count_vowels(word):
    s = 0
    global vowels
    for letter in word:
        if letter in vowels:
            s += 1
    return s


def count_syll(words, position=-1):
    line_segment = ''.join([word['text'] for word in words[:position]])
    return count_vowels(line_segment)


def get_syll_onset(word):
    if word[0] in vowels:
        return 'open'
    else:
        return 'closed'


def mystem_pos(word):
    if 'analysis' in word and len(word['analysis']) != 0:
        return word['analysis'][0]['gr'].split('=')[0].split(',')[0]
    else:
        return 'NA'


def neigh_data(words, position):
    if position > 1:
        left = words[position - 2]['text']
        left_neigh = (count_vowels(left) == 1)
        left_syll = get_syll_type(left)
    else:
        left_neigh = False
        left_syll = None

    try:
        right = words[position + 2]['text']
        # right_neigh = (count_vowels(right) == 1)
        right_onset = get_syll_onset(right)
    except IndexError:
        # right_neigh = False
        right_onset = None

    return left_neigh, left_syll, right_onset
