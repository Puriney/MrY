import sys
import argparse
import yaml
from snakemake import snakemake
from .helper import base_name, dir_name, join_path
from .helper import is_nonempty_file, print_logger, ymd
from .helper import rmfile, rmfolder
from .version import __version__
from .locate_workflow import get_workflow_fpath
from .locate_preset import get_species_name_fpath

from .install_receipt import new_installation_receipt
from .install_refs import main as do_install_refs

from .list_avail import list_avail
from .delete_avail import delete_avail


MY_PKG_NAME = 'MrY'

with open(get_species_name_fpath(fname='species_name.yaml'), 'rt') as fin:
    preset = yaml.load(fin)
    SPECIES_SUPPORTED = preset.get('common_scientific_name_pairs',
                                   dict()).keys()
    ORG_SUPPORTED = preset.get('supported_orgs', list())

TARGETS_SUPPORTED = ['task_genome_fasta',
                     'task_annotation',
                     'task_annotation_gtf', 'task_annotation_gff3',
                     'task_aligner_index_bowtie2', 'task_aligner_index_star',
                     'all']

'''
- subcommands: https://docs.python.org/3/library/argparse.html#sub-commands
- Group input/output: https://docs.python.org/3/library/argparse.html#argument-groups
'''


def do_install(args):
    if (not args.root_dir) or \
        (not args.species) or \
        (not args.assembly) or \
        (not args.org) or \
            (not args.release):
        print('Specify species + assembly + org + release to install. ')
        return
    do_install_refs(args)


def do_list(args):
    avail_installations = list_avail(args)
    print('=' * 10)
    print('All Available Installed Refs: ')
    print(avail_installations)


def do_delete(args):
    if (not args.root_dir) or \
        (not args.species) or \
        (not args.assembly) or \
        (not args.org) or \
            (not args.release):
        print('Specify species + assembly + org + release to delete. ')
        return

    delete_avail(args)


def get_argument_parser():
    desc = ('Mr.Y -- Management of references at Yanai Lab')
    parser = argparse.ArgumentParser(
        description=desc,
        add_help=False,
        usage='yun [Subcommands] [Input] [Ref_Dir] [Run-time] [Server]')

    g_input = parser.add_argument_group('Input')
    g_input.add_argument(
        "--species",
        default=[], nargs='*', choices=SPECIES_SUPPORTED,
        help=('Common name of supported genome (e.g. Human). '))
    g_input.add_argument(
        "--org",
        default=[], nargs='*', choices=ORG_SUPPORTED,
        help=('Download references from speficied orgnization '
              '(e.g. Gencode). '))
    g_input.add_argument(
        "--assembly",
        default=[], nargs='*',
        help=('Genome assembly version (e.g. GRCh38). '))
    g_input.add_argument(
        "--release",
        default=[], nargs='*',
        help=('Release name/number of genome assembly '
              '(e.g. 27). '))
    g_output = parser.add_argument_group('Reference Dir')
    g_output.add_argument(
        "--root-dir", "--ref-dir",
        default='.', type=str,
        help='Root directory to save all references.')

    g_runtime = parser.add_argument_group('Run-time')
    g_runtime.add_argument("--dryrun", "-n",
                           action="store_true",
                           help="Do not execute anything.")
    g_runtime.add_argument("--nolock",
                           action="store_true", default=True,
                           help="Do not lock the working directory")
    g_runtime.add_argument("--unlock",
                           action="store_true",
                           help="Remove a lock on the working directory.")
    g_runtime.add_argument(
        "--cores", "--jobs", "-j",
        action="store",
        nargs="?",
        metavar="N",
        type=int,
        default=1,
        help=("Use at most N cores in parallel (default: 1). "))
    g_runtime.add_argument(
        "--rerun-incomplete", "--ri",
        action="store_true",
        help=("Re-run all "
              "jobs the output of which is recognized as incomplete."))
    g_runtime.add_argument(
        "--ignore-incomplete", "--ii",
        action="store_true",
        help="Do not check for incomplete output files.")

    g_cluster = parser.add_mutually_exclusive_group()
    g_cluster.add_argument(
        "--cluster", "-c",
        metavar="CMD",
        help=("Execute pipeline by taking tasks as jobs running in cluster, "
              "e.g. --cluster 'qsub -cwd -j y'"))

    parser.add_argument(
        "--version",
        action="version",
        version=__version__)
    parser.add_argument(
        "--verbose", "-v",
        action="count",
        default=0)

    subparsers = parser.add_subparsers(title='Subcommands')
    # Install Receipt
    parser_receipt = subparsers.add_parser(
        'new-receipt',
        parent=[parser],
        usage='yun new-receipt -o FILE',
        help='New receipt for installation of references')
    parser_receipt.add_argument(
        '-o', '--saveto',
        default='install_receipt_ncbi.yaml', type=str, metavar='FILENAME',
        help='Save receipt of installation to file.' )
    # Install
    parser_install = subparsers.add_parser(
        'install',
        parents=[parser],
        usage='yun install target [Input] [Ref_Dir] [Run-time] [Server]',
        help=('Perform installation.'))
    parser_install.add_argument(
        "--target",
        default='all', choices=TARGETS_SUPPORTED, nargs=1,
        help=('Target to install. '))
    parser_install.set_defaults(func=do_install)
    # List
    parser_list = subparsers.add_parser(
        'list',
        parents=[parser],
        help=('List installed references.'))
    parser_list.add_argument(
        "--soft",
        action='store_true',
        help=(('List available installations by tracking flags only, '
               'instead of searching actual files.')))
    parser_list.add_argument(
        "--snapshot",
        type=str,
        metavar='FILENAME', default='refs_all_available_' + ymd() + '.txt',
        help=(('Save items list to file.')))
    parser_list.set_defaults(func=do_list)
    # Delete
    parser_delete = subparsers.add_parser(
        'delete',
        parents=[parser],
        help=('Delete references, if installed.'))
    parser_delete.add_argument(
        "--soft",
        action='store_true',
        help=(('Delete flags for installed references, '
               'instead of the actual files.')))
    parser_delete.add_argument(
        "--target",
        default='all', choices=TARGETS_SUPPORTED, nargs=1,
        help=('Target to delete. '))
    parser_delete.set_defaults(func=do_delete)

    return(parser)


def main():
    p = get_argument_parser()
    args = p.parse_args()

    if args.verbose >= 4:
        print(args)

    if 'func' not in args:
        p.print_help()
        sys.exit(1)

    if args.root_dir:
        args.func(args)
    else:
        p.print_help()
        print()
        print_logger(('Specify directory to '
                      'install or list references.'))


if __name__ == '__main__':
    main()
