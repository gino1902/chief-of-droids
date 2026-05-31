# Python Basics — Refresher (2026)

Language fundamentals, dense. Assumes you program (Node/JS background). Designed so the Databricks doc reads effortlessly after this.

---

## 0. Five things that trip up JS people

1. **Indentation is syntax.** No braces. 4 spaces per level, consistently. Mixing tabs and spaces is a syntax error.
2. **`None`, not `null`.** And `True` / `False` are capitalized.
3. **`==` compares values; `is` compares identity.** Use `is` only for `None`/`True`/`False`/singletons.
4. **No `var`/`let`/`const`.** Just assignment. Variables are untyped bindings to objects.
5. **No implicit type coercion.** `"2" + 2` raises; `1 == "1"` is `False`. Python refuses to guess.

---

## 1. Running Python, variables, comments

```python
# A comment
x = 42              # int, no type declaration
y: int = 42         # same, with a type hint (decorative at runtime)
name = "Gilles"
ok = True
nothing = None

print(x, name)      # 42 Gilles
```

Multiple assignment and swap:

```python
a, b = 1, 2
a, b = b, a           # swap, no temp var
x = y = z = 0         # chain
first, *rest = [1,2,3,4]   # first=1, rest=[2,3,4]
```

---

## 2. Primitive types

| Type      | Example               | Notes                                      |
|-----------|-----------------------|--------------------------------------------|
| `int`     | `42`, `-3`, `1_000_000` | Arbitrary precision. `_` is a separator.  |
| `float`   | `3.14`, `1e-3`        | Double-precision. `math.inf`, `math.nan`.  |
| `bool`    | `True`, `False`       | Subtype of `int`: `True == 1`.             |
| `str`     | `"hi"`, `'hi'`        | Immutable. Unicode native.                  |
| `bytes`   | `b"hi"`               | Immutable byte sequence.                    |
| `None`    | `None`                | The null/absence value.                     |

Casts are explicit constructors:

```python
int("42")      # 42
float("3.14")  # 3.14
str(42)        # "42"
bool(0)        # False
bool("")       # False
bool("no")     # True (non-empty string is truthy)
```

---

## 3. Strings — you'll use f-strings constantly

```python
name = "Gilles"
msg = f"hello {name}, you have {3+4} messages"
# 'hello Gilles, you have 7 messages'

# Format specs after a colon
pi = 3.14159
f"{pi:.2f}"     # '3.14'
f"{1000000:,}"  # '1,000,000'
f"{0.12:.0%}"   # '12%'
f"{'hi':>10}"   # '        hi'  (right-align width 10)

# Debug form (3.8+): prints the expression and its value
n = 42
f"{n=}"         # 'n=42'

# Triple-quoted (multi-line)
sql = f"""
select *
from {table}
where d = '{date}'
"""
```

Common string methods:

```python
s = "  Hello, World!  "
s.strip()              # "Hello, World!"
s.lower()              # "  hello, world!  "
s.upper()
s.replace("World","Py")
s.split(",")           # ['  Hello', ' World!  ']
",".join(["a","b","c"]) # 'a,b,c'
s.startswith("Hello")   # False (leading spaces)
"abc" in "xabcy"        # True
len(s)
```

Strings are immutable: methods return new strings.

---

## 4. Numbers and operators

```python
10 / 3      # 3.333...   (always float)
10 // 3     # 3          (floor division)
10 % 3      # 1          (modulo)
2 ** 10     # 1024       (power — not ^)
abs(-5)     # 5
round(3.567, 1)  # 3.6
```

Bitwise: `& | ^ ~ << >>`. Math functions: `import math` → `math.sqrt`, `math.log`, `math.floor`, `math.ceil`.

---

## 5. Booleans, truthiness, None

Falsy values: `False`, `None`, `0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()`. Everything else is truthy.

