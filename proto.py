def quine_code_area():
    assert activated == 아

    while send_to_catch(안):
        assert activated == 아
        push_strict(2)
        send_to(악)

    assert activated == 아

    while activate(안) and duplicate_catch():
        assert activated == 안
        # 바반받밤발밦밝밣밞
        #  0 2 3 4 5 6 7 8 9

        # 0 2 5 8 3 7 4 6 9

        send_to(아)

        aheui_eval('밞밞따빠밤다따밝타밝따박다') # push(48148) # 바
        swap()
        duplicate()

        # ord('바') v
        if not pop_is_nonzero():
            pop()
            pop_print_char()
            continue

        push_strict(2)
        sub()
        swap()
        push_strict(4)
        add()
        swap()
        duplicate()

        # ord('반') v-2
        if not pop_is_nonzero():
            pop()
            pop_print_char()
            continue

        push_strict(3)
        sub()
        swap()
        push_strict(4)
        add()
        swap()
        duplicate()

        # ord('발') v-5
        if not pop_is_nonzero():
            pop()
            pop_print_char()
            continue

        push_strict(3)
        sub()
        swap()
        push_strict(7)
        add()
        swap()
        duplicate()

        # ord('밣') v-8
        if not pop_is_nonzero():
            pop()
            pop_print_char()
            continue

        push_strict(5)
        add()
        swap()
        push_strict(8)
        sub()
        swap()
        duplicate()

        # ord('받') v-3
        if not pop_is_nonzero():
            pop()
            pop_print_char()
            continue

        push_strict(4)
        sub()
        swap()
        push_strict(2)
        add()
        swap()
        duplicate()

        # ord('밝') v-7
        if not pop_is_nonzero():
            pop()
            pop_print_char()
            continue

        push_strict(3)
        add()
        swap()
        push_strict(7)
        add()
        swap()
        duplicate()

        # ord('밤') v-4
        if not pop_is_nonzero():
            pop()
            pop_print_char()
            continue

        push_strict(2)
        sub()
        swap()
        push_strict(2)
        add()
        swap()
        duplicate()

        # ord('밦') v-6
        if not pop_is_nonzero():
            pop()
            pop_print_char()
            continue

        swap()
        push_strict(8)
        sub()
        swap()
        push_strict(0)

        # ord('밞') v-9
        if not pop_is_nonzero():
            pop()
            pop_print_char()
            continue

    aheui_eval('밦발따빠따밣다밝따박다밣따') # push(50864) # 우
    aheui_eval('빠맣발박따맣맣')

    assert activated == 안

    while activate(악) and pop_catch():
        aheui_eval('밞발따발따빠따밞밤다타') # push(50612) # 어
        pop_print_char()

    push_strict(5)
    push_strict(2)
    mul()

    assert activated == 악

    while pop_print_char() and activate(아) and duplicate_catch():
        push_strict(2)
        compare()
        sub()

        for __ in range(4):
            push_strict(9)
            mul()
            swap()
            duplicate()
            push_strict(2)
            compare()
            sub()
            add()

    push_strict(0)
    halt()


