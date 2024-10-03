import re
from flask import request

class IPInfo(object):
    """IP."""

    @property
    def browser(self):
        """Browser type."""
        ua = request.headers.get('User-Agent')
        if (ua):
            browser = ua
            if (re.compile(r'MicroMessenger', re.I).search(ua)):
                browser = 'WeChat'
            elif (re.compile(r'MinxingMessenger', re.I).search(ua)):
                browser = 'MinxingMessenger'
            elif (re.compile(r'QQ', re.I).search(ua)):
                browser = 'TencentQQ'
            elif (re.compile(r'MSIE', re.I).search(ua) or re.compile(r'rv:([^\)]+)\) like Gecko', re.I).search(ua)):
                browser = 'MSIE'
            elif (re.compile(r'Firefox', re.I).search(ua)):
                browser = 'Firefox'
            elif (re.compile(r'Chrome', re.I).search(ua)):
                browser = 'Chrome'
            elif (re.compile(r'Safari', re.I).search(ua)):
                browser = 'Safari'
            elif (re.compile(r'Opera', re.I).search(ua)):
                browser = 'Opera'
            return(browser)
        else:
            return('Unknown')

    @property
    def lang(self):
        """Browser language."""
        lang = request.headers.get('Accept-Language')
        if (lang):
            if (re.compile(r'zh-cn', re.I).search(lang)):
                lang = '简体中文'
            elif (re.compile(r'zh', re.I).search(lang)):
                lang = '繁体中文'
            else:
                lang = 'English'
            return(lang)
        else:
            return('Unknown')

    @property
    def os(self):
        """Customer operation system."""
        ua = request.headers.get('User-Agent')
        if (ua):
            if (re.compile(r'win', re.I).search(ua)):
                os = 'Windows'
            elif (re.compile(r'iphone', re.I).search(ua)):
                os = 'iPhone'
            elif (re.compile(r'mac', re.I).search(ua)):
                os = 'MAC'
            elif (re.compile(r'android', re.I).search(ua)):
                os = 'Android'
            elif (re.compile(r'linux', re.I).search(ua)):
                os = 'Linux'
            elif (re.compile(r'unix', re.I).search(ua)):
                os = 'Unix'
            elif (re.compile(r'bsd', re.I).search(ua)):
                os = 'BSD'
            else:
                os = 'Other'
            return(os)
        else:
            return('Unknown')

    @property
    def ipaddress(self):
        """IP address."""
        ip = request.remote_addr
        if (ip):
            return(ip)
        else:
            return('Unknown')