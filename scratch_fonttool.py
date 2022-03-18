import math

from fontTools import ttLib

from Typr.parser import parse_cmap, parse_glyf
from Typr.svg import simple_Glyphfunction

tt = ttLib.TTFont("LiberationSans-Bold.ttf")
print(tt)

print(tt['maxp'].__dict__)
## 字形的数量
print(tt['maxp'].__dict__['numGlyphs'])

"""
loca 表的结构是一个数组，
每一项对应一个字体形状数据在 glyf 表中的偏移位置(offset)。
不过 loca 表对偏移位置的存储有两种方式: long 和 sort。
具体使用哪个，由 head 表中 indexToLocFormat 标识决定。
"""
indexToLocFormat = tt['head'].__dict__['indexToLocFormat']
# indexToLocFormat = 0 // sort 模式
# indexToLocFormat = 1 // long 模式


print(len(tt['loca'].__dict__['locations']))

cmap_buf = tt.getTableData('cmap')
cmap_data = parse_cmap(cmap_buf, 0, len(cmap_buf), {})

tind = cmap_data['ids']['p0e3']
table = cmap_data['tables'][tind]
# print()
fmt = table['format']
end_count = table['endCount']



def arr_search(arr, k, v):
    l = 0
    r = math.floor(len(arr) / k)
    while l + 1 != r:
        mid = l + ((r - l) >> 1)
        if (arr[mid * k] <= v):
            l = mid
        else:
            r = mid
    return l * k


print(tt['kern'].__dict__['kernTables'][0].__dict__['kernTable'])

# def parse_text(text):
text = 'P'
for i, code in enumerate(text):
    code = list(code.encode('utf-8'))[0]
    sind = arr_search(end_count, 1, code)
    print(sind)
    print(table['idDelta'][sind])
    gli = code + table['idDelta'][sind]
    gid = gli & 0xFFFF

    padj = [0, 0, 0, 0]


    # print(tt['glyf'].__dict__.keys())
    gl = tt['glyf'].__dict__['glyphOrder'][gid]
    # ax = font["hmtx"].aWidth[gid] + padj[2]
    ax, _ = tt['hmtx'].__dict__['metrics']['P']  # ax = 1366

    shape = {"g": gid, "cl": i, "dx": 0, "dy": 0, "ax": ax, "ay": 0}

    data = tt['glyf'].__dict__['glyphs'][gl].data

    data = parse_glyf(data)
    print(data)

    svg_path = simple_Glyphfunction(data)

    print(' '.join([str(i) for i in svg_path]))
