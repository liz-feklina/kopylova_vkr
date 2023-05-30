import re
import sys
import pandas
from .meter_recognition import verse_scheme_base, verse_scheme_mono

choree = '10'*100
iamb = '01'*100
dactyl = '100'*100
amphibrach = '010'*100
anapaest = '001'*100

meters = [choree, iamb, dactyl, amphibrach, anapaest]
meters_name = ['choree', 'iamb', 'dactyl', 'amphibrach', 'anapaest']

ict = 'о̀'[1]

# sum_data = pandas.read_csv('/content/drive/MyDrive/diplom/sum_data.csv', index_col=0, quotechar='&')


def meter_rec(line, function_name='verse_scheme_mono', a1=1, a2=1):
    line = re.sub(ict, '', line)
    rhythm = None
    if function_name == 'verse_scheme_base':
        rhythm = verse_scheme_base(line)
    if function_name == 'verse_scheme_mono':
        rhythm = verse_scheme_mono(line)
    scores = []
    for meter in meters:
        s = 0
        for i in range(len(rhythm)):
            if rhythm[i] == '1' and meter[i] == '0':
                s += a1
            elif rhythm[i] == '0' and meter[i] == '1':
                s += a2
        scores.append(s)
    val, idx = min((val, idx) for (idx, val) in enumerate(scores))
    return meters_name[idx]


def write_file(files):
    for file in files:
        with open(file, encoding='utf-8') as clear_file:
            with open(re.sub(r'\.(?=[^.]+$)', '.accented.', file), 'w', encoding='utf-8') as file_write:
                for line in clear_file:
                    file_write.write(meter_rec(line) + '\n')


def main():
    files = sys.argv[1:]
    if not files:
        print('No files to accent')
        exit()
    write_file(files)


if __name__ == '__main__':
    main()
