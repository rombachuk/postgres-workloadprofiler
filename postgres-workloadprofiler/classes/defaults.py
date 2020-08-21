import os
from helpers.pgwputils import get_installbase

class  CommandDefaults:

    def __init__(self, cfile):
     self.monitorconnection = os.path.join(get_installbase(),u'resources/connections/monitorconnection.info')
     self.dashboardconnection = os.path.join(get_installbase(),u'resources/connections/dashboardconnection.info')
     self.verifycertificates = True
     if cfile and os.path.isfile(cfile):
        cf = open(cfile,'r')
        cflines = cf.readlines()
        for cfline in cflines:
            cflineparts = cfline.split()
            if len(cflineparts) == 2 and cflineparts[0] == u'default_monitorconnection':
                self.monitorconnection = os.path.join(get_installbase(),cflineparts[1])   
            elif len(cflineparts) == 2 and cflineparts[0] == u'default_dashboardconnection':
                 self.dashboardconnection = os.path.join(get_installbase(),cflineparts[1])                             
            else:
                 pass
        cf.close()

    def __str__(self):
        return str(self.__dict__)