import pandas
from .accent__line import accent_line
import re
import os
from .mono_word_data import *
from pymystem3 import Mystem
ms = Mystem()

BASE_DIR = os.path.dirname(__file__)
sum_data = pandas.read_csv(os.path.join(BASE_DIR, 'sum_data.csv'), index_col=0, quotechar='&')


def is_ict(pos_ms, left_syll, syll_onset, syll_type, right_onset, left_neigh, last_syll, second_last_syll):
    if last_syll:
        ict_prob = 0.95
    elif second_last_syll:
        ict_prob = 0.07
    else:
        res_df = sum_data[(sum_data['POS_ms'] == pos_ms) &
                          (sum_data['left_syll'] == left_syll) &
                          (sum_data['syll_onset'] == syll_onset) &
                          (sum_data['syll_type'] == syll_type) &
                          (sum_data['right_onset'] == right_onset) &
                          (sum_data['left_neigh'] == left_neigh)]
        if len(res_df) == 0:
            return 0.5
        elif len(res_df) == 1:
            if res_df['ict'].values[0]:
                return 1.0
            else:
                return 0.0

        ict_f, ict_t = res_df['word'].values
        ict_prob = round(ict_t / (ict_t + ict_f), 2)

    return ict_prob


def verse_scheme_base(line):
    line = accent_line(line)
    line = re.sub(r'[аяоёуюыиэеАЯОЁУЮЫИЭЕ]\'', '1', line)
    # заменяем гласная+' на 1
    line = re.sub(r'[аяоёуюыиэеАЯОЁУЮЫИЭЕ]', '0', line)
    # заменяем оставшиеся гласные на нули
    line = re.sub(r'[^01]', '', line)
    # стираем всё кроме цифр
    return line


def verse_scheme_mono(line):
    # находим все односложные слова и расставляем там икты

    mono_ict_num = []
    words = ms.analyze(line)

    for i in range(len(words)):
        word_data = words[i]
        if count_vowels(word_data['text']) == 1:

            word = word_data['text'].lower()
            pos_ms = mystem_pos(word_data)

            syll_onset = get_syll_onset(word)
            syll_type = get_syll_type(word)
            left_neigh, left_syll, right_onset = neigh_data(words, i)

            syll_num = count_syll(words, i)
            num_reversed = count_syll(words) - syll_num
            last_syll = (num_reversed == 1)
            second_last_syll = (num_reversed == 2)

            if is_ict(pos_ms, left_syll, syll_onset, syll_type, right_onset, left_neigh, last_syll,
                      second_last_syll) > 0.5:
                mono_ict_num.append(syll_num)

    line = accent_line(line)
    line = re.sub(r'[аяоёуюыиэеАЯОЁУЮЫИЭЕ]\'', '1', line)
    # заменяем гласная+' на 1
    line = re.sub(r'[аяоёуюыиэеАЯОЁУЮЫИЭЕ]', '0', line)
    # заменяем оставшиеся гласные на нули
    line = re.sub(r'[^01]', '', line)
    # стираем всё кроме цифр
    line = list(line)
    for i in mono_ict_num:
        line[i] = '1'

    return line
