# MrY -- :books: Management of references at Yanai lab

## Why this mini-manager?

When human, mouse, zebrafish, roundworm (*C. elegans*), yeast (*S. cerevisiae*),
and bacteria (salmonella and *M. tuberculosis*) show up together in one zoo,
a manager is suggested.


## What does it do for you?

- Download genome sequence (.fasta). It downloads the `primary_assembly`
version, if not available, `toplevel` version is downloaded.
- Download annotation (both .gff3 and .gtf).
- Build aligner index.
- Maintain references in a folder structure which is making sense.


## How to install `MrY`?

```bash
git clone git@github.com:Puriney/MrY.git
cd MrY
pip install ./
```

## How to use `MrY`?

### Install references

``` bash
yun install  --root-dir /path/to/your/zoo \
--species zebrafish \
--assembly GRCz10 \
--org Ensembl \
--release 90 \
--target all
```

`MrY` will generate a folder named <kbd>zebrafish</kbd> under <kbd>/path/to/your/zoo</kbd>
to create references for zebrafish of which the assembly name is GRCz10 in
release 90 of Ensembl.

```
zebrafish/
├── aligner_index
│   ├── bowtie2
│   │   └── Ensembl
│   │       └── GRCz10
│   │           └── release_90
│   │               ├── GRCz10.dna.1.bt2
│   │               ├── GRCz10.dna.2.bt2
│   │               ├── GRCz10.dna.3.bt2
│   │               ├── GRCz10.dna.4.bt2
│   │               ├── GRCz10.dna.rev.1.bt2
│   │               └── GRCz10.dna.rev.2.bt2
│   └── star
│       └── Ensembl
│           └── GRCz10
│               └── release_90
│                   ├── chrLength.txt
│                   ├── chrNameLength.txt
│                   ├── chrName.txt
│                   ├── chrStart.txt
│                   ├── exonGeTrInfo.tab
│                   ├── exonInfo.tab
│                   ├── geneInfo.tab
│                   ├── Genome
│                   ├── genomeParameters.txt
│                   ├── Log.out
│                   ├── SA
│                   ├── SAindex
│                   ├── sjdbInfo.txt
│                   ├── sjdbList.fromGTF.out.tab
│                   ├── sjdbList.out.tab
│                   └── transcriptInfo.tab
├── annotation
│   └── Ensembl
│       └── GRCz10
│           └── release_90
│               ├── ensembl.GRCz10.90.gff3
│               ├── ensembl.GRCz10.90.gff3.gz
│               ├── ensembl.GRCz10.90.gtf
│               └── ensembl.GRCz10.90.gtf.gz
└── genome
    └── Ensembl
        └── GRCz10
            └── release_90
                ├── Danio_rerio.GRCz10.dna.toplevel.fa.gz
                ├── GRCz10.dna.fa
                └── GRCz10.dna.fa.gz -> /path/to/your/zoo/zebrafish/genome/Ensembl/GRCz10/release_90/Danio_rerio.GRCz10.dna.toplevel.fa.gz
```

Alternatively, more than one species can be installed in the same time:

```
yun install --root-dir /ifs/data/yanailab/ref \
--species zebrafish roundworm brewer_yeast \
--assembly GRCz10 WBcel235 R64-1-1 \
--release  90 90 90 \
--org Ensembl \
--target all
```

### List available references

List available references for specific zibrafish:
```
yun list  --root-dir /path/to/your/zoo \
--species zebrafish \
--assembly GRCz10 \
--org Ensembl \
--release 90
```

```
==========
zebrafish-GRCz10-Ensembl-90 was queried:
            Genome (.fa): Installed
       Annotation (.gtf): Installed
      Annotation (.gff3): Installed
                 Bowtie2: Installed
                    STAR: Installed
```

Alternatively, list all available references and a markdown table will be generated.

```
yun list  --root-dir /path/to/your/zoo
```

| Species      | Assembly   | Org     | Release   | Genome (.fa)   | Annotation (.gtf)   | Annotation (.gff3)   | Bowtie2   | STAR   |
|:-------------|:-----------|:--------|:----------|:---------------|:--------------------|:---------------------|:----------|:-------|
| zebrafish    | GRCz10     | Ensembl | 90        | True           | True                | True                 | True      | True   |
| roundworm    | WBcel235   | Ensembl | 90        | True           | True                | True                 | False     | False  |
| mouse        | GRCm38     | GENCODE | M15       | True           | True                | True                 | True      | True   |
| mouse        | GRCm38     | Ensembl | 90        | True           | True                | True                 | True      | True   |
| human        | GRCh38     | GENCODE | 27        | True           | True                | True                 | True      | True   |
| human        | GRCh38     | GENCODE | 23        | False          | True                | True                 | False     | False  |
| human        | GRCh38     | Ensembl | 90        | True           | True                | True                 | True      | True   |
| brewer_yeast | R64-1-1    | Ensembl | 90        | True           | True                | True                 | True      | True   |


### Delete references

Check which GTF and GFF3 files are to be deleted before actually removing them.
```
yun delete  --root-dir /path/to/your/zoo \
--species zebrafish \
--assembly GRCz10 \
--org Ensembl \
--release 90 \
--target task_annotation \
-n
```
Run above command without `-n` and actually remove them. Change
*task_annotation* to *all* to delete all references of specific zebrafish.

