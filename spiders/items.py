from .loader.item import Field, Item
from .loader.processors import MapCompose, TakeFirst

from w3lib.html import remove_tags
import json
import re


def parse_time(string_to_parse):
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
                              string_to_parse).groups()
        for duration in helper(odd, 'odd'):
            yield duration
        for duration in helper(even, 'even'):
            yield duration
    except AttributeError:
        for duration in helper(string_to_parse, 'both'):
            yield duration


class Course(Item):
    teacher = Field(input_processor=MapCompose(remove_tags, str.strip),
                    output_processor=TakeFirst())
    teacher_job = Field(input_processor=MapCompose(remove_tags, str.strip),
                        output_processor=TakeFirst())
    time = Field(input_processor=MapCompose(remove_tags,
                                            lambda s:
                                            json.dumps(list(parse_time((s))))),
                 output_processor=TakeFirst())
    cid = Field(input_processor=MapCompose(remove_tags, lambda s: re.search('\w{2}\d{3}', s).group(0)),
                output_processor=TakeFirst())
    hours = Field(input_processor=MapCompose(remove_tags, int),
                  output_processor=TakeFirst())
    max_member = Field(input_processor=MapCompose(remove_tags, int),
                       output_processor=TakeFirst())
    min_member = Field(input_processor=MapCompose(remove_tags, int),
                       output_processor=TakeFirst())
    now_member = Field(input_processor=MapCompose(remove_tags, int),
                       output_processor=TakeFirst())
    remark = Field(input_processor=MapCompose(remove_tags, str.strip),
                   output_processor=TakeFirst())
    course_type = Field(output_processor=TakeFirst())
    place = Field(input_processor=TakeFirst())
    bsid = Field(input_processor=lambda s: int(s[0]),
                 output_processor=TakeFirst())
    asp = Field(input_processor=MapCompose(remove_tags, str.strip),
                output_processor=TakeFirst())
