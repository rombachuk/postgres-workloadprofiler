import time
import datetime
import string
import logging
import os
import sys
import re
import subprocess 
import requests 


from pgwp_menu import *

from classes.defaults import CommandDefaults
import commands 
   
# Processors - these functions validate and execute the command line request

def process_monitor(connection,args,opts):
    if args[0] == u"monitor" and len(args) == 2:
                commands.monitor(connection,opts,dblist,args[1])
                return True
    return False
   
