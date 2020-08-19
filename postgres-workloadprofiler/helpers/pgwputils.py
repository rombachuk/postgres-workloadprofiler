import os


# general purpose convenience functions
def process_boolean(opt,default):    
    if not opt:
        if default == u'True' or default == u'true':
           return True
        else:
           return False
    else:
        return opt

# special cases

       
       
# environmental and naming-convention functions


    
def get_installbase():
    if u'PGWP_INSTALL_BASE' in os.environ:
        install_base = os.environ[u'PGWP_INSTALL_BASE']
    else:
        install_base = os.getcwd()
    return install_base

