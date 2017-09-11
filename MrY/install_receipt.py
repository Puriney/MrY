import yaml


def new_installation_receipt(fpath):
    receipt_dict = {
        'SPECIES': 'Salmonella_SL1344',
        'ASSEMBLY': 'ASM21085v2',
        'RELEASE': 'GCF_000210855.2',
        'ORG': 'NCBI',
        'LINK_FASTA': 'path/to/file',
        'LINK_GFF3': 'path/to/file',
        'LINK_GTF': 'path/to/file'
    }
    with open(fpath, 'w') as fout:
        yaml.dump(receipt_dict, fout)


def load_installation_receipt(fpath):
    with open(fpath, 'r') as fin:
        out = yaml.load(fin)
    assert set(['LINK_FASTA', 'LINK_GFF3', 'LINK_GTF']) == set(out.keys())
    return out

