'''
Delete available installations at root_dir
'''
import glob
from MrY import join_path as jpath
from MrY import rmfile, rmfolder, print_logger


def delete_avail(args):

    args = vars(args)
    species = args.get('species')[0]
    org = args.get('org')[0]
    assembly = args.get('assembly')[0]
    release = args.get('release')[0]

    delete_flag_only = args.get('soft')
    ROOTDIR = args.get('root_dir', '.')

    task = args.get('target', 'all')

    # ['rootdir/species/type/org/assembly/release']
    genome_fa_avail = glob.iglob(jpath(
        ROOTDIR, species,
        'genome',
        org, assembly, 'release_' + release))
    gtf_avail = glob.iglob(jpath(
        ROOTDIR, species,
        'annotation',
        org, assembly, 'release_' + release))
    gff3_avail = glob.iglob(jpath(
        ROOTDIR, species,
        'annotation',
        org, assembly, 'release_' + release))
    bowtie_avail = glob.iglob(jpath(
        ROOTDIR, species,
        'aligner_index', 'bowtie2',
        org, assembly, 'release_' + release))
    star_avail = glob.iglob(jpath(
        ROOTDIR, species,
        'aligner_index', 'star',
        org, assembly, 'release_' + release))

    flag_avail = glob.iglob(jpath(
        ROOTDIR, '_flag', '_{sp}_{org}_{asb}_{rel}_done_*').format(
        sp=species,
        org=org,
        abs=assembly,
        rel=release))

    for flag in flag_avail:
        rmfile(flag)
    if delete_flag_only:
        return

    # TARGETS_SUPPORTED = ['task_genome_fasta',
    #                      'task_annotation',
    #                      'task_annotation_gtf', 'task_annotation_gff3',
    #                      'task_aligner_index_bowtie2', 'task_aligner_index_star',
    #                      'all']
    if task in ['all', 'task_genome_fasta']:
        for d in genome_fa_avail:
            print_logger('Delete {}.'.format(d))
            rmfolder(d)
    if task in ['all', 'task_annotation_gtf']:
        for d in gtf_avail:
            print_logger('Delete {}.'.format(d))
            rmfolder(d)
    if task in ['all', 'task_annotation_gff3']:
        for d in gff3_avail:
            print_logger('Delete {}.'.format(d))
            rmfolder(d)
    if task in ['all', 'task_aligner_index_bowtie2']:
        for d in bowtie_avail:
            print_logger('Delete {}.'.format(d))
            rmfolder(d)
    if task in ['all', 'task_aligner_index_star']:
        for d in star_avail:
            print_logger('Delete {}.'.format(d))
            rmfolder(d)
