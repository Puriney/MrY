import sys
from MrY import get_workflow_fpath, print_logger
from MrY import load_installation_receipt
from snakemake import snakemake


def main(args):
    if 'GENCODE' in args.org:
        print_logger('yun install GENCODE...')
        snakefile = get_workflow_fpath(fname='gencode.snakemake')
    elif 'Ensembl' in args.org:
        print_logger('yun install Ensembl...')
        snakefile = get_workflow_fpath(fname='ensembl.snakemake')
    elif 'NCBI' in args.org:
        print_logger('yun install NCBI... ')
        receipt = load_installation_receipt(fpath=args.receipt)
        args.species = [receipt.get('species', None)]
        args.assembly = [receipt.get('assembly', None)]
        args.org = [receipt.get('org', None)]
        args.release = [receipt.get('release', None)]
        snakefile = get_workflow_fpath(fname='ncbi.snakemake')
    else:
        pass

    if args.verbose >= 5:
        print(args)

    success = snakemake(
        snakefile=snakefile,
        targets=args.target,

        # configfile=args.config_file,
        config={'root_dir': args.root_dir,
                'species': args.species,
                'assembly': args.assembly,
                'org': args.org,
                'release': args.release},

        printshellcmds=True,
        printreason=True,
        timestamp=True,
        latency_wait=1800,
        jobname="MrY.{rulename}.{jobid}.sh",

        dryrun=args.dryrun,
        lock=not args.nolock,
        unlock=args.unlock,

        cluster=args.cluster,
        cores=args.cores,
        nodes=args.cores,

        force_incomplete=args.rerun_incomplete,
        ignore_incomplete=args.ignore_incomplete)

    sys.exit(0 if success else 1)

    '''
    to-do
    If requested installation is not possible, for example, release version
    is not available in org, the setup-dir task still runs.

    To delete these dir, `snakemake --summary` can list files/dirs created,
    so that I can delete them if snakemake did not run successfully.

    Wait for new official release of snakemake because there is a bug when
    running `snakemake --summary`. See reported issue Aug-1-2017 here:
    https://bitbucket.org/snakemake/snakemake/issues/597/persistence-object-has-no-attribute-code

    '''


if __name__ == '__main__':
    main()