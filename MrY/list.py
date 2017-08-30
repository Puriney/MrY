'''
List available installations at root_dir
'''
import sys

from MrY import join_path as jpath
from MrY import base_name, dir_name
from MrY import print_logger
from MrY import get_species_name_fpath


with open(get_species_name_fpath(fname='species_name.yaml'), 'rt') as fin:
    preset = yaml.load(fin)
    dict_name_common2sci = preset.get('common_scientific_name_pairs',
                                      dict())
    orgs_supported = preset.get('supported_orgs', list())

SPECIES_SUPPORTED = dict_name_common2sci.keys()
ORG_SUPPORTED = ['GENCODE', 'Ensembl']

SPECIES = config.get('species', SPECIES_SUPPORTED)
ORG = config.get('org', ORG_SUPPORTED)
ASSEMBLY = config.get('assembly', [])
RELEASE = config.get('release', [])

ROOTDIR = config.get('root_dir', '.')
