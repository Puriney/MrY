from snakemake import snakemake
import sys
import argparse
from .helper import base_name, dir_name, join_path
from .helper import is_nonempty_file, print_logger
from .version import __version__
from .locate_workflow import get_workflow_fpath

MY_PKG_NAME = 'MrY'


SPECIES_SUPPORTED = ['Human', 'Mouse', 'Zebrafish']
ORG_SUPPORTED = ['Gencode', 'Ensemble']

'''
- subcommands: https://docs.python.org/3/library/argparse.html#sub-commands
- Group input/output: https://docs.python.org/3/library/argparse.html#argument-groups
'''


def do_install(args):
    print(args.root_dir)
    print(args.specie)
    pass


def do_list(args):
    print(args.root_dir + '<<<')
    pass


def get_argument_parser():
    desc = ('Mr.Y -- Management of references at Yanai Lab')
    parser = argparse.ArgumentParser(
        description=desc,
        add_help=False,
        usage='yan [Subcommands] [Input] [Output] [Run-time]')

    g_input = parser.add_argument_group('Input')
    g_input.add_argument(
        "--specie",
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
        "--root-dir", "--od",
        # required=True,
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
        help=('Perform installation.'))
    parser_install.set_defaults(func=do_install)
    # List
    parser_list = subparsers.add_parser(
        'list',
        parents=[parser],
        help=('List installed references.'))
    # parser_list.add_argument(
    #     "root_dir",
    #     # required=True,
    #     help=('Root directory where references '
    #           'to be listed.'))
    parser_list.set_defaults(func=do_list)

    return(parser)


def main():
    p = get_argument_parser()
    args = p.parse_args()

    if args.verbose >= 3:
        print(args)

    if args.func and args.root_dir:
        args.func(args)
    else:
        # print_logger('Specify directory to install or list references.')
        p.print_help()


if __name__ == '__main__':
    main()
