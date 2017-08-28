from MrY import get_workflow_fpath
from snakemake import snakemake
import sys

def main(args):
# species=None, assembly=None, release=None, savetodir=None):

    snakefile = get_workflow_fpath(fname='gencode.snakemake')
    success = snakemake(
        snakefile=snakefile,
        targets=args.target,

        configfile=args.config_file,
        config={'output_dir': args.output_dir,
                'experiment_table': args.experiment_table},

        printshellcmds=True,
        printreason=True,
        timestamp=True,
        latency_wait=1800,
        jobname="celseq2_job.{rulename}.{jobid}.sh",

        dryrun=args.dryrun,
        lock=not args.nolock,
        unlock=args.unlock,

        cluster=args.cluster,
        cores=args.cores,
        nodes=args.cores,

        force_incomplete=args.rerun_incomplete,
        ignore_incomplete=args.ignore_incomplete)

    sys.exit(0 if success else 1)

    pass
