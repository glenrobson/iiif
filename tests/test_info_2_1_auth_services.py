"""Test code for iiif/info.py for Image API v2.1 auth service descriptions

See: https://github.com/IIIF/iiif.io/blob/image-auth/source/api/image/2.1/authentication.md
"""
import unittest
import re #needed because no assertRegexpMatches in 2.6
import json
from iiif.info import IIIFInfo
from iiif.auth import IIIFAuth

class TestAll(unittest.TestCase):

    def assertJSONEqual(self, stra, strb):
        """Check JSON strings for equality.
        
        In python2.x the as_json method includes spaces after commas
        but before \n, this is not included in python3.x. Strip such
        spaces before doing the comparison.
        """
        a = re.sub(r',\s+',',',stra)
        b = re.sub(r',\s+',',',strb)
        self.assertEqual( a, b )

    def test01_empty_auth_defined(self):
        info = IIIFInfo(identifier="http://example.com/i1", api_version='2.1')
        auth = IIIFAuth()
        auth.add_services(info)
        self.assertJSONEqual( info.as_json(validate=False), '{\n  "@context": "http://iiif.io/api/image/2/context.json", \n  "@id": "http://example.com/i1", \n  "profile": [\n    "http://iiif.io/api/image/2/level1.json"\n  ], \n  "protocol": "http://iiif.io/api/image"\n}' )
        self.assertEqual( info.service, None )

    def test02_just_login(self):
        info = IIIFInfo(identifier="http://example.com/i1", api_version='2.1')
        auth = IIIFAuth()
        auth.login_uri = 'http://example.com/login'
        auth.add_services(info) 
        self.assertEqual( info.service['@id'], "http://example.com/login" )
        self.assertEqual( info.service['label'], "Login to image server" )
        self.assertEqual( info.service['profile'], "http://iiif.io/api/auth/0/login" )

    def test03_login_and_logout(self):
        info = IIIFInfo(identifier="http://example.com/i1", api_version='2.1')
        auth = IIIFAuth()
        auth.login_uri = 'http://example.com/login'
        auth.logout_uri = 'http://example.com/logout'
        auth.add_services(info) 
        self.assertEqual( info.service['@id'], "http://example.com/login" )
        self.assertEqual( info.service['label'], "Login to image server" )
        self.assertEqual( info.service['profile'], "http://iiif.io/api/auth/0/login" )
        svcs = info.service['service']
        self.assertEqual( svcs['@id'], "http://example.com/logout" )
        self.assertEqual( svcs['label'], "Logout from image server" )
        self.assertEqual( svcs['profile'], "http://iiif.io/api/auth/0/logout" )

    def test04_login_and_client_id(self):
        info = IIIFInfo(identifier="http://example.com/i1", api_version='2.1')
        auth = IIIFAuth()
        auth.login_uri = 'http://example.com/login'
        auth.client_id_uri = 'http://example.com/client_id'
        auth.add_services(info) 
        self.assertEqual( info.service['@id'], "http://example.com/login" )
        self.assertEqual( info.service['label'], "Login to image server" )
        self.assertEqual( info.service['profile'], "http://iiif.io/api/auth/0/login" )
        svcs = info.service['service']
        self.assertEqual( svcs['@id'], "http://example.com/client_id" )
        self.assertEqual( svcs['profile'], "http://iiif.io/api/auth/0/clientId" )

    def test05_login_and_access_token(self):
        info = IIIFInfo(identifier="http://example.com/i1", api_version='2.1')
        auth = IIIFAuth()
        auth.login_uri = 'http://example.com/login'
        auth.access_token_uri = 'http://example.com/token'
        auth.add_services(info) 
        self.assertEqual( info.service['@id'], "http://example.com/login" )
        self.assertEqual( info.service['label'], "Login to image server" )
        self.assertEqual( info.service['profile'], "http://iiif.io/api/auth/0/login" )
        svcs = info.service['service']
        self.assertEqual( svcs['@id'], "http://example.com/token" )
        self.assertEqual( svcs['profile'], "http://iiif.io/api/auth/0/token" )

    def test06_full_set(self):
        info = IIIFInfo(identifier="http://example.com/i1", api_version='2.1')
        auth = IIIFAuth()
        auth.name = "Whizzo!"
        auth.logout_uri = 'http://example.com/logout'
        auth.access_token_uri = 'http://example.com/token'
        auth.client_id_uri = 'http://example.com/clientId'
        auth.login_uri = 'http://example.com/login'
        auth.add_services(info) 
        self.assertEqual( info.service['@id'], "http://example.com/login" )
        self.assertEqual( info.service['label'], "Login to Whizzo!" )
        svcs = info.service['service']
        self.assertEqual( svcs[0]['@id'], "http://example.com/logout" )
        self.assertEqual( svcs[1]['@id'], "http://example.com/clientId" )
        self.assertEqual( svcs[2]['@id'], "http://example.com/token" )


