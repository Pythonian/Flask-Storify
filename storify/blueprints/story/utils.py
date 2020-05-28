import re
import math
from django.utils.html import strip_tags


def count_words(html_string):
    word_string = strip_tags(html_string)
    count = len(re.findall(r'\w+', word_string))
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    # round up value to the nearest minute. 200 wpm
    read_time_min = math.ceil(count // 200)
    return int(read_time_min)
