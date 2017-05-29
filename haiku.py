__author__ = 'Zachery Thomas'


import math
from textstat.textstat import textstat


def haiku(text):
    words = text.split()

    syllables = [int(math.ceil(textstat.syllable_count(word))) for word in words]
    if sum(syllables) != 17: return

    syl_line = [0,0,0]
    haiku_lines = ['','','']

    for word, syllable_count in zip(words, syllables):
        if syl_line[0] < 5:
            syl_line[0] += syllable_count
            haiku_lines[0] += word + ' '
        elif syl_line[0] is 5 and syl_line[1] < 7:
            syl_line[1] += syllable_count
            haiku_lines[1] += word + ' '
        elif syl_line[0] is 5 and syl_line[1] is 7 and syl_line[2] < 5:
            syl_line[2] += syllable_count
            haiku_lines[2] += word + ' '

        # ain't a haiku,
        if syl_line[0] > 5 or syl_line[2] > 5 or syl_line[1] > 7: return

    # If haiku return haiku as string
    if syl_line == [5, 7, 5]:
        return ('%s\n%s\n%s' % tuple(haiku_lines))[:-1]


if __name__ == '__main__':
    test_haiku = """An old silent pond... A frog jumps into the pond, splash! Silence again."""
    print haiku(test_haiku)