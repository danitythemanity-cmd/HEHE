"""Fictional review sample. Reads no client files and uses no network."""
import json

LIMIT_LOW = -(2**63)
LIMIT_HIGH = 2**63 - 1

def original(raw):
    obj = json.loads(raw)
    if obj['op'] != 'add':
        raise ValueError('op')
    a, b = obj['a'], obj['b']
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError('integer')
    return a + b

def reject_constant(value):
    raise ValueError('non-standard JSON constant')

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate key')
        result[key] = value
    return result

def revised(raw):
    obj = json.loads(raw, parse_constant=reject_constant,
                     object_pairs_hook=unique_object)
    if type(obj) is not dict or set(obj) != {'op', 'a', 'b'}:
        raise ValueError('object fields')
    if obj['op'] != 'add':
        raise ValueError('op')
    a, b = obj['a'], obj['b']
    if type(a) is not int or type(b) is not int:
        raise ValueError('integer token required')
    if not all(LIMIT_LOW <= n <= LIMIT_HIGH for n in (a, b)):
        raise ValueError('operand range')
    result = a + b
    if not LIMIT_LOW <= result <= LIMIT_HIGH:
        raise ValueError('result range')
    return result

# Expected results are stated independently of either implementation.
CASES = [
    ('ordinary', '{"op":"add","a":2,"b":3}', 5),
    ('negative', '{"op":"add","a":-7,"b":2}', -5),
    ('zero', '{"op":"add","a":0,"b":0}', 0),
    ('upper-bound', '{"op":"add","a":9223372036854775807,"b":0}', 9223372036854775807),
    ('lower-bound', '{"op":"add","a":-9223372036854775808,"b":0}', -9223372036854775808),
    ('large-cancel', '{"op":"add","a":9223372036854775807,"b":-9223372036854775808}', -1),
    ('boolean', '{"op":"add","a":true,"b":2}', 'REJECT'),
    ('boolean-false', '{"op":"add","a":0,"b":false}', 'REJECT'),
    ('string', '{"op":"add","a":"2","b":3}', 'REJECT'),
    ('float-token', '{"op":"add","a":2.0,"b":3}', 'REJECT'),
    ('exponent-token', '{"op":"add","a":2e0,"b":3}', 'REJECT'),
    ('null', '{"op":"add","a":null,"b":3}', 'REJECT'),
    ('missing', '{"op":"add","a":2}', 'REJECT'),
    ('unknown-field', '{"op":"add","a":2,"b":3,"extra":4}', 'REJECT'),
    ('duplicate-key', '{"op":"add","a":1,"a":9,"b":2}', 'REJECT'),
    ('upper-operand', '{"op":"add","a":9223372036854775808,"b":-1}', 'REJECT'),
    ('lower-operand', '{"op":"add","a":-9223372036854775809,"b":1}', 'REJECT'),
    ('overflow', '{"op":"add","a":9223372036854775807,"b":1}', 'REJECT'),
    ('underflow', '{"op":"add","a":-9223372036854775808,"b":-1}', 'REJECT'),
    ('wrong-operation', '{"op":"multiply","a":2,"b":3}', 'REJECT'),
    ('array-top-level', '[2,3]', 'REJECT'),
    ('null-top-level', 'null', 'REJECT'),
    ('trailing-data', '{"op":"add","a":2,"b":3}{}', 'REJECT'),
    ('malformed', '{"op":"add",}', 'REJECT'),
    ('nan-hidden', '{"op":"add","a":2,"b":3,"extra":NaN}', 'REJECT'),
    ('infinity', '{"op":"add","a":Infinity,"b":3}', 'REJECT'),
]

def run(fn):
    failed = []
    for name, raw, expected in CASES:
        try:
            actual = fn(raw)
        except (ValueError, KeyError, TypeError):
            actual = 'REJECT'
        if actual != expected:
            failed.append({'case': name, 'expected': expected, 'actual': actual})
    return {'cases': len(CASES), 'passed': len(CASES)-len(failed), 'failures': failed}

if __name__ == '__main__':
    before, after = run(original), run(revised)
    print(json.dumps({'original': before, 'revised': after}, indent=2))
    assert before['failures'], 'The sample must demonstrate observed defects.'
    assert not after['failures'], 'The revision must satisfy every fixture.'

