import json
import logging

from classes.loghandler import LogHandler
 
def dashboardcreateschema(dconnection,opts):
 try:
  dconnection.connection.rollback()
  dconnection.connection.autocommit = True
  cursor = dconnection.connection.cursor() 
  statements = [
    u"DROP SCHEMA pgwp CASCADE",
    u"CREATE SCHEMA pgwp AUTHORIZATION {}".format(dconnection.user),
    u"GRANT ALL ON SCHEMA pgwp to {}".format(dconnection.user),
    u"CREATE TABLE pgwp.statements as SELECT * FROM pg_stat_statements;",
    u"ALTER TABLE pgwp.statements ADD COLUMN host TEXT",
    u"ALTER TABLE pgwp.statements ADD COLUMN dbname TEXT",
    u"ALTER TABLE pgwp.statements ADD COLUMN mtime TIMESTAMPTZ",
    u"ALTER TABLE pgwp.statements ADD COLUMN mtime_epoch BIGINT",
    u"ALTER TABLE pgwp.statements ADD COLUMN inc_total_time DOUBLE PRECISION",
    u"ALTER TABLE pgwp.statements ADD COLUMN inc_calls BIGINT",
    u"ALTER TABLE pgwp.statements ADD COLUMN inc_rows BIGINT",
    u"UPDATE pgwp.statements SET host = '{}'".format(dconnection.host),
    u"UPDATE pgwp.statements s SET dbname = (SELECT datname FROM pg_database d WHERE s.dbid = d.oid)",
    u"UPDATE pgwp.statements SET mtime_epoch = (SELECT extract(epoch from date_trunc('minute',now())))",
    u"UPDATE pgwp.statements SET mtime =  date_trunc('minute',now())",
    u"SELECT * FROM pgwp.statements LIMIT 1;"]
  for s in statements:
      dconnection.logger.log(u" statement [{}]".format(s))
      cursor.execute(s)
  cursor.close()
  dconnection.connection.autocommit = False
 except Exception as e:
    exceptionlogger = LogHandler(u'/var/log/pgwp/pgwp.log',u'[dashboard create schema] ')
    exceptionlogger.logprint(u'Unexpected error during dashboard schema creation : {}'.format(str(e)))
    return False
