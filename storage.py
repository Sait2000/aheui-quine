import collections
import functools
import operator


__all__ = ['AheuiStorage', 'AheuiHalt']

__all__ += [chr(a + ord('아')) for a in range(28)]

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


class AheuiHalt(Exception):
    pass


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

    def aheui_eval(self, commands, input_num=None, input_char=None):
        aheui_command_map = {
            '다': self.add,
            '따': self.mul,
            '맣': self.pop_print_char,
            '바': lambda: self.push_strict(0),
            '박': lambda: self.push_strict(2),
            '밖': lambda: self.push_strict(4),
            '밗': lambda: self.push_strict(4),
            '반': lambda: self.push_strict(2),
            '밙': lambda: self.push_strict(5),
            '밚': lambda: self.push_strict(5),
            '받': lambda: self.push_strict(3),
            '발': lambda: self.push_strict(5),
            '밝': lambda: self.push_strict(7),
            '밞': lambda: self.push_strict(9),
            '밟': lambda: self.push_strict(9),
            '밠': lambda: self.push_strict(7),
            '밡': lambda: self.push_strict(9),
            '밢': lambda: self.push_strict(9),
            '밣': lambda: self.push_strict(8),
            '밤': lambda: self.push_strict(4),
            '밥': lambda: self.push_strict(4),
            '밦': lambda: self.push_strict(6),
            '밧': lambda: self.push_strict(2),
            '밨': lambda: self.push_strict(4),
            '방': lambda: self.push(input_num()),
            '밪': lambda: self.push_strict(3),
            '밫': lambda: self.push_strict(4),
            '밬': lambda: self.push_strict(3),
            '밭': lambda: self.push_strict(4),
            '밮': lambda: self.push_strict(4),
            '밯': lambda: self.push(input_char()),
            '빠': self.duplicate,
            '타': self.sub,
        }
        for command in commands:
            aheui_command_map[command]()
