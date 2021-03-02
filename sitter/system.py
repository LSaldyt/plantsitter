import psutil

def to_dict(telem):
    data = dict()
    for field in dir(telem):
        if not field.startswith('_'):
            item = getattr(telem, field)
            if not callable(item):
                data[field] = item if item is not None else False
    return data

def _flatten(data, prefix=''):
    for k0, v0 in data.items():
        if isinstance(v0, dict):
            for k1, v1 in _flatten(v0, prefix=f'{prefix}{k0}_'): # Recursion
                yield k1, v1
        elif isinstance(v0, list):
            for i, v1 in enumerate(v0):
                pre = f'{prefix}{k0}_{i}_'
                if not isinstance(v1, dict) and not isinstance(v1, list):
                    yield pre, v1
                else:
                    for k2, v2 in _flatten(v1, prefix=pre): # Recursion
                        yield k2, v2
        else:
            yield f'{prefix}{k0}', v0

def flatten(data):
    return {k : v for k, v in _flatten(data)}

def extract(telem):
    return flatten(to_dict(telem))

def snapshot():
    snap = dict()
    for i, p in enumerate(psutil.cpu_percent(interval=0.01, percpu=True)):
        snap[f'cpu_{i}_percent'] = p

    temp = psutil.sensors_temperatures()['cpu-thermal']
    snap[f'cpu_temp'] = temp[0].current
    snap['memory']    = extract(psutil.virtual_memory())
    snap['swap']      = extract(psutil.swap_memory())
    snap['storage']   = extract(psutil.disk_usage('/'))
    snap['disk_io']   = extract(psutil.disk_io_counters(perdisk=False))
    snap['net']       = flatten({k : to_dict(v) 
                              for k, v in 
                              psutil.net_io_counters(pernic=True).items()})
    return flatten(snap)
