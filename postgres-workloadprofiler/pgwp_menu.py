import datetime
import sys
import base64
import os
from optparse import OptionParser

from classes.defaults import CommandDefaults
from helpers.cbutils import process_boolean
    
           
def process_defaults(opts,defaults):

    if not opts.monitorconnection:
       opts.connectioninfo =  defaults.monitorconnection
       
    if not opts.dashboardconnection:
       opts.connectioninfo =  defaults.dashboardconnection      

    return opts

def options(defaults):
    parser = OptionParser()


    parser.add_option(u"-x",u"--monitorconnection",                
                      help=u"file containing postgres db to be monitored info [default none]")
    parser.add_option(u"--dashboardconnection",                
                      help=u"file containing postgres db to store results for grafana[default none]")
    opts, args = parser.parse_args()
    opts = process_defaults(opts,defaults)
    return opts, args


