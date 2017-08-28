import sys
import argparse
from snakemake import snakemake
from .helper import base_name, dir_name, join_path
from .helper import is_nonempty_file, print_logger
from .version import __version__
from .locate_workflow import get_workflow_fpath

from .install_gencode import main as do_install_gencode
MY_PKG_NAME = 'MrY'


SPECIES_SUPPORTED = ['Human', 'Mouse', 'Zebrafish']
ORG_SUPPORTED = ['GENCODE', 'Ensemble']
INSTALL_TARGETS = ['fasta', 'gtf', 'gff',
                   'aligner_bowtie', 'aligner_star',
                   'all']

'''
- subcommands: https://docs.python.org/3/library/argparse.html#sub-commands
- Group input/output: https://docs.python.org/3/library/argparse.html#argument-groups
'''


def do_install(args):
    if args.org == 'GENCODE':
        do_install_gencode(args)


def do_list(args):
    print(args.root_dir + '<<<')
    pass


def get_argument_parser():
    desc = ('Mr.Y -- Management of references at Yanai Lab')
    parser = argparse.ArgumentParser(
        description=desc,
        add_help=False,
        usage='yun [Subcommands] [Input] [Output] [Run-time]')

    g_input = parser.add_argument_group('Input')
    g_input.add_argument(
        "--species",
        default=None, nargs='*', choices=SPECIES_SUPPORTED,
        help=('Common name of supported genome (e.g. Human). '))
    g_input.add_argument(
        "--org",
        default=None, nargs='*', choices=ORG_SUPPORTED,
        help=('Download references from speficied orgnization '
              '(e.g. Gencode). '))
    g_input.add_argument(
        "--assembly",
        default=None, nargs='*',
        help=('Genome assembly version (e.g. GRCh38). '))
    g_input.add_argument(
        "--release",
        default=None, nargs='*',
        help=('Release name/number of genome assembly '
              '(e.g. 27). '))
    g_output = parser.add_argument_group('Output')
    g_output.add_argument(
        "--root-dir",
        required=True,
        default=None,
        help='Root directory to save all references.')

    g_runtime = parser.add_argument_group('Run-time')
    g_runtime.add_argument("--dryrun", "-n",
                           action="store_true",
                           help="Do not execute anything.")
    g_runtime.add_argument("--nolock",
                           action="store_true",
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

    parser.add_argument(
        "--version",
        action="version",
        version=__version__)
    parser.add_argument(
        "--verbose", "-v",
        action="count",
        default=0)

    subparsers = parser.add_subparsers(title='Subcommands')
    # Install
    parser_install = subparsers.add_parser(
        'install',
        parents=[parser],
        usage='yun install target [Input] [Output] [Run-time]',
        help=('Perform installation.'))
    parser_install.add_argument(
        "--target",
        default='all', nargs=1, choices=INSTALL_TARGETS,
        required=True,
        help=('Target to install. '))
    parser_install.set_defaults(func=do_install)
    # List
    parser_list = subparsers.add_parser(
        'list',
        parents=[parser],
        help=('List installed references.'))
    parser_list.set_defaults(func=do_list)

    return(parser)


def main():
    p = get_argument_parser()
    args = p.parse_args()

    if args.verbose >= 3:
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
