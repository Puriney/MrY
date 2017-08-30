'''
List available installations at root_dir
'''
import os
import yaml
import glob
from tabulate import tabulate
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


def list_avail(args):
    with open(get_species_name_fpath(fname='species_name.yaml'), 'rt') as fin:
        preset = yaml.load(fin)
        SPECIES_SUPPORTED = preset.get('common_scientific_name_pairs',
                                       dict()).keys()
        ORG_SUPPORTED = preset.get('supported_orgs', list())

    species = args.get('species', SPECIES_SUPPORTED)
    org = args.get('org', ORG_SUPPORTED)
    assembly = args.get('assembly', [])
    release = args.get('release', [])

    ROOTDIR = args.get('root_dir', '.')

    # rootdir/type/org/assembly/release/file => [org, assembly, release, file]
    genome_fagz_avail = map(lambda fpath: fpath
                            .replace(jpath(ROOTDIR, 'genome', os.sep), '')
                            .split(os.sep),
                            glob.iglob(jpath(ROOTDIR, 'genome',
                                             '*', '*', '*',
                                             '*.fa.gz')))
    genome_fa_avail = map(lambda x: base_name(x, ext='gz'),
                          genome_fagz_avail)

    gtf_avail = map(lambda fpath: fpath
                    .replace(jpath(ROOTDIR, 'annotation', os.sep), '')
                    .split(os.sep),
                    glob.iglob(jpath(ROOTDIR, 'annotation',
                                     '*', '*', '*',
                                     '*.gtf.gz')))
    gff_avail = map(lambda fpath: fpath
                    .replace(jpath(ROOTDIR, 'annotation', os.sep), '')
                    .split(os.sep),
                    glob.iglob(jpath(ROOTDIR, 'annotation',
                                     '*', '*', '*',
                                     '*.gff3.gz')))
    # 1.bt2, .2.bt2, .3.bt2, .4.bt2, .rev.1.bt2, .rev.2.bt2
    bowtie_avail = map(lambda fpath: fpath
                       .replace(jpath(ROOTDIR, 'aligner_index', 'bowtie2',
                                      os.sep), '')
                       .split(os.sep),
                       glob.iglob(jpath(ROOTDIR, 'aligner_index', 'bowtie2',
                                        '*', '*', '*',
                                        '*.gff3.gz')))
    star_avail = []
