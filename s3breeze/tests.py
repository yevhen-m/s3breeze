import json

from unittest import TestCase

from .main import double_json_formatter, json_formatter, xml_formatter


class FormattersTestCase(TestCase):
    maxDiff = None

    def test_xml_formatter(self):
        value = "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\"><soap:Body><soap:Fault><faultcode>soap:Server</faultcode><faultstring></faultstring><detail><code></code><detail></detail></detail></soap:Fault></soap:Body></soap:Envelope>"  # noqa
        self.assertTrue(xml_formatter(value))

    def test_json_formatter(self):
        value = '{"result": []}'
        self.assertTrue(json_formatter(value))

    def test_double_json_formatter(self):
        value = json.dumps('{"result": []}')
        self.assertTrue(double_json_formatter(value))
