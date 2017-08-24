from pkg_resources import resource_string, resource_filename


def get_workflow_fpath(fname, pkgname='MrY'):
    fpath = resource_filename(pkgname, 'workflow/{}'.format(fname))
    return(fpath)
