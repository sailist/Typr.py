from pprint import pprint

from Typr.reader import read_uint, read_ushort, read_ascii
from Typr.parser import parse_map, parse_list

with open('LiberationSans-Bold.ttf', 'rb') as r:
    buf = r.read()

print(buf[:4])

tag, _, offset = read_ascii(buf)
tag = b''.join(tag)  # .decode()


def summary_table(buf, foff=0):
    res = {}
    num_tables, _, _ = read_ushort(buf, foff + 4)

    offset = foff + 12
    for i in range(num_tables):
        tag, _, offset = read_ascii(buf, offset)
        tag = b''.join(tag).decode()

        check_sum, _, offset = read_uint(buf, offset)
        toffset, _, offset = read_uint(buf, offset)
        length, _, offset = read_uint(buf, offset)

        res[tag] = [toffset, length]

    return res


res = summary_table(buf)

font_obj = {}
for k in parse_list:
    if k in {'cmap'}:
        off, length = res[k]
        tobj = parse_map[k](buf, off, length, font_obj)

        print(k)
        pprint(tobj)
        font_obj[k] = tobj
        # print(tobj['tables'][0]['endCount'])
