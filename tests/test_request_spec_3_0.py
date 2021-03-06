"""Test encoding and decoding of request URLs of IIIF Image API v3.0.

This test includes only test cases for the table in section 8,
at <http://iiif.io/api/image/3.0/#uri-encoding-and-decoding>. See
test_request_3_0.py for more examples that test other cases and alter
default forms which should still be decoded correctly.

Simeon Warner - 2015-05...
"""
from iiif.request import IIIFRequest
from .testlib.request import TestRequests

# Data for test. Format is
# name : [ {args}, 'canonical_url', 'alternate_form1', ... ]
#
data = {
    '01_identity': [
        {'identifier': 'id1', 'region': 'full', 'size': 'full',
            'rotation': '0', 'quality': 'default'},
        'id1/full/full/0/default'],
    '02_params': [
        {'identifier': 'id1', 'region': '0,10,100,200', 'size': 'pct:50',
            'rotation': '90', 'quality': 'default', 'format': 'png'},
        'id1/0,10,100,200/pct:50/90/default.png'],
    '03_params': [
        {'identifier': 'id1', 'region': 'pct:10,10,80,80', 'size': '50,',
            'rotation': '22.5', 'quality': 'color', 'format': 'jpg'},
        'id1/pct:10,10,80,80/50,/22.5/color.jpg'],
    '04_params': [
        {'identifier': 'bb157hs6068', 'region': 'full', 'size': 'full',
            'rotation': '270', 'quality': 'gray', 'format': 'jpg'},
        'bb157hs6068/full/full/270/gray.jpg'],
    # ARKs from http://tools.ietf.org/html/draft-kunze-ark-00
    # ark:sneezy.dopey.com/12025/654xz321
    # ark:/12025/654xz321
    '05_ark': [
        {'identifier': 'ark:/12025/654xz321', 'region': 'full',
            'size': 'full', 'rotation': '0', 'quality': 'default'},
        'ark:%2F12025%2F654xz321/full/full/0/default'],
    # URNs from http://tools.ietf.org/html/rfc2141
    # urn:foo:a123,456
    '06_urn': [
        {'identifier': 'urn:foo:a123,456', 'region': 'full',
            'size': 'full', 'rotation': '0', 'quality': 'default'},
        'urn:foo:a123,456/full/full/0/default'],
    # URNs from http://en.wikipedia.org/wiki/Uniform_resource_name
    # urn:sici:1046-8188(199501)13:1%3C69:FTTHBI%3E2.0.TX;2-4
    # ** note will get double encoding **
    '07_urn': [
        {'identifier': 'urn:sici:1046-8188(199501)13:1%3C69:FTTHBI%3E2.0.TX;2-4',
         'region': 'full', 'size': 'full', 'rotation': '0', 'quality': 'default'},

        'urn:sici:1046-8188(199501)13:1%253C69:FTTHBI%253E2.0.TX;2-4/full/full/0/default'],
    # Extreme silliness
    '08_http': [
        {'identifier': 'http://example.com/?54#a', 'region': 'full',
            'size': 'full', 'rotation': '0', 'quality': 'default'},
        'http:%2F%2Fexample.com%2F%3F54%23a/full/full/0/default']
}


class TestAll(TestRequests):
    """Tests for requests from spec."""

    def test01_encode(self):
        """Encoding."""
        self.check_encoding(data, '3.0')

    def test02_decode(self):
        """Decoding."""
        self.check_decoding(data, '3.0')