```python
if items:           # idiomatic: non-empty list?
    ...
if name:            # idiomatic: non-empty string?
    ...

a and b             # short-circuit: returns a if falsy, else b
a or b              # returns a if truthy, else b
not a

x is None           # preferred over x == None
x is not None
```

Chained comparisons (unique to Python):

```python
if 0 <= age < 18:   # reads like math
    ...
```

---

## 6. Collections — the four essentials

### list — ordered, mutable, heterogeneous

```python
xs = [1, 2, 3]
xs.append(4)          # [1,2,3,4]
xs.extend([5,6])      # [1,2,3,4,5,6]
xs.insert(0, 0)
xs.pop()              # removes & returns last
xs.pop(0)             # removes & returns at index
xs.remove(3)          # removes first occurrence of 3
xs[0]                 # 0
xs[-1]                # last element
xs[1:3]               # slice [start:stop) — a new list
xs[::2]               # every 2nd element
xs[::-1]              # reversed copy
len(xs)
3 in xs               # membership
sorted(xs)            # new sorted list
xs.sort()             # in-place sort
```

Slicing works on any sequence (list, tuple, str, bytes).

### tuple — ordered, **immutable**, often heterogeneous

```python
point = (3, 4)
x, y = point          # unpacking
single = (1,)         # trailing comma for 1-tuple
empty = ()
```

Use tuples for fixed records, function returns, dict keys. Cheaper than lists.

### dict — hash map, keys → values, ordered since 3.7

```python
d = {"name": "Gilles", "age": 40}
d["name"]             # KeyError if missing
d.get("name")         # None if missing
d.get("city", "Lyon") # default if missing
d["city"] = "Lyon"    # insert/update
del d["age"]
"name" in d           # membership checks keys

for k, v in d.items():
    ...
for k in d:           # iterates keys
    ...
list(d.keys()), list(d.values())
d | {"x": 1}          # merge, returns new dict (3.9+)
```

### set — unordered, unique elements

```python
s = {1, 2, 3}
s.add(4)
s.discard(2)          # no error if missing
s & other             # intersection
s | other             # union
s - other             # difference
s ^ other             # symmetric difference
3 in s                # O(1) membership
empty = set()         # {} is an empty dict, not a set
```

**Rule of thumb**: if you're about to write `if x in list` and the list is big, switch to a set.

---

## 7. Control flow

```python
# if / elif / else
if x > 0:
    ...
elif x == 0:
    ...
else:
    ...

# Ternary
label = "adult" if age >= 18 else "minor"

# while
while queue:
    item = queue.pop()
    ...

# for — always iterates over something (no C-style for)
for i in range(10):          # 0..9
    ...
for i in range(2, 10, 2):    # 2,4,6,8
    ...
for name in names:
    ...
for i, name in enumerate(names):
    ...
for a, b in zip(xs, ys):
    ...
for k, v in d.items():
    ...

# break / continue behave as expected
# for...else: runs `else` if loop completed without break (quirky; rarely needed)
```

`range(stop)`, `range(start, stop)`, `range(start, stop, step)` — `stop` is exclusive.

---

## 8. Structural pattern matching (`match` / `case`, 3.10+)

Not `switch`. It destructures.

```python
def handle(msg):
    match msg:
        case {"type": "ping"}:                    return "pong"
        case {"type": "add", "n": int(n)}:        return n + 1
        case [x, y, *rest]:                       return (x, y, rest)
        case str() as s if s.startswith("!"):     return s.upper()
        case _:                                   return "unknown"
```

Patterns:
- `literal` — matches equal values
- `name` — binds (captures) the value
- `ClassName(a, b)` / `ClassName(x=...)` — matches type + destructures
- `[a, b, *rest]` / `(a, b)` — sequence
- `{"key": pattern}` — mapping (matches subset; extras ignored)
- `p1 | p2` — OR pattern
- `_` — wildcard (no binding)
- `case X if cond:` — guard

---

## 9. Functions

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"

