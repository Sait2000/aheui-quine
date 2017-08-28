import itertools

diff_to_code = dict([
    (-30, '바밦발따타'),
    (-29, '받밣밤따타'),
    (-28, '바밝밤따타'),
    (-27, '바밞받따타'),
    (-26, '박밝밤따타'),
    (-25, '바발발따타'),
    (-24, '바밣받따타'),
    (-23, '박발발따타'),
    (-22, '박밣받따타'),
    (-21, '바밝받따타'),
    (-20, '바발밤따타'),
    (-19, '박밝받따타'),
    (-18, '바밞밞다타'),
    (-17, '바밞밣다타'),
    (-16, '바밞밝다타'),
    (-15, '바밞밦다타'),
    (-14, '바밞발다타'),
    (-13, '바밞밤다타'),
    (-12, '바밞받다타'),
    (-11, '바밞박다타'),
    (-10, '바밣박다타'),
    (-9, '바밞타'),
    (-8, '바밣타'),
    (-7, '바밝타'),
    (-6, '바밦타'),
    (-5, '바발타'),
    (-4, '바밤타'),
    (-3, '바받타'),
    (-2, '바박타'),
    (-1, '박받타'),
    (0, '바'),
    (1, '받박타'),
    (2, '박'),
    (3, '받'),
    (4, '밤'),
    (5, '발'),
    (6, '밦'),
    (7, '밝'),
    (8, '밣'),
    (9, '밞'),
    (10, '밣박다'),
    (11, '밞박다'),
    (12, '밞받다'),
    (13, '밞밤다'),
    (14, '밞발다'),
    (15, '밞밦다'),
    (16, '밞밝다'),
    (17, '밞밣다'),
    (18, '밞밞다'),
    (19, '밝받따박타'),
    (20, '발밤따'),
    (21, '밝받따'),
    (22, '밣받따박타'),
    (23, '발발따박타'),
    (24, '밣받따'),
    (25, '발발따'),
    (26, '밝밤따박타'),
    (27, '밞받따'),
    (28, '밝밤따'),
    (29, '밣밤따받타'),
    (30, '밦발따'),
])

num_to_chr = dict([
    (0, '바'),
    (2, '반'),
    (3, '받'),
    (4, '밤'),
    (5, '발'),
    (6, '밦'),
    (7, '밝'),
    (8, '밣'),
    (9, '밞'),
])


length_record = 9e999
length_record_order = None


for t in itertools.permutations(range(2, 9 + 1)):
    if any(abs(n - p) == 1 for n, p in zip(t, (0,) + t)):
        continue
    ccs = [ord(num_to_chr[v]) for v in (0,) + t]
    total = sum(
        min(len(diff_to_code[n - p]), len(diff_to_code[p - n]))
        for n, p in zip(ccs[1:], ccs)
    )

    if total < length_record:
        length_record = total
        length_record_order = t

print('    #', length_record, length_record_order)

t = length_record_order
ccs = [ord(num_to_chr[v]) for v in (0,) + t]

for n, p, nc, pc in zip(t, (0,) + t, ccs[1:], ccs):
    d = n - p
    dc = nc - pc
    print('    push({})'.format(abs(d)))
    print('    {}()'.format('sub' if d > 0 else 'add'))
    print('    swap()')
    print('    push({})'.format(abs(dc)))
    print('    {}()'.format('add' if dc > 0 else 'sub'))
    print('''\
    swap()
    duplicate()

    # ord('{}') v-{}
    if pop_is_zero():
        pop()
        pop_print_char()
        continue
'''.format(chr(nc), n))
