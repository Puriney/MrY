import yaml
from collections import defaultdict
from MrY import print_logger as printl


def new_installation_receipt(fpath, num=1):
    '''
    [{'LINK_GENOME': '',
    'LINK_ANNOTATION': '',
    'assembly': '',
    'org': '',
    'release': '',
    'species': ''}]
    '''
    fout = open(fpath, 'w')
    for i in range(num):
        fout.write('- species: \'{}\'\n'.format(''))
        fout.write('  assembly: \'{}\'\n'.format(''))
        fout.write('  release: \'{}\'\n'.format(''))
        fout.write('  org: \'{}\'\n'.format(''))
        fout.write('  LINK_GENOME: \'{}\'\n'.format(''))
        fout.write('  LINK_ANNOTATION: \'{}\'\n'.format(''))
    fout.close()


def load_installation_receipt(fpath):
    res = defaultdict(list)
    with open(fpath, 'r') as fin:
        receipts = yaml.load(fin)
    i, j = 0, 0
    for receipt in receipts:
        i += 1
        if not set(receipt.values()) or set(receipt.values()) == set(['']):
            printl('Input item-{} is empty.'.format(i))
            continue
        j += 1
        res['species'].append(receipt['species'])
        res['assembly'].append(receipt['assembly'])
        res['release'].append(receipt['release'])
        res['org'].append(receipt['org'])
        res['LINK_GENOME'].append(receipt['LINK_GENOME'])
        res['LINK_ANNOTATION'].append(receipt['LINK_ANNOTATION'])
    printl('{}/{} genomes are to be installed.'.format(j, i))
    return res