greet("Gilles")                  # positional
greet("Gilles", "Bonjour")       # positional
greet(name="Gilles")             # keyword
greet(greeting="Salut", name="G")  # order free with keywords
```

### `*args`, `**kwargs`

```python
def f(*args, **kwargs):
    # args is a tuple, kwargs is a dict
    print(args, kwargs)

f(1, 2, x=3, y=4)     # (1,2) {'x':3,'y':4}

# Forwarding
def wrap(*args, **kwargs):
    return f(*args, **kwargs)
```

Also unpack at call sites:

```python
nums = [1, 2, 3]
print(*nums)              # print(1, 2, 3)

opts = {"sep": "-", "end": "!\n"}
print("a", "b", **opts)
```

### Positional-only and keyword-only

```python
def f(a, b, /, c, d, *, e, f):
    # a,b positional-only   (before /)
    # c,d either
    # e,f keyword-only      (after *)
    ...
```

Rarely write these yourself; you'll see them in stdlib signatures.

### Default args — the classic trap

```python
def bad(xs=[]):       # DON'T. Default is evaluated once and shared across calls.
    xs.append(1)
    return xs

def good(xs=None):
    xs = [] if xs is None else xs
    xs.append(1)
    return xs
```

Same trap with `{}`. Rule: never use mutable defaults.

### Lambdas — anonymous one-expression functions

```python
square = lambda x: x * x
sorted(pairs, key=lambda p: p[1])
```

Use sparingly; a named `def` is usually clearer.

### Return values and tuples

```python
def stats(xs):
    return min(xs), max(xs), sum(xs) / len(xs)

lo, hi, avg = stats([1,2,3,4])
```

`return` without a value returns `None`. No return at all → `None`.

---

## 10. Scope — LEGB

Name resolution order: **Local → Enclosing → Global → Built-in**.

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        # x refers to the enclosing x
        print(x)
    inner()

outer()   # prints "enclosing"
```

To **assign** a name to a non-local scope: `nonlocal` (enclosing function) or `global` (module). You rarely need either.

Closures capture by reference:

```python
def make_adder(n):
    def add(x): return x + n
    return add

plus5 = make_adder(5)
plus5(3)    # 8
```

---

## 11. Comprehensions — core idiom

```python
# List comprehension
squares = [x*x for x in range(10)]
evens   = [x for x in xs if x % 2 == 0]
pairs   = [(x, y) for x in xs for y in ys if x != y]

# Dict comprehension
by_id = {u.id: u for u in users}
inv   = {v: k for k, v in d.items()}

# Set comprehension
seen  = {x.key for x in events}

# Generator expression (no brackets, parens) — lazy
total = sum(x*x for x in range(1000))
```

Rule: use comprehensions for transform/filter. Use a `for` loop when logic has side effects or is more than one-line-readable.

---

## 12. Iterators and generators

**Iterable** = thing you can loop over. **Iterator** = thing with `__next__`, remembers where it is.

Any `for x in X` calls `iter(X)` then `next(...)` until `StopIteration`.

```python
it = iter([1,2,3])
next(it)   # 1
next(it)   # 2
next(it)   # 3
next(it)   # raises StopIteration
```

### Generator functions — the Python superpower

A function with `yield` returns a lazy iterator. Each `yield` pauses the function, remembering state.

```python
def count_up(n):
    i = 0
    while i < n:
        yield i
        i += 1

for x in count_up(3):    # 0, 1, 2
    print(x)
```

