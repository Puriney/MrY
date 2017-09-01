'''
List available installations at root_dir
'''
import os
import glob
from tabulate import tabulate
from collections import defaultdict, OrderedDict
from operator import itemgetter
from MrY import join_path as jpath


'''

Example Output:

Org=GECODE
Species Assembly Release Genome.Fasta Genome.Fasta.gz GTF GFF3 Bowtie2 STAR
human GRCh38 90 Yes Yes No No Yes No No
'''


def tag_installed(filelist=[]):
    tag = OrderedDict({'Genome (.fa)': False,
                       # 'Genome(.fa.gz)': True,
                       'Annotation (.gtf)': False, 'Annotation (.gff3)': False,
                       'Bowtie2': False, 'STAR': False})
    for f in filelist:
        if f.endswith('.fa'):
            tag['Genome (.fa)'] = True
        # elif f.endswith('.fa.gz'):
        #     tag['Genome(.fa.gz)'] = True
        elif f.endswith('.gtf'):
            tag['Annotation (.gtf)'] = True
        elif f.endswith('.gff3'):
            tag['Annotation (.gff3)'] = True
        elif f.endswith('.bt2'):
            tag['Bowtie2'] = True
        elif f.endswith('SA'):
            tag['STAR'] = True
        else:
            continue
    return(tag)


def list_avail(args):

    args = vars(args)
    species = args.get('species')
    org = args.get('org')
    assembly = args.get('assembly')
    release = args.get('release')

    ROOTDIR = args.get('root_dir')

    savetofile = args.get('snapshot', None)

    # ['rootdir/species/type/org/assembly/release/file'] =>
    # [['species', 'org', 'assembly', 'release', 'file']]
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
    # genome_fagz_avail = map(lambda fpath: fpath
    #                         .replace(ROOTDIR + os.sep, '')
    #                         .replace('genome' + os.sep, '')
    #                         .split(os.sep),
    #                         glob.iglob(jpath(ROOTDIR, '*',
    #                                          'genome',
    #                                          '*', '*', '*',
    #                                          '*.fa.gz')))
    gtf_avail = map(lambda fpath: fpath
                    .replace(ROOTDIR + os.sep, '')
                    .replace('annotation' + os.sep, '')
                    .split(os.sep),
                    glob.iglob(jpath(ROOTDIR, '*',
                                     'annotation',
                                     '*', '*', '*',
                                          '*.gtf')))
    gff3_avail = map(lambda fpath: fpath
                     .replace(ROOTDIR + os.sep, '')
                     .replace('annotation' + os.sep, '')
                     .split(os.sep),
                     glob.iglob(jpath(ROOTDIR, '*',
                                      'annotation',
                                      '*', '*', '*',
                                      '*.gff3')))
    # 1.bt2, .2.bt2, .3.bt2, .4.bt2, .rev.1.bt2, .rev.2.bt2
    bowtie_avail = map(lambda fpath: fpath
                       .replace(ROOTDIR + os.sep, '')
                       .replace(jpath('aligner_index', 'bowtie2') + os.sep, '')
                       .split(os.sep),
                       glob.iglob(jpath(ROOTDIR, '*',
                                        'aligner_index', 'bowtie2',
                                        '*', '*', '*',
                                        '*.rev.2.bt2')))
    # SA, SAindex, ...
    star_avail = map(lambda fpath: fpath
                     .replace(ROOTDIR + os.sep, '')
                     .replace(jpath('aligner_index', 'star') + os.sep, '')
                     .split(os.sep),
                     glob.iglob(jpath(ROOTDIR, '*',
                                      'aligner_index', 'star',
                                      '*', '*', '*',
                                      'SA')))
    table = []

    species_avail_subinfo = defaultdict(list)
    for info_avail in [genome_fa_avail,
                       # genome_fagz_avail,
                       gtf_avail, gff3_avail,
                       bowtie_avail, star_avail]:
        for info in info_avail:
            sp_org_asb_rel, fname = info[: len(info) - 1], info[-1]
            sp_org_asb_rel[-1] = sp_org_asb_rel[-1].replace('release_', '')
            sp_org_asb_rel = (os.sep).join(sp_org_asb_rel)
            species_avail_subinfo[sp_org_asb_rel].append(fname)

    for sp_org_asb_rel, fl in species_avail_subinfo.items():
        sp_org_asb_rel_tag = tag_installed(fl)
        species_avail_subinfo[sp_org_asb_rel] = sp_org_asb_rel_tag
        sp_org_asb_rel = sp_org_asb_rel.split(os.sep)
        sp_org_asb_rel[1], sp_org_asb_rel[2] = \
            sp_org_asb_rel[2], sp_org_asb_rel[1]
        sp_asb_org_rel = sp_org_asb_rel
        table.append(sp_asb_org_rel +
                     list(sp_org_asb_rel_tag.values()))

    table_header = ['Species', 'Assembly', 'Org', 'Release',
                    'Genome (.fa)',
                    # 'Genome (.fa.gz)',
                    'Annotation (.gtf)', 'Annotation (.gff3)',
                    'Bowtie2', 'STAR']

    table.sort(key=itemgetter(0, 1, 2, 3),
               reverse=True)  # sort by sp-assembly-org-release
    table = tabulate(table, headers=table_header, tablefmt="pipe")

    if savetofile:
        with open(savetofile, 'w') as fout:
            fout.write(table)
            fout.write('\n')

    print('=' * 10)
    if not species or not assembly or not org or not release:
        print('Specify species + assembly + org + release, if needed.')
    else:
        user_query = (os.sep).join([species[0], org[0],
                                    assembly[0], release[0]])

        print('{}-{}-{}-{} was queried:'.format(species[0], assembly[0],
                                                org[0], release[0]))
        for k, v in species_avail_subinfo.get(user_query,
                                              tag_installed()).items():
            print('\t{:>20}: {}'.format(
                k,
                'Installed' if v else 'Not-installed'))

    return(table)
