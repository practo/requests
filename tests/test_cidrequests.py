import requests
import pytest


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

    def test_extract_cid(self, httpbin):
        dummy_req = requests.models.Request()
        dummy_req.headers['Cid'] = '98765'
        extracted_cid = requests.extract_cid(dummy_req)
        assert extracted_cid == '98765'

    def test_mutate_with_cid(self, httpbin):
        r = requests.get(httpbin('get'), cid='1234')
        new_header = requests.mutate_with_cid(r.request.headers)
        assert new_header['Cid'] == '1234'
        del new_header['Cid']
        assert 'Cid' not in new_header
        new_header2 = requests.mutate_with_cid(new_header)
        assert 'Cid' in new_header2
