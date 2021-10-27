import csv
import re


def sanitized(string: str):
    '''
    A function that takes a string and returns a sanitized version of it.
    The function first removes spaces between words and capitalizes the first letter of each word.
    Then, non-alphanumeric characters are replaced with underscores.
    '''
    return re.sub('[^0-9a-zA-Z]+', '_', string.strip().title().replace(' ', ''))


def escapeQuotes(string):
    '''
    Removes quotes in a string.
    '''
    return string.replace('"', '')


def serializeToTurtle(outPath, values, prefixData="http://ex.org/data", prefixPredicate="http://ex.org/pred#", elementTitlePredicateName="title"):
    '''
    A function that takes the following parameters:
    - outPath: path to the output file
    - values: a dictionary with the following structure:
        - keys: the value of the first column
        - values: a dictionary with the following structure:
            - keys: the titles of the rest of the columns (if no title, column name is col1, col2, etc.)
            - values: the corresponding value in the row for the given column

    The function writes the values to the output file in the .ttl format.
    For example, for the following input:
    {
        '1': {
            'id': '1',
            'column1': 'a',
            'column2': 'b'
        },
        '2': {
            'id': '2',
            'column1': 'c',
            'column2': 'd'
        }
    }
    The resulting turtle file would be:
    @prefix : <http://ex.org/data> .
    @prefix pred: <http://ex.org/pred#> .
    :1  :id "1" ;
        :column1 "a" ;
        :column2 "b" .
    :2  :id "2" ;  
        :column1 "c" ;
        :column2 "d" .
    '''
    with open(outPath, 'w', encoding='utf-8') as f:
        f.write('@prefix : <{}> .\n'.format(prefixData))
        f.write('@prefix pred: <{}> .\n\n'.format(prefixPredicate))
        for i, key in enumerate(values):
            sanitizedKey = sanitized(key)
            f.write(':{} '.format(sanitizedKey))
            f.write('pred:{} "{}" ;\n'.format(
                sanitized(elementTitlePredicateName), escapeQuotes(key)))
            for title in values[key]:
                sanitizedTitle = sanitized(title)
                f.write('pred:{} "{}" {}\n'.format(sanitizedTitle, escapeQuotes(
                    values[key][title]), '.' if i == len(values) - 1 else ';'))
            f.write('\n')


def processCSV(filePath, withTitles=True, delimiter=',', titleLine=1, dataLine=2):
    '''
    A function that takes the following parameters:
    - CSV file path with UTF-8 encoding
    - withTitles: true by default
    - delimiter: ',' by default
    - titleLine: line number of the title line (first line by default)
    - dataLine: line number of the first line of data

    The CSV file can have empty lines before the first line of data,
    and before the title line (which is optional, specified by withTitles).


    The function reads the CSV values and returns a tuple with the following elements:
    * title of the first column
    * dictionary with the following structure:
    - keys: the value of the first column
    - values: a dictionary with the following structure:
        - keys: the titles of the rest of the columns (if no title, column name is col1, col2, etc.)
        - values: the corresponding value in the row for the given column

    For example, for this CSV file:
    id,column1,column2
    1,a,b
    2,c,d

    The value returned by the function is:
    {
        '1': {
            'id': '1',
            'column1': 'a',
            'column2': 'b'
        },
        '2': {
            'id': '2',
            'column1': 'c',
            'column2': 'd'
        }
    }
    '''
    with open(filePath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter)
        lines = list(reader)

    if withTitles:
        titles = lines[titleLine - 1]
    else:
        titles = ['col{}'.format(i)
                  for i in range(1, len(lines[dataLine - 1]) + 1)]

    values = {}
    for line in lines[dataLine - 1:]:
        values[line[0]] = {}
        for i in range(1, len(line)):
            values[line[0]][titles[i]] = line[i]

    return (titles[0], values)


title, values = processCSV("test/test4.csv", withTitles=True,
                           delimiter=',', titleLine=1, dataLine=2)

serializeToTurtle("test/test4.ttl", values, elementTitlePredicateName=title)
