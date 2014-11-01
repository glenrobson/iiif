#!/usr/bin/env python
"""
Run validator code from command line

Wrapper around validator.py for use in local manual and continuous 
integration tests of IIIF servers. Command line options specify
parameters of the server, the API version to be tested and the 
expected compliance level. Exit code is zero for success, non-zero 
otherwise (number of failed tests).

TO-DO:

  * Need change in validator.py so it doesn't run "application = apache()"
  * Want nice way to turn off print of URLs

"""
from validator import ValidationInfo,TestSuite,ImageAPI
import logging
import optparse
import sys

# Options and arguments
p = optparse.OptionParser(description='IIIF Command Line Validator')
p.add_option('--identifier','-i', action='store',
             help="Identifier to run tests for")
p.add_option('--server','-s', action='store', default='localhost',
             help="Server name of IIIF service")
p.add_option('--prefix','-p', action='store', default='',
             help="Prefix of IIIF service on server")
p.add_option('--scheme', action='store', default='http',
             help="Scheme (http or https)")
p.add_option('--auth','-a', action='store', default='',
             help="Auth info for service")
p.add_option('--version', action='store', default='2.0',
             help="IIIF API version")
p.add_option('--level', action='store', type='int', default=1,
             help="Compliance level to test (default 1)")
p.add_option('--verbose', '-v', action='store_true',
             help="Be verbose")
p.add_option('--quiet','-q', action='store_true',
             help="Minimal output only")
(opt, args) = p.parse_args()

# Logging/output
level = (logging.INFO if opt.verbose else (logging.ERROR if opt.quiet else logging.WARNING))
logging.basicConfig(level=level,format='%(message)s')

# Sanity checks
if (not opt.identifier):
    logging.error("No identifier specified, aborting (-h for help)") 
    exit(99)

# Run as one shot set of tests with output to stdout
info2 = ValidationInfo()
tests = TestSuite(info2).list_tests(opt.version)
n = 0
bad = 0
for testname in tests:
    if (tests[testname]['level']>opt.level):
        continue
    n += 1
    test_str = ("[%d] test %s" % (n,testname))
    try:
        info = ValidationInfo()
        testSuite = TestSuite(info) 
        result = ImageAPI(opt.identifier, opt.server, opt.prefix, opt.scheme, opt.auth, opt.version)
        testSuite.run_test(testname, result)
        if result.exception:
            e = result.exception
            bad += 1
            logging.error("%s FAIL"%test_str)
            logging.error("  url: %s\n  got: %s\n  expected: %s\n  type: %s"%(result.urls,e.got,e.expected,e.type))
        else:
            logging.warning("%s PASS"%test_str)
            logging.info("  url: %s\n  tests: %s\n"%(result.urls,result.tests))
    except Exception as e:
        #raise
        #info = {'test' : testname, 'status': 'internal-error', 'url':e.url, 'msg':str(e)}
        bad += 1
        logging.error("%s FAIL"%test_str)
        logging.error("  exception: %s\n"%(str(e)))
logging.warning("Done (%d tests, %d failures)" % (n,bad))
exit(bad)