def install_global():
    import collections
    import functools
    import operator

    global 아, 악, 앆, 앇, 안, 앉, 않
    global 앋, 알, 앍, 앎, 앏, 앐, 앑
    global 앒, 앓, 암, 압, 앖, 앗, 았
    global 앙, 앚, 앛, 앜, 앝, 앞, 앟

    global activated

    global machine_storage

    global output_buffer

    global activate
    global send_to
    global pop_is_nonzero

    global pop
    global pop_print_char
    global push_strict
    global duplicate
    global swap

    global compare
    global add
    global sub
    global mul
    global div
    global mod

    global halt
    global AheuiHalt

    global send_to_catch
    global pop_catch
    global duplicate_catch
    global swap_catch
    global compare_catch
    global swap_catch
    global add_catch
    global sub_catch
    global mul_catch
    global div_catch
    global mod_catch

    global aheui_eval


    (
        아, 악, 앆, 앇, 안, 앉, 않,
        앋, 알, 앍, 앎, 앏, 앐, 앑,
        앒, 앓, 암, 압, 앖, 앗, 았,
        앙, 앚, 앛, 앜, 앝, 앞, 앟,
    ) = (chr(a + ord('아')) for a in range(28))

    activated = 아

    def catch(err_class):
        def deco(f):
            @functools.wraps(f)
            def f_catch(*args):
                try:
                    return f(*args)
                except err_class:
                    return False
            f_catch.__name__ += '_catch'
            return f_catch
        return deco

    def guard_arity(arity):
        def deco(f):
            @functools.wraps(f)
            def f_with_arity_check(self, *args):
                if not len(self.storage) >= arity:
                    raise TypeError
                return f(self, *args)
            return f_with_arity_check
        return deco

    def arithmetic(op):
        def deco(f_):
            @guard_arity(2)
            @functools.wraps(f_)
            def f(self):
                a = self.pop()
                b = self.pop()
                self.push(op(b, a))
            return f
        return deco

    class AheuiStorage(object):
        @arithmetic(lambda b, a: int(b >= a))
        def compare(self): pass

        @arithmetic(operator.add)
        def add(self): pass

        @arithmetic(operator.sub)
        def sub(self): pass

        @arithmetic(operator.mul)
        def mul(self): pass

        @arithmetic(operator.floordiv)
        def div(self): pass

        @arithmetic(operator.mod)
        def mod(self): pass

    class AheuiStack(AheuiStorage):
        def __init__(self):
            self.storage = []

        def push(self, val):
            self.storage.append(val)

        @guard_arity(1)
        def pop(self):
            return self.storage.pop()

        @guard_arity(1)
        def duplicate(self):
            self.storage.append(self.storage[-1])

        @guard_arity(2)
        def swap(self):
            self.storage[-2:] = self.storage[:-3:-1]

    class AheuiQueue(AheuiStorage):
        def __init__(self):
            self.storage = collections.deque()

        def push(self, val):
            self.storage.append(val)

        @guard_arity(1)
        def pop(self):
            return self.storage.popleft()

        @guard_arity(1)
        def duplicate(self):
            self.storage.appendleft(self.storage[0])

        @guard_arity(2)
        def swap(self):
            a = self.storage.popleft()
            b = self.storage.popleft()
            self.storage.appendleft(a)
            self.storage.appendleft(b)

    class AheuiPipe(AheuiStorage):
        def __init__(self):
            self.storage = []

        def push(self, val):
            raise NotImplementedError

        @guard_arity(1)
        def pop(self):
            raise NotImplementedError

        @guard_arity(1)
        def duplicate(self):
            raise NotImplementedError

        @guard_arity(2)
        def swap(self):
            raise NotImplementedError

    machine_storage = {
        storage_id: (
            AheuiQueue() if storage_id == 앙
            else AheuiPipe() if storage_id == 앟
            else AheuiStack()
        )
        for storage_id in (
            아, 악, 앆, 앇, 안, 앉, 않,
            앋, 알, 앍, 앎, 앏, 앐, 앑,
            앒, 앓, 암, 압, 앖, 앗, 았,
            앙, 앚, 앛, 앜, 앝, 앞, 앟,
        )
    }

    output_buffer = []

    def activate(storage_id):
        global activated
        activated = storage_id
        return True

    def send_to(other_storage_id):
        v = machine_storage[activated].pop()
        machine_storage[other_storage_id].push(v)
        return True

    def pop_is_nonzero():
        v = machine_storage[activated].pop()
        return v != 0

    def pop():
        machine_storage[activated].pop()
        return True

    def pop_print_char():
        v = machine_storage[activated].pop()
        output_buffer.append(v)
        return True

    def push_strict(val):
        if val not in (0, 2, 3, 4, 5, 6, 7, 8, 9):
            raise ValueError
        return push(val)

    def push(val):
        machine_storage[activated].push(val)
        return True

    def duplicate():
        machine_storage[activated].duplicate()
        return True

    def swap():
        machine_storage[activated].swap()
        return True

    def compare():
        machine_storage[activated].compare()
        return True

    def add():
        machine_storage[activated].add()
        return True

    def sub():
        machine_storage[activated].sub()
        return True

    def mul():
        machine_storage[activated].mul()
        return True

    def div():
        machine_storage[activated].div()
        return True

    def mod():
        machine_storage[activated].mod()
        return True

    def halt():
        raise AheuiHalt

    class AheuiHalt(Exception): pass

    catch_typeerror = catch(TypeError)

    send_to_catch = catch_typeerror(send_to)
    pop_catch = catch_typeerror(pop)
    duplicate_catch = catch_typeerror(duplicate)
    swap_catch = catch_typeerror(swap)
    compare_catch = catch_typeerror(compare)
    add_catch = catch_typeerror(add)
    sub_catch = catch_typeerror(sub)
    mul_catch = catch_typeerror(mul)
    div_catch = catch_typeerror(div)
    mod_catch = catch_typeerror(mod)

    aheui_command_map = {
        '다': add,
        '따': mul,
        '맣': pop_print_char,
        '바': lambda: push_strict(0),
        '박': lambda: push_strict(2),
        '반': lambda: push_strict(2),
        '받': lambda: push_strict(3),
        '발': lambda: push_strict(5),
        '밝': lambda: push_strict(7),
        '밞': lambda: push_strict(9),
        '밣': lambda: push_strict(8),
        '밤': lambda: push_strict(4),
        '밦': lambda: push_strict(6),
        '빠': duplicate,
        '타': sub,
    }

    def aheui_eval(commands):
        for command in commands:
            aheui_command_map[command]()


def generate_data_area(s):
    res = []
    for c in s:
        cc = ord(c)
        vs = []
        while len(vs) < 5:
            vs.append(cc % 9)
            cc //= 9
        for v in reversed(vs):
            res.append('바반받밤발밦밝밣밞'[v])
    return ''.join(reversed(res))


if __name__ == '__main__':
    install_global()
    with open('code_area.aheui', 'rb') as fr:
        code_area = fr.read().decode('utf-8')
    aheui_eval(generate_data_area(code_area))
    try:
        quine_code_area()
    except AheuiHalt:
        pass
    else:
        raise ValueError

    with open('quine.aheui', 'wb') as fw:
        fw.write(''.join(
            chr(cc)
            for cc in output_buffer
        ).encode('utf-8'))
