import re


def parse_time(s):
    ''' Parse duration of a course from the remark field.
    '''
    def helper(parity, rmk):
        for match in re.finditer(r'星期(?P<day>\w)\s*第(?P<cbegin>\d+)节--'
                                 r'第(?P<cend>\d+)节\s*(?P<place>.*)'
                                 r'\((?P<wbegin>\d+)-(?P<wend>\d+)周\)\.',
                                 parity):
            result = match.groupdict()
            result['day'] = '日一二三四五六'.index(result['day'])
            result.update({'parity': rmk})
            yield result

    try:
        odd, even = re.search(r'单周((?:\s(?:.*))+)双周((?:\s(?:.*))+)',
                              s).groups()
        for duration in helper(odd, 'odd'):
            yield duration
        for duration in helper(even, 'even'):
            yield duration
    except AttributeError:
        for duration in helper(s, 'both'):
            yield duration