Great for streaming (don't materialize huge lists):

```python
def lines_of(path):
    with open(path) as f:
        for line in f:
            yield line.rstrip()

for line in lines_of("big.log"):
    process(line)
```

`yield from` delegates:

```python
def chain(a, b):
    yield from a
    yield from b
```

---

## 13. Exceptions

```python
try:
    risky()
except ValueError as e:
    print("bad value:", e)
except (KeyError, IndexError):
    ...
except Exception as e:      # catches anything except SystemExit/KeyboardInterrupt
    ...
else:
    # runs if no exception
    ...
finally:
    # always runs
    cleanup()
```

Raising:

```python
if n < 0:
    raise ValueError(f"n must be non-negative, got {n}")

# Re-raise preserving traceback
try:
    ...
except SomeError:
    raise
# Or chain a new one
except SomeError as e:
    raise RuntimeError("wrapping") from e
```

Common built-in exceptions: `ValueError`, `TypeError`, `KeyError`, `IndexError`, `FileNotFoundError`, `ZeroDivisionError`, `AttributeError`, `RuntimeError`, `StopIteration`.

Define your own:

```python
class DomainError(Exception): ...
class OrderNotFound(DomainError): ...
```

---

## 14. Classes — basic OO

```python
class Order:
    # class attribute (shared across instances)
    tax_rate = 0.2

    def __init__(self, id: str, amount: float):
        # instance attributes
        self.id = id
        self.amount = amount

    def total(self) -> float:
        return self.amount * (1 + self.tax_rate)

    def __repr__(self) -> str:
        return f"Order(id={self.id!r}, amount={self.amount})"

o = Order("A1", 100)
o.total()        # 120.0
print(o)         # Order(id='A1', amount=100)
```

Key conventions:
- `self` is always the first parameter of instance methods (explicit).
- `_name` = "internal, leave alone" (convention, not enforced).
- `__name` = name-mangled (rarely needed).
- `__dunder__` = language hooks (see below).

### Useful dunder methods

| Dunder               | Triggers                     |
|----------------------|------------------------------|
| `__init__`           | `Order(...)`                 |
| `__repr__`           | `repr(x)`, REPL display, debugging |
| `__str__`            | `str(x)`, `print(x)`         |
| `__eq__`, `__hash__` | `==`, set/dict key usage     |
| `__lt__`, etc.       | `<`, sorting                 |
| `__len__`            | `len(x)`                     |
| `__iter__`           | `for y in x`                 |
| `__getitem__`        | `x[k]`                       |
| `__call__`           | `x(...)` — makes instance callable |

### Classmethod and staticmethod

```python
class Order:
    @classmethod
    def from_dict(cls, d):         # factory
        return cls(d["id"], d["amount"])

    @staticmethod
    def is_valid_id(s):            # pure utility, no self/cls
        return s.isalnum()
```

### Inheritance

```python
class Animal:
    def speak(self): return "..."

class Dog(Animal):
    def speak(self): return "woof"

class Puppy(Dog):
    def speak(self):
        return super().speak() + "!"
```

Python allows multiple inheritance. MRO (method resolution order) via C3 linearization. Use sparingly; mixins are the main legitimate use case.

---

## 15. Dataclasses — 90% of the classes you'll write

```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float = 0.0

p = Point(3, 4)
p.x, p.y
p == Point(3, 4)      # True — auto __eq__

@dataclass(frozen=True, slots=True)
class Config:
    host: str
    port: int = 5432
    tags: list[str] = field(default_factory=list)  # for mutable defaults
```

- `frozen=True` → immutable (hashable, safe as dict key/set member).
- `slots=True` → memory-compact, faster attribute access.
- `field(default_factory=list)` → the correct way to default a mutable.

For validation/coercion at IO boundaries, reach for `pydantic` instead.

---

## 16. Modules and imports

One file = one module. A folder with `__init__.py` (or marked as package) = a package.

```python
import math
math.sqrt(16)

from math import sqrt, pi
sqrt(16)

from math import sqrt as msqrt

from mypkg.utils import helper
from . import sibling             # relative (inside a package)
```

Each module runs once; subsequent imports hit the cache.

```python
# my_script.py
def main(): ...

if __name__ == "__main__":
    main()
```

`__name__ == "__main__"` is `True` only when the file is run directly, not when imported. Lets a module be both a library and a script.

---

## 17. File IO and `with`

```python
with open("data.txt", "r", encoding="utf-8") as f:
    text = f.read()
    # or: for line in f: ...

with open("out.txt", "w", encoding="utf-8") as f:
    f.write("hello\n")
```

`with` guarantees cleanup (close) even on exceptions. Always prefer over manual `open`/`close`.

Modes: `"r"` read (default), `"w"` write (truncates), `"a"` append, `"b"` binary, `"+"` read+write.

---

## 18. Context managers

Any object with `__enter__` / `__exit__` works with `with`. The easy way to make one:

```python
from contextlib import contextmanager

@contextmanager
def timing(label):
    import time
    t = time.perf_counter()
    try:
        yield          # code inside `with` runs here
    finally:
        print(f"{label}: {time.perf_counter() - t:.3f}s")

with timing("query"):
    run_query()
```

Everything before `yield` is setup; everything after is teardown. Teardown runs even if the `with` body raises.

---

## 19. Decorators

A decorator is a function that takes a function and returns a function.

```python
def trace(fn):
    def wrapper(*args, **kwargs):
        print(f"calling {fn.__name__}")
        result = fn(*args, **kwargs)
        print(f"-> {result}")
        return result
    return wrapper

@trace
def add(a, b):
    return a + b

add(2, 3)
# calling add
# -> 5
```

`@trace` is sugar for `add = trace(add)`.

Preserve metadata with `functools.wraps`:

```python
from functools import wraps

def trace(fn):
    @wraps(fn)                        # keeps __name__, __doc__, signature
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper
```

Decorators with arguments are decorator factories:

```python
def retry(times):
    def deco(fn):
        @wraps(fn)
        def wrapper(*a, **kw):
            last = None
            for _ in range(times):
                try: return fn(*a, **kw)
                except Exception as e: last = e
            raise last
        return wrapper
    return deco

@retry(3)
def fetch(): ...
```

Decorators you'll constantly see: `@property`, `@staticmethod`, `@classmethod`, `@dataclass`, `@functools.lru_cache`, `@contextmanager`, `@pytest.fixture`.

---

## 20. Type hints — the quick version

```python
x: int = 3
name: str = "g"
flag: bool = True
xs: list[int] = [1, 2]
d: dict[str, int] = {"a": 1}
t: tuple[int, str] = (1, "a")
tn: tuple[int, ...] = (1, 2, 3)      # variable-length
maybe: int | None = None
from collections.abc import Iterable, Callable
xs: Iterable[int]
cb: Callable[[int, str], bool]
```

Function signatures:

```python
def enrich(rows: list[dict], *, tag: str = "") -> list[dict]:
    ...
```

Hints are not enforced at runtime. They document intent and are checked by tools (`pyright`, `mypy`) and used by IDEs for completion. Worth adding on public function signatures; skip in throwaway scripts.

---

## 21. The built-ins worth memorizing

```python
len(x)                  # length of any sized collection
range(n), range(a, b, step)

enumerate(xs)           # yields (index, item)
zip(xs, ys)             # yields (x, y) pairs — stops at shortest
zip(xs, ys, strict=True)  # 3.10+: raise if lengths differ

sorted(xs)              # new sorted list
sorted(xs, key=lambda x: x.name, reverse=True)
reversed(xs)
min(xs), max(xs), sum(xs)

any(xs), all(xs)        # short-circuiting boolean folds
map(fn, xs)             # lazy; usually prefer comprehension
filter(fn, xs)          # lazy; usually prefer comprehension

isinstance(x, int)
isinstance(x, (int, float))     # tuple = "any of these"
type(x)                         # prefer isinstance for checks

id(x)                   # object identity
hash(x)                 # for hashable types

print("a", "b", sep="-", end="!\n")
repr(x), str(x)
```

---

## 22. Equality vs identity

```python
a = [1, 2]
b = [1, 2]
a == b        # True  — value equality
a is b        # False — different objects

n = None
x is None     # prefer for None (and True/False)
```

CPython interns small ints and short strings, so `is` sometimes accidentally returns `True` — never rely on that.

---

## 23. Mutability — the thing that bites everyone eventually

Mutable: `list`, `dict`, `set`, most objects. Immutable: `int`, `float`, `bool`, `str`, `tuple`, `frozenset`, `None`.

```python
a = [1, 2, 3]
b = a              # same object
b.append(4)
a                  # [1,2,3,4]  — surprise

b = a.copy()       # shallow copy
b = a[:]           # also shallow

import copy
b = copy.deepcopy(a)   # deep copy for nested structures
```

This is why mutable default args are a trap (see §9) and why `frozen=True` on dataclasses is useful for value objects.

---

## 24. Style and naming conventions (PEP 8)

- `snake_case` for functions, methods, variables, modules.
- `PascalCase` for classes.
- `UPPER_SNAKE` for constants.
- `_leading_underscore` = "internal".
- 4-space indent, lines ~88–100 cols (ruff/black default).
- Imports: stdlib, then 3rd-party, then local — separated by blank lines.
- No trailing semicolons. No braces. Let the indentation speak.

Run `ruff format` and `ruff check` — it settles all style debates for you.

---

## 25. The stdlib modules worth knowing by name

| Module       | For                                      |
|--------------|------------------------------------------|
| `pathlib`    | File paths (`Path("/tmp") / "x.txt"`)    |
| `os`         | Env vars, process, filesystem (old-school) |
| `sys`        | argv, exit, stdin/stdout                 |
| `json`       | JSON parse/serialize                     |
| `csv`        | CSV read/write                           |
| `datetime`   | Dates/times (+ `zoneinfo` for TZ)        |
| `re`         | Regex                                    |
| `itertools`  | `chain`, `groupby`, `islice`, `batched`  |
| `functools`  | `wraps`, `lru_cache`, `partial`, `reduce` |
| `collections`| `defaultdict`, `Counter`, `deque`, `namedtuple` |
| `dataclasses`| `@dataclass`, `field`                    |
| `typing` / `collections.abc` | `Iterable`, `Callable`, `Protocol` |
| `contextlib` | `contextmanager`, `suppress`             |
| `logging`    | Structured logging                       |
| `subprocess` | Running shell commands                   |
| `asyncio`    | Async IO (covered later if needed)       |

---

## 26. Five idioms that make code look "Pythonic"

1. **`for x in xs:`**, not `for i in range(len(xs))`.
2. **`if not items:`**, not `if len(items) == 0`.
3. **`value = a if cond else b`**, not multi-line if-else for assignment.
4. **Comprehensions over `map`/`filter`** for building collections.
5. **Unpack returns**: `name, count = parse(line)`.

---

## 27. Read-through test — can you parse this?

If this all reads naturally, you're solid for the Databricks doc:

```python
from dataclasses import dataclass, field
from functools import wraps
from collections.abc import Iterable

@dataclass(frozen=True, slots=True)
class Order:
    id: str
    lines: list[dict] = field(default_factory=list)

    @property
    def total(self) -> float:
        return sum(l["qty"] * l["price"] for l in self.lines)

def log_calls(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        print(f"-> {fn.__name__}")
        return fn(*args, **kwargs)
    return inner

@log_calls
def summarize(orders: Iterable[Order]) -> dict[str, float]:
    return {o.id: o.total for o in orders if o.total > 0}

orders = [
    Order("A1", [{"qty": 2, "price": 10.0}]),
    Order("A2", [{"qty": 1, "price": 5.0}, {"qty": 3, "price": 2.0}]),
]
print(summarize(orders))
# -> summarize
# {'A1': 20.0, 'A2': 11.0}
```

If any line gave you pause, jump back to the corresponding section. Otherwise, the Databricks doc is now comfortable territory.
