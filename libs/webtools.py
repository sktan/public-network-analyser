""" Class for Web functions """
import urllib.request
import urllib.parse

class WebTools:
    """ Class for network functions """
    @staticmethod
    def get(url, expected_response=200):
        """ Submits a GET request """
        response = urllib.request.urlopen(url)
        retval = {}
        retval['response'] = response.read()
        retval['status'] = response.getcode()
        retval['success'] = False
        if retval['status'] == expected_response:
            retval['success'] = True
        return retval
    @staticmethod
    def post(url, data, expected_response=200):
        """ Submits a POST request """
        post_data = urllib.parse.urlencode(data).encode('UTF-8')
        response = urllib.request.urlopen(url, post_data)
        retval = {}
        retval['response'] = response.read()
        retval['status'] = response.getcode()
        retval['success'] = False
        if retval['status'] == expected_response:
            retval['success'] = True
        return retval
