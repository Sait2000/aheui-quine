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


def install_global():
    import collections
    import functools
    import operator

    global 아, 악, 앆, 앇, 안, 앉, 않
    global 앋, 알, 앍, 앎, 앏, 앐, 앑
    global 앒, 앓, 암, 압, 앖, 앗, 았
    global 앙, 앚, 앛, 앜, 앝, 앞, 앟

    global AheuiStorage
    global AheuiHalt

    (
        아, 악, 앆, 앇, 안, 앉, 않,
        앋, 알, 앍, 앎, 앏, 앐, 앑,
        앒, 앓, 암, 압, 앖, 앗, 았,
        앙, 앚, 앛, 앜, 앝, 앞, 앟,
    ) = (chr(a + ord('아')) for a in range(28))

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

    class AheuiHalt(Exception): pass

    class AheuiStorageMixin(object):
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

    class AheuiStack(AheuiStorageMixin):
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

    class AheuiQueue(AheuiStorageMixin):
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

    class AheuiPipe(AheuiStorageMixin):
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

    class AheuiStorage(object):
        def __init__(self):
            self.activated = 아
            self.output_buffer = []
            self.machine_storage = {
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

        def activate(self, storage_id):
            self.activated = storage_id
            return True

        def send_to(self, other_storage_id):
            v = self.machine_storage[self.activated].pop()
            self.machine_storage[other_storage_id].push(v)
            return True

        def pop_is_nonzero(self):
            v = self.machine_storage[self.activated].pop()
            return v != 0

        def pop(self):
            self.machine_storage[self.activated].pop()
            return True

        def pop_print_char(self):
            v = self.machine_storage[self.activated].pop()
            self.output_buffer.append(v)
            return True

        def push_strict(self, val):
            if val not in (0, 2, 3, 4, 5, 6, 7, 8, 9):
                raise ValueError
            return self.push(val)

        def push(self, val):
            self.machine_storage[self.activated].push(val)
            return True

        def duplicate(self):
            self.machine_storage[self.activated].duplicate()
            return True

        def swap(self):
            self.machine_storage[self.activated].swap()
            return True

        def compare(self):
            self.machine_storage[self.activated].compare()
            return True

        def add(self):
            self.machine_storage[self.activated].add()
            return True

        def sub(self):
            self.machine_storage[self.activated].sub()
            return True

        def mul(self):
            self.machine_storage[self.activated].mul()
            return True

        def div(self):
            self.machine_storage[self.activated].div()
            return True

        def mod(self):
            self.machine_storage[self.activated].mod()
            return True

        def halt(self):
            raise AheuiHalt

        catch_typeerror = catch(TypeError)

        send_to_catch = catch_typeerror(send_to)
        pop_catch = catch_typeerror(pop)
        pop_print_char_catch = catch_typeerror(pop_print_char)
        duplicate_catch = catch_typeerror(duplicate)
        swap_catch = catch_typeerror(swap)
        compare_catch = catch_typeerror(compare)
        add_catch = catch_typeerror(add)
        sub_catch = catch_typeerror(sub)
        mul_catch = catch_typeerror(mul)
        div_catch = catch_typeerror(div)
        mod_catch = catch_typeerror(mod)

        del catch_typeerror

        def aheui_eval(self, commands):
            aheui_command_map = {
                '다': self.add,
                '따': self.mul,
                '맣': self.pop_print_char,
                '바': lambda: self.push_strict(0),
                '박': lambda: self.push_strict(2),
                '반': lambda: self.push_strict(2),
                '받': lambda: self.push_strict(3),
                '발': lambda: self.push_strict(5),
                '밝': lambda: self.push_strict(7),
                '밞': lambda: self.push_strict(9),
                '밣': lambda: self.push_strict(8),
                '밤': lambda: self.push_strict(4),
                '밦': lambda: self.push_strict(6),
                '빠': self.duplicate,
                '타': self.sub,
            }
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
        for v in vs:
            res.append('바반받밤발밦밝밣밞'[v])
    return ''.join(res)


if __name__ == '__main__':
    install_global()
    s = AheuiStorage()
    with open('code_area.aheui', 'rb') as fr:
        code_area = fr.read().decode('utf-8')
    s.aheui_eval(generate_data_area(code_area))
    try:
        # XXX
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
