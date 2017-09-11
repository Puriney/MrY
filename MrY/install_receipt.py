import yaml


def new_installation_receipt(fpath):
    fout = open(fpath, 'w')
    fout.write('{}: {}'.format('root_dir', '.'))

    # receipt_dict = {
    #     'species': 'Salmonella_SL1344',
    #     'assembly': 'ASM21085v2',
    #     'release': 'GCF_000210855.2',
    #     'org': 'NCBI',
    #     'LINK_FASTA': 'path/to/file',
    #     'LINK_GFF3': 'path/to/file',
    #     'LINK_GTF': 'path/to/file'
    # }
    # with open(fpath, 'w') as fout:
    #     yaml.dump(receipt_dict, fout)


def load_installation_receipt(fpath):
    with open(fpath, 'r') as fin:
        out = yaml.load(fin)
    assert set(['LINK_FASTA', 'LINK_GFF3', 'LINK_GTF']) == set(out.keys())
    return out

