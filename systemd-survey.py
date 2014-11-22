#!/usr/bin/env python3

with open('systemd-survey', 'rb') as file:
    data = file.read()
data = data.decode('utf-8', 'replace').split('\n')

columns = []
column_name = None
column_data = []

for line in data:
    if line[:3] == ':: ':
        column_name = line[3:]
    elif line[:10] == '==========':
        columns.append((column_name, column_data))
        column_data = []
    else:
        column_data.append(line)

survey = []
names = [name for name, _ in columns]

for i in range(len(columns)):
    data = []
    for j in range(len(columns[0][1])):
        data.append(columns[i][1][j])
    survey.append(data)

import sys

if len(sys.argv) == 1:
    i = 0
    for name in names:
        i += 1
        print('%2i - %s' % (i, name))
    sys.exit(0)

def transpose(m):
    x, y = len(m), len(m[0])
    mt = [[None] * x for _ in range(y)]
    for i in range(x):
        for j in range(y):
            mt[j][i] = m[i][j]
    return mt

def sort_survey(survey, i):
    survey_t = transpose(survey)
    survey_t.sort(key = lambda x : x[i])
    survey = transpose(survey_t)
    return survey

def unique(answers):
    last = None
    count = 0
    result = []
    for answer in answers:
        if answer != last:
            if last is not None:
                result.append((last, count))
            last = answer
            count = 1
        else:
            count += 1
    result.append((last, count))
    return result

def print_survey(args, subsurvey, indent = ''):
    if len(args) == 0:
        return
    i = xint(args[0])
    reverse = '^' not in args[0]
    filterto = None
    mapping = None
    if '=' in args[0]:
        filterto = {}
        for x in args[0][args[0].find('=') + 1:].split('::'):
            answer = x.split(':')[0].lower()
            newanswer = ':'.join(x.split(':')[1:])
            if newanswer == '':
                newanswer = answer
            filterto[answer] = newanswer
    args = args[1:]
    subsurvey = sort_survey(subsurvey, i)
    answers = unique(subsurvey[i])
    maxcount = sum([x[1] for x in answers])
    offset = 0
    answers_ = []
    for answer, count in answers:
        end = offset + count
        answers_.append((answer, count, offset, end))
        offset = end
    answers = sorted(answers_, key = lambda x : x[1])
    answers = reversed(answers) if reverse else answers
    for answer, count, offset, end in answers:
        if (filterto is not None) and (answer.lower() not in filterto):
            continue
        if filterto is not None:
            answer = filterto[answer.lower()]
        print('%s‘%s’ (%i %%, %i of %i)' % (indent, answer, 100 * count / maxcount + 0.5, count, maxcount))
        print_survey(args, [subsurvey[i][offset : end] for i in range(len(subsurvey))], indent + '  ')

def xint(s):
    s = s.replace('^', '')
    if '=' in s:
        s = s[:s.find('=')]
    return int(s) - 1

for name in [names[xint(i)] for i in sys.argv[1:]]:
    print(name)
print()

print_survey(sys.argv[1:], survey)

