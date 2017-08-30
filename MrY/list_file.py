'''
List available installations at root_dir
'''
import os
import yaml
import glob
from tabulate import tabulate
from collections import defaultdict, OrderedDict
from itertools import islice
from MrY import join_path as jpath
from MrY import base_name, dir_name
from MrY import print_logger
from MrY import get_species_name_fpath


'''

Example Output:

Org=GECODE
Species Assembly Release Genome.Fasta Genome.Fasta.gz GTF GFF3 Bowtie2 STAR
human GRCh38 90 Yes Yes No No Yes No No
'''


def tag_installed(filelist):
    tag = OrderedDict({'Genome(.fa)': False, 'Genome(.fa.gz)': False,
                       'GTF(.gtf.gz)': False, 'GFF3(.gff3.gz)': False,
                       'Bowtie2': False, 'STAR': False})
    for f in filelist:
        if f.endswith('.fa'):
            tag['Genome(.fa)'] = True
        elif f.endswith('.fa.gz'):
            tag['Genome(.fa.gz)'] = True
        elif f.endswith('.gtf.gz'):
            tag['GTF(.gtf.gz)'] = True
        elif f.endswith('.gff3.gz'):
            tag['GFF3(.gff3.gz)'] = True
        elif f.endswith('.bt2'):
            tag['Bowtie2'] = True
        elif f.endswith('.star'):  # to-do
            tag['STAR'] = True
        else:
            continue
    return(tag)


def list_avail(args):

    with open(get_species_name_fpath(fname='species_name.yaml'), 'rt') as fin:
        preset = yaml.load(fin)
        SPECIES_SUPPORTED = preset.get('common_scientific_name_pairs',
                                       dict()).keys()
        ORG_SUPPORTED = preset.get('supported_orgs', list())

    args = vars(args)
    species = args.get('species', SPECIES_SUPPORTED)
    org = args.get('org', ORG_SUPPORTED)
    assembly = args.get('assembly', [])
    release = args.get('release', [])

    ROOTDIR = args.get('root_dir', '.')

    savetofile = args.get('snapshot', None)

    # [rootdir/species/type/org/assembly/release/file] =>
    # [[species, org, assembly, release, file]]
    genome_fa_avail = map(lambda fpath: fpath
                          .replace(ROOTDIR + os.sep, '')
                          .replace('genome' + os.sep, '')
                          .split(os.sep),
                          glob.iglob(jpath(ROOTDIR, '*',
                                           'genome',
                                           '*', '*', '*',
                                                '*.fa')))
    # genome_fagz_avail = map(lambda x: x,
    #                         genome_fa_avail)
    genome_fagz_avail = map(lambda fpath: fpath
                            .replace(ROOTDIR + os.sep, '')
                            .replace('genome' + os.sep, '')
                            .split(os.sep),
                            glob.iglob(jpath(ROOTDIR, '*',
                                             'genome',
                                             '*', '*', '*',
                                             '*.fa.gz')))
    gtf_avail = map(lambda fpath: fpath
                    .replace(ROOTDIR + os.sep, '')
                    .replace('annotation' + os.sep, '')
                    .split(os.sep),
                    glob.iglob(jpath(ROOTDIR, '*',
                                     'annotation',
                                     '*', '*', '*',
                                          '*.gtf.gz')))
    gff3_avail = map(lambda fpath: fpath
                     .replace(ROOTDIR + os.sep, '')
                     .replace('annotation' + os.sep, '')
                     .split(os.sep),
                     glob.iglob(jpath(ROOTDIR, '*',
                                      'annotation',
                                      '*', '*', '*',
                                      '*.gff3.gz')))
    # 1.bt2, .2.bt2, .3.bt2, .4.bt2, .rev.1.bt2, .rev.2.bt2
    bowtie_avail = map(lambda fpath: fpath
                       .replace(ROOTDIR + os.sep, '')
                       .replace(jpath('aligner_index', 'bowtie2') + os.sep, '')
                       .split(os.sep),
                       glob.iglob(jpath(ROOTDIR, '*',
                                        'aligner_index', 'bowtie2',
                                        '*', '*', '*',
                                        '*.rev.2.bt2')))
    # to-do
    star_avail = []

    table = []
    species_avail_info = dict()
    species_avail_subinfo = defaultdict(list)
    for info_avail in [genome_fa_avail, genome_fagz_avail,
                       gtf_avail, gff3_avail,
                       bowtie_avail, star_avail]:
        for info in info_avail:
            sp, fname = info[0], info[-1]
            sp_org_asb_rel = info[: len(info) - 1]
            sp_org_asb_rel = '/'.join(sp_org_asb_rel)
            species_avail_info[sp] = sp_org_asb_rel
            species_avail_subinfo[sp_org_asb_rel].append(fname)

    for sp_org_asb_rel, fl in species_avail_subinfo.items():
        sp_org_asb_rel_tag = tag_installed(fl)
        species_avail_subinfo[sp_org_asb_rel] = sp_org_asb_rel_tag
        table.append(sp_org_asb_rel.split('/') +
                     list(sp_org_asb_rel_tag.values()))

    table_header = ['Species', 'Org', 'Assembly', 'Release',
                    'Genome(.fa)', 'Genome(.fa.gz)',
                    'GTF(.gtf.gz)', 'GFF3(.gff3.gz)',
                    'Bowtie2', 'STAR']

    table = tabulate(table, headers=table_header, tablefmt="rst")
    # table = tabulate(table)

    if savetofile:
        with open(savetofile, 'w') as fout:
            fout.write(table)
            fout.write('\n')
    return(table)
