import time
import datetime
import string
import logging
import os
import sys
import re
import subprocess 


from pgwp_menu import *

from classes.defaults import CommandDefaults
import commands 
   
# Processors - these functions validate and execute the command line request


def process_dashboardcreateschema(connection,args,opts):
    if (args[0] == u"monitor" and len(args) == 2) or \
    (args[0] == u"dashboard" and args[1] == u"createschema" and len(args) ==2):
                commands.dashboardcreateschema(connection,opts)
                return True
    return False

def process_monitor(monitorconnection,dashboardconnection,args,opts):
    if args[0] == u"monitor" and len(args) == 2:
                commands.monitor(monitorconnection,dashboardconnection,opts,args[1])
                return True
    return False
   
