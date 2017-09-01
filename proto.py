def quine_code_area(s):
    assert s.activated == 아
    s.push_strict(0)
    s.push_strict(0)
    s.send_to(안)
    s.send_to(안)

    while s.duplicate_catch():
        assert s.activated == 아
        s.aheui_eval('밞발따발따빠따밞밤다타') # s.push(50612) # 어
        s.send_to(악)

        s.send_to(안)
        s.activate(안)
        s.swap()
        s.push_strict(9)
        s.mul()
        s.swap()
        s.duplicate()
        s.push_strict(2)
        s.compare()
        s.sub()
        s.add()
        s.swap()
        s.push_strict(2)
        s.add()
        s.duplicate()
        s.push_strict(9)
        s.compare()
        if s.pop_is_nonzero():
            s.pop()
            s.send_to(앋)
            s.push_strict(0)
            s.push_strict(0)
        else:
            s.swap()

        s.activate(아)

        s.duplicate()

        s.duplicate()
        s.push_strict(2)
        s.compare()
        s.push_strict(2)
        s.mul()
        s.swap()

        s.duplicate()
        s.push_strict(3)
        s.compare()
        s.push_strict(2)
        s.mul()
        s.swap()

        s.duplicate()
        s.push_strict(4)
        s.compare()
        s.push_strict(8)
        s.mul()
        s.swap()

        s.duplicate()
        s.push_strict(6)
        s.compare()
        s.push_strict(9)
        s.mul()
        s.swap()

        s.duplicate()
        s.push_strict(8)
        s.compare()
        s.push_strict(2)
        s.mul()
        s.swap()

        s.duplicate()
        s.push_strict(5)
        s.compare()
        s.push_strict(9)
        s.mul()
        s.swap()

        s.duplicate()
        s.push_strict(7)
        s.compare()
        s.push_strict(7)
        s.mul()
        s.swap()

        s.push_strict(9)
        s.compare()
        s.push_strict(3)
        s.mul()

        s.add()
        s.add()
        s.sub()
        s.add()
        s.add()
        s.add()
        s.add()
        s.add()
        s.aheui_eval('밞밞따빠밤다따밝타밝따박다') # s.push(48148) # 바
        s.add()

        # s.pop_print_char()
        s.send_to(알)

    while s.activate(알) and s.pop_print_char_catch():
        pass

    s.aheui_eval('밦발따빠따밣다밝따박다밣따') # s.push(50864) # 우
    s.aheui_eval('빠맣발박따맣맣')

    while s.activate(악) and s.pop_print_char_catch():
        pass

    s.push_strict(5)
    s.push_strict(2)
    s.mul()
    s.pop_print_char()

    while s.activate(앋) and s.pop_print_char_catch():
        pass

    s.halt()


def generate_data_area(s):
    res = []
    for c in s:
        cc = ord(c)
        vs = []
        while len(vs) < 5:
            vs.append(cc % 9)
            cc //= 9
        for v in vs:
            res.append('바반받밤발밦밝밣밞'[v])
    return ''.join(res)


if __name__ == '__main__':
    from storage import *
    s = AheuiStorage()
    with open('code_area.aheui', 'rb') as fr:
        code_area = fr.read().decode('utf-8')
    s.aheui_eval(generate_data_area(code_area))
    try:
        quine_code_area(s)
    except AheuiHalt:
        pass
    else:
        raise ValueError

    with open('quine.aheui', 'wb') as fw:
        fw.write(''.join(
            chr(cc)
            for cc in s.output_buffer
        ).encode('utf-8'))
