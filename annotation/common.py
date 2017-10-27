# 2) hard-code books with double quotations:
# NOTE - Look into Frankenstein: Normally double, but single when inside written texts
# any new books with double quotation marks must be added to this list
DOUBLE_QUOTEMARKS = [
    'bh',
    'cc',
    'ge',
    'hm',
    'ttc',
    'na',
    'ss',
    'per',
    'prpr',
    'mp',
    'emma',
    'wwhite',
    'viviang',
    'vanity',
    'tess',
    'sybil',
    'prof',
    'pride',
    'persuasion',
    'native',
    'mill',
    'mary',
    'ladyaud',
    'jude',
    'jekyll',
    'jane',
    'frank',
    'dracula',
    'dorian',
    'deronda',
    'cran',
    'basker',
    'arma',
    'alli',
]

# Chillit corpus books
DOUBLE_QUOTEMARKS += [
    'alone',
    'beauty',
    'brass',
    'bunny',
    'canada',
    'carved',
    'clive',
    'coral',
    'crofton',
    'cuckoo',
    'daisy',
    'dominics',
    'dove',
    'dragons',
    'dreamdays',
    'duke',
    'enchanted',
    'eric',
    'fiord',
    'five',
    'flopsy',
    'forest',
    'girls',
    'goldenage',
    'gulliver',
    'holiday',
    'howwhy',
    'jackanapes',
    'jemima',
    'jessica',
    'jungle',
    'kidnap',
    'leila',
    'masterman',
    'mice',
    'mopsa',
    'mulgars',
    'overtheway',
    'pan',
    'peasant',
    'prigio',
    'princess',
    'prince',
    'railway',
    'rival',
    'secret',
    'settlers',
    'solomons',
    'squirrel',
    'stalky',
    'stiria',
    'tapestry',
    'toadylion',
    'tombrown',
    'treasure',
    'unlikely',
    'vice',
    'wallypug',
    'water',
    'wind',
    'winning',
    'woodmagic',
]

# Other corpus books
DOUBLE_QUOTEMARKS += [
    'awakening',
    'carol',
    'heart',
    'huckleberry',
    'ladysusan',
    'maisie',
    'mansfield',
    'middlemarch',
    'moonstone',
    'northanger',
    'portraitone',
    'portraittwo',
    'room',
    'sense',
    'signfour',
    'silas',
    'soldier',
    'thejungle',
    'twelveyears',
    'war',
    'yellow',
]

def single_or_double(book):
    """
    Look up whether the book uses single or double quotation marks
    """
    return 'double' if book.lower() in DOUBLE_QUOTEMARKS else 'single'
