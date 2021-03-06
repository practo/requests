import requests
import pytest


class Gobj(object):
    """ A minimal mock of flask's g.
    """
    def __init__(self, cid=None):
        self.Cid = cid


class TestRequest:
    def test_request(self, httpbin):
        r = requests.request('GET', httpbin('get'), cid=requests.new_cid())
        assert r.status_code == 200
        reqHeaders = r.json()['headers']
        assert 'Cid' in reqHeaders

    def test_request_no_explicit_cid(self, httpbin):
        r = requests.request('GET', httpbin('get'))
        assert r.status_code == 200
        reqHeaders = r.json()['headers']
        assert 'Cid' in reqHeaders

    def test_request_params(self, httpbin):
        r = requests.request('GET', httpbin('get'), cid=requests.new_cid(),
                             params={'param1': 123, 'param2': 456})
        assert r.status_code == 200
        reqQueryParams = r.json()['args']
        assert reqQueryParams['param1'] == '123'
        assert reqQueryParams['param2'] == '456'
        reqHeaders = r.json()['headers']
        assert 'Cid' in reqHeaders

    def test_request_headers(self, httpbin):
        r = requests.request('GET', httpbin('get'), cid=requests.new_cid(),
                             headers={'head1': 'air', 'head2': 'water'})
        assert r.status_code == 200
        reqHeaders = r.json()['headers']
        assert 'Cid' in reqHeaders
        assert reqHeaders['Head1'] == 'air'
        assert reqHeaders['Head2'] == 'water'

    def test_get_with_cid(self, httpbin):
        r = requests.get(httpbin('get'), cid=requests.new_cid())
        assert r.status_code == 200
        reqHeaders = r.json()['headers']
        assert 'Cid' in reqHeaders

    def test_get_with_hardcid(self, httpbin):
        r = requests.get(httpbin('get'), cid='9876')
        assert r.status_code == 200
        reqHeaders = r.json()['headers']
        assert reqHeaders['Cid'] == '9876'

    def test_post_with_cid(self, httpbin):
        r = requests.post(httpbin('post'), cid=requests.new_cid())
        assert r.status_code == 200
        reqHeaders = r.json()['headers']
        assert 'Cid' in reqHeaders

    def test_no_cid(self, httpbin):
        r = requests.get(httpbin('get'), no_cid=True)
        assert r.status_code == 200
        reqHeaders = r.json()['headers']
        assert 'Cid' not in reqHeaders

    def test_extract_cid(self):
        gobj = Gobj('98765')
        extracted_cid = requests.extract_cid(gobj)
        assert extracted_cid == '98765'

    def test_extract_without_cid(self):
        gobj = Gobj()
        assert requests.extract_cid(gobj) != None

    def test_mutate_with_cid(self, httpbin):
        r = requests.get(httpbin('get'), cid='1234')
        gobj = Gobj()
        requests.mutate_with_cid(r.request.headers, gobj)
        assert getattr(gobj, 'Cid', None) == '1234'

    def test_mutate_existing_lowecase_cid(self):
        headers1 = {'cid': '2222', 'host': 'python'}
        gobj = Gobj()
        requests.mutate_with_cid(headers1, gobj)
        assert getattr(gobj, 'Cid', None) == '2222'

    def test_lowecase_cid_extraction(self):
        headers = {'cid': '6666'}
        gobj = Gobj()
        requests.mutate_with_cid(headers, gobj)
        assert getattr(gobj, 'Cid', None) == '6666'
