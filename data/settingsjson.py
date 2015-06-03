import json

settings_json_server = json.dumps([
    {'type':    'title',
     'title':   'ComicStream Server Settings'},

    {'type':    'string',
     'title':   'Server URL',
     'desc':    'URL for server',
     'section': 'Server',
     'key':     'url'},
    {'type':    'path',
     'title':   'Storage Directory',
     'desc':    'Where to store Comic Pages Buffer',
     'section': 'Server',
     'key':     'storagedir'}
    ])


settings_json_dispaly = json.dumps(
    [
     {'type':   'title',
     'title':   'Settings for how comic reader behaves'},

    {'type':    'bool',
     'title':   'Split Double Page',
     'desc':    'Split double pages into 2 slides',
     'section': 'Display',
     'key':     'dblpagesplit'},
    {
    'type':     'numeric',
    'title':    'Magnifying Glass Size',
    'desc':     'Size of Magnifying Glass Square on each side',
    'section':  'Display',
    'key':      'mag_glass_size'},
    ])




    #
    # {'type': 'bool',
    #  'title': 'A boolean setting',
    #  'desc': 'Boolean description text',
    #  'section': 'Server',
    #  'key': 'boolexample'},
    # {'type': 'numeric',
    #  'title': 'Page Buffer',
    #  'desc': 'How many pages to prefetch',
    #  'section': 'Server',
    #  'key': 'pagebuffer'},
    # {'type': 'options',
    #  'title': 'An options setting',
    #  'desc': 'Options description text',
    #  'section': 'Server',
    #  'key': 'optionsexample',
    #  'options': ['option1', 'option2', 'option3']},