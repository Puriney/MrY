from pkg_resources import resource_filename


def get_species_name_fpath(fname='species_name.yaml', pkgname='MrY'):
    fpath = resource_filename(pkgname, 'template/{}'.format(fname))
    return(fpath)
