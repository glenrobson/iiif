"""Test code for iiif/info.py for Image API version 1.1."""
import unittest
from .testlib.assert_json_equal_mixin import AssertJSONEqual
from iiif.info import IIIFInfo, IIIFInfoError


class TestAll(unittest.TestCase, AssertJSONEqual):
    """Tests."""

    def test01_minmal(self):
        """Trivial JSON test."""
        ir = IIIFInfo(server_and_prefix="http://example.com",
                      identifier="i1", api_version='1.1')
        self.assertJSONEqual(ir.as_json(validate=False),
                             '{\n  "@context": "http://library.stanford.edu/iiif/image-api/1.1/context.json", \n  "@id": "http://example.com/i1", \n  "profile": "http://library.stanford.edu/iiif/image-api/1.1/compliance.html#level1"\n}')
        ir.width = 100
        ir.height = 200
        self.assertJSONEqual(ir.as_json(),
                             '{\n  "@context": "http://library.stanford.edu/iiif/image-api/1.1/context.json", \n  "@id": "http://example.com/i1", \n  "height": 200, \n  "profile": "http://library.stanford.edu/iiif/image-api/1.1/compliance.html#level1", \n  "width": 100\n}')

    def test02_scale_factor(self):
        """Test scale factor."""
        ir = IIIFInfo(width=1, height=2, scale_factors=[1, 2], api_version='1.1')
        json = ir.as_json(validate=False)
        self.assertRegexpMatches(json, r'"scale_factors": \[\s*1')

    def test03_array_vals(self):
        """Test array values."""
        i = IIIFInfo(api_version='1.1')
        i.scale_factors = [1, 2, 3]
        self.assertEqual(i.scale_factors, [1, 2, 3])
        i._setattr('scale_factors', [4, 5, 6])
        self.assertEqual(i.scale_factors, [4, 5, 6])

    def test04_conf(self):
        """Test configuration via conf parameter."""
        conf = {'tile_width': 999, 'scale_factors': [9, 8, 7]}
        i = IIIFInfo(api_version='1.1', conf=conf)
        self.assertEqual(i.tile_width, 999)
        self.assertEqual(i.scale_factors, [9, 8, 7])

    def test05_level_and_profile(self):
        """Test level and profile."""
        i = IIIFInfo(api_version='1.1')
        i.level = 0
        self.assertEqual(i.level, 0)
        self.assertEqual(i.profile,
                         "http://library.stanford.edu/iiif/image-api/1.1/compliance.html#level0")
        i.level = 2
        self.assertEqual(i.level, 2)
        self.assertEqual(i.profile,
                         "http://library.stanford.edu/iiif/image-api/1.1/compliance.html#level2")
        i.profile = "http://library.stanford.edu/iiif/image-api/1.1/compliance.html#level1"
        self.assertEqual(i.level, 1)

    def test06_validate(self):
        """Test validate()."""
        i = IIIFInfo(api_version='1.1')
        self.assertRaises(IIIFInfoError, i.validate)
        i = IIIFInfo(identifier='a')
        self.assertRaises(IIIFInfoError, i.validate)
        i = IIIFInfo(identifier='a', width=1, height=2)
        self.assertTrue(i.validate())

    def test10_read_example_from_spec(self):
        """Test read of example from spec."""
        i = IIIFInfo(api_version='1.1')
        fh = open('tests/testdata/info_json_1_1/info_from_spec.json')
        i.read(fh)
        self.assertEqual(i.context,
                         "http://library.stanford.edu/iiif/image-api/1.1/context.json")
        self.assertEqual(i.id,
                         "http://iiif.example.com/prefix/1E34750D-38DB-4825-A38A-B60A345E591C")
        self.assertEqual(i.profile,
                         "http://library.stanford.edu/iiif/image-api/1.1/compliance.html#level0")
        self.assertEqual(i.width, 6000)
        self.assertEqual(i.height, 4000)
        self.assertEqual(i.scale_factors, [1, 2, 4])
        self.assertEqual(i.tile_width, 1024)
        self.assertEqual(i.tile_height, 1024)
        self.assertEqual(i.formats, ['jpg', 'png'])
        self.assertEqual(i.qualities, ['native', 'grey'])

    def test11_read_example_with_explicit_version(self):
        """Test reading without explicit version."""
        i = IIIFInfo()  # default not 1.1
        fh = open('tests/testdata/info_json_1_1/info_from_spec.json')
        i.read(fh)  # will get 1.1 from @context
        self.assertEqual(i.api_version, '1.1')
        fh = open('tests/testdata/info_json_1_1/info_from_spec.json')
        self.assertRaises(IIIFInfoError, i.read, fh, '0.1')  # 0.1 bad
        fh = open('tests/testdata/info_json_1_1/info_from_spec.json')
        i.read(fh, '1.1')
        self.assertEqual(i.api_version, '1.1')

    def test12_read_example_with_unknown_context(self):
        """Test read with unknown/bad context."""
        i = IIIFInfo()
        fh = open('tests/testdata/info_json_1_1/info_bad_context.json')
        self.assertRaises(IIIFInfoError, i.read, fh)
