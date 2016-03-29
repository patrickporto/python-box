def force_unicode(s, encoding='utf-8', errors='ignore'):
    if s is None:
        return ''
    try:
        if not isinstance(s, basestring,):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                try:
                    s = unicode(str(s), encoding, errors)
                except UnicodeEncodeError:
                    if not isinstance(s, Exception):
                        raise
                    s = ' '.join([force_unicode(arg, encoding, errors) for arg in s])
        elif not isinstance(s, unicode):
            s = s.decode(encoding, errors)
    except UnicodeDecodeError, e:
        if not isinstance(s, Exception):
            raise UnicodeDecodeError(s, *e.args)
        else:
            s = ' '.join([force_unicode(arg, encoding, errors) for arg in s])
    return s
