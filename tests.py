__author__ = 'Matthew'
import unittest
from pdfparser import getTextFromFirstPage
from pdfparser import extractFirstPageContent
import hashlib
from collections import OrderedDict

class TestPDFParser(unittest.TestCase):

    def test_checkPDFText(self):
        hash = hashlib.md5(getTextFromFirstPage('example.pdf').encode(encoding= 'UTF-8')).hexdigest()
        self.assertEqual(hash, "5fea1ebb094ffc8c6ac31ab1c804fe36")
    def test_checkFirstPageArray(self):
        po=extractFirstPageContent(getTextFromFirstPage('example.pdf'))
        DVArray = {'DV PROTECTIVE': OrderedDict([('FEMALE', '93'), ('MALE', '211'), ('UNKNOWN', '9'), ('Total Orders', '313')]), 'JUVENILE PEACE': OrderedDict([('FEMALE', '9'), ('MALE', '3'), ('Total Orders', '12')]), 'PEACE': OrderedDict([('FEMALE', '71'), ('MALE', '70'), ('UNKNOWN', '5'), ('Total Orders', '146')])}
        self.assertEqual(po,DVArray)
    def test_notAllElementsFirstPage(self):
        po=extractFirstPageContent(getTextFromFirstPage('example2.pdf'))
        DVArray = {'DV PROTECTIVE': OrderedDict([('FEMALE', '1'), ('MALE', '6'), ('Total Orders', '7')]), 'PEACE': OrderedDict([('MALE', '5'), ('Total Orders', '5')])}
        self.assertEqual(po,DVArray)
if __name__ == '__main__':
    unittest.main()