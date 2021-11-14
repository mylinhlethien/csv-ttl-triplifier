import csv
import re


def sanitized(string: str, capitalize=True):
    '''
    A function that takes a string and returns a sanitized version of it.
    The function first removes spaces between words
    and capitalizes the first letter of each word (if the capitalize option is set to true).
    Then, non-alphanumeric characters are replaced with underscores.
    '''
    inStr = string.strip()
    if capitalize:
        inStr = inStr.title()
    inStr.replace(' ', '')
    return re.sub('[^0-9a-zA-Z]+', '_', inStr)


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
    # Create the output file
    with open(outPath, 'w', encoding='utf-8') as f:
        # Add the prefix lines
        f.write('@prefix : <{}> .\n'.format(prefixData))
        f.write('@prefix pred: <{}> .\n\n'.format(prefixPredicate))
        # Write the triples
        for i, key in enumerate(values):
            # Write the sanitized subject
            sanitizedKey = sanitized(key)
            f.write(':{} '.format(sanitizedKey))
            # Write the triple <subject pred:firstcolumnname "UnsanitizedName">. Note that the predicate isn't capitalized
            f.write('pred:{} "{}" ;\n'.format(
                sanitized(elementTitlePredicateName, capitalize=False), escapeQuotes(key)))
            # Write the rest of the triples <subject pred:columnname "value">
            for k, title in enumerate(values[key]):
                sanitizedTitle = sanitized(title, capitalize=False)
                f.write('pred:{} "{}" {}\n'.format(sanitizedTitle, escapeQuotes(
                    values[key][title]), '.' if k == len(values[key]) - 1 else ';'))
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
    # Open the input file and read the lines
    with open(filePath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter)
        lines = list(reader)

    # Store the titles in a variable. If the CSV has no titles, the predicate names will be col1, col2, etc.
    if withTitles:
        titles = lines[titleLine - 1]
    else:
        titles = ['col{}'.format(i)
                  for i in range(1, len(lines[dataLine - 1]) + 1)]

    # Build the value dictionary following the structure documented above
    values = {}
    for line in lines[dataLine - 1:]:
        values[line[0]] = {}
        for i in range(1, len(line)):
            values[line[0]][titles[i]] = line[i]

    return (titles[0], values)


# TODO: don't hardcode these values
title, values = processCSV("test/test1.csv", withTitles=False,
                           delimiter=';', titleLine=1, dataLine=3)

# TODO default titleLine and dataLine. WithTitles default True
# TODO fix serializer
serializeToTurtle("test/test1.ttl", values, elementTitlePredicateName=title)
