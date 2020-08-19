import pyscopg2
from os import path

from classes.helpers import get_installbase

class Connection:
    
    def __init__(self, infofile):
        if infofile and os.path.isfile(infofile):
            cf = open(infofile,'r')
            cflines = cf.readlines()
            for cfline in cflines:
                cflineparts = cfline.split()
                if len(cflineparts) == 2 and cflineparts[0] == u'dbname':
                    self.dbname = cflineparts[1]
                elif len(cflineparts) == 2 and cflineparts[0] == u'host':
                    self.host = cflineparts[1]
                elif len(cflineparts) == 2 and cflineparts[0] == u'port':
                    self.port = cflineparts[1]
                elif len(cflineparts) == 2 and cflineparts[0] == u'user':
                    self.user = cflineparts[1]
                elif len(cflineparts) == 2 and cflineparts[0] == u'password':
                    self.password = cflineparts[1]
                elif len(cflineparts) == 2 and cflineparts[0] == u'sslmode':
                    self.sslmode = cflineparts[1]
                elif len(cflineparts) == 2 and cflineparts[0] == u'sslrootcertname':
                    self.sslrootcertname = cflineparts[1]
                elif len(cflineparts) == 2 and cflineparts[0] == u'sslrootcertpath':
                    if cflineparts[1].startswith(u'/'):
                        self.sslrootcertpath = cflineparts[1]
                    else:
                        self.sslrootcertpath = os.path.join(get_installbase(),cflineparts[1])
                else:
                    pass
            cf.close()
            
            if self.dbname is not None  and self.host is not None \
            and self.port is not None  and self.user is not None \
            and self.user is not None  and self.password is not None and self.sslmode is not None:
                if self.sslmode == u'verify-full' or self.sslmode == u'verify-ca':
                    if self.sslrootcertpath is not None and self.sslrootcertname is not None:
                        if os.path.isfile(os.path.join(self.sslrootcertpath+self.sslrootcertname)):
                            self.valid = True 
                        else:
                            self.failurereason = u'Missing certificate file {}'.format(self.sslrootcertpath+self.sslrootcertname)
                    else:
                        self.valid = False
                        self.failurereason = u'Missing certificate file parameters in connection file'
                else:
                    self.valid = True
            else:
                self.valid = False
                self.failurereason = u'Missing connection parameters in connection file'
        else:
            self.valid = False
            self.failurereason = u'Missing connection file {}'.format(infofile)
            
        if self.valid :
            try:
                if self.sslmode == u'verify-full' or self.sslmode == u'verify-ca':
                    self.connection = psycopg2.connect(
                                    dbname = self.dbname,
                                    user = self.user,
                                    password = self.password,
                                    host = self.host,
                                    port = self.port,
                                    sslmode = self.sslmode
                                    )
                else:
                     self.connection = psycopg2.connect(
                                    dbname = self.dbname,
                                    user = self.user,
                                    password = self.password,
                                    host = self.host,
                                    port = self.port,
                                    sslmode = self.sslmode,
                                    sslrootcert = os.path.join(self.sslrootcertpath,self.sslrootcertname)
                                    )  

            except (Exception, pyscopg2.Error) as error:                
                self.valid = False
                self.failurereason = u'Connect test error [{}]'.format(str(error))


    def testQuery(self,query,limit=1):
        if len(query) > 0 and self.valid:
            try:
                cursor = self.connection.cursor()
                if u'LIMIT' not in query.upper():
                    cursor.execute(query+u' LIMIT {}'.format(str(limit)))
                else:
                    cursor.execute(query)
                rows = cursor.fetchall()
                cursor.close()
                return True
            except (Exception, pyscopg2.Error) as error: 
                return False  
        
    def __str__(self):
        return str(self.__dict__)
 
# Special Helpers
 

