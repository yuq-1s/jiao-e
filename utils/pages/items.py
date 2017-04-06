from scrapy import Field, Item
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
from ..parsers import parse_time
import re


class Course(Item):
    teacher = Field(input_processor=MapCompose(remove_tags, str.strip),
                    output_processor=TakeFirst())
    teacher_job = Field(input_processor=MapCompose(remove_tags, str.strip),
                        output_processor=TakeFirst())
    time = Field(input_processor=MapCompose(remove_tags, parse_time))
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
    bsid = Field(input_processor=lambda s: int(s[0]), output_processor=TakeFirst())

