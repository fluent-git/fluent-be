import json
import string
import re

second_per_word = 0.6


def analyze(input, source, time, expected_time=0):
    old_src = source
    input = input.translate(
        str.maketrans('', '', string.punctuation)).lower()
    source = source.translate(
        str.maketrans('', '', string.punctuation)).lower()
    response = {}

    # result calculation
    # wrong words will be marked by *...*
    differences = set(source.split()) - set(input.split())
    differences = sorted(differences, key=len, reverse=True)
    words = old_src.split()
    result = []
    for word in words:
        if word.lower() in differences:
            result.append('*' + word + '*')
        elif word[:-1].lower() in differences:
            result.append('*' + word[:-1] + '*' + word[-1])
        else:
            result.append(word)
    response['result'] = ' '.join(result)
    response['wrong_words'] = list(differences)

    # clarity calculation
    count_src = len(set(source.split()))
    count_differences = len(differences)
    clarity = (count_src-count_differences)/count_src
    response['clarity'] = round(clarity, 2)

    # pace calculation
    # if expected_time wasn't set, replace it with <total words in source>*second_per_word
    if expected_time == 0:
        expected_time = len(source.split())*second_per_word
    if time-2*expected_time <= 0:
        pace = 1 - (time-expected_time)/expected_time
    else:
        pace = 0
    response['pace'] = round(pace, 2)

    # star calculation
    star = (clarity+pace)/2
    if star < 0.25:
        star = 0
    elif star < 0.5:
        star = 1
    elif star < 0.75:
        star = 2
    else:
        star = 3
    response['star'] = star

    return response
