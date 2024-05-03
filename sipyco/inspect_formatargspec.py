from inspect import formatannotation

def inspect_formatargspec(
        args, varargs=None, varkw=None, defaults=None,
        kwonlyargs=(), kwonlydefaults={}, annotations={},
        formatarg=str,
        formatvarargs=lambda name: '*' + name,
        formatvarkw=lambda name: '**' + name,
        formatvalue=lambda value: '=' + repr(value),
        formatreturns=lambda text: ' -> ' + text,
        formatannotation=formatannotation):
    """Copy formatargspec from python 3.7 standard library.
    Python 3 has deprecated formatargspec and requested that Signature
    be used instead, however this requires a full reimplementation
    of formatargspec() in terms of creating Parameter objects and such.
    Instead of introducing all the object-creation overhead and having
    to reinvent from scratch, just copy their compatibility routine.
    Utimately we would need to rewrite our "decorator" routine completely
    which is not really worth it right now, until all Python 2.x support
    is dropped.
    """
    def formatargandannotation(arg):
        result = formatarg(arg)
        if arg in annotations:
            result += ': ' + formatannotation(annotations[arg])
        return result
    specs = []
    if defaults:
        firstdefault = len(args) - len(defaults)
    for i, arg in enumerate(args):
        spec = formatargandannotation(arg)
        if defaults and i >= firstdefault:
            spec = spec + formatvalue(defaults[i - firstdefault])
        specs.append(spec)
    if varargs is not None:
        specs.append(formatvarargs(formatargandannotation(varargs)))
    else:
        if kwonlyargs:
            specs.append('*')
    if kwonlyargs:
        for kwonlyarg in kwonlyargs:
            spec = formatargandannotation(kwonlyarg)
            if kwonlydefaults and kwonlyarg in kwonlydefaults:
                spec += formatvalue(kwonlydefaults[kwonlyarg])
            specs.append(spec)
    if varkw is not None:
        specs.append(formatvarkw(formatargandannotation(varkw)))
    result = '(' + ', '.join(specs) + ')'
    if 'return' in annotations:
        result += formatreturns(formatannotation(annotations['return']))
    return result
