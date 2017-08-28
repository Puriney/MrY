from MrY import get_workflow_fpath
from snakemake import snakemake
import sys


def main(args):
    # species=None, assembly=None, release=None, savetodir=None):
    snakefile = get_workflow_fpath(fname='ensembl.snakemake')
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


if __name__ == '__main__':
    main()
