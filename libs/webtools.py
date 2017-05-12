""" Class for Web functions """
import urllib.request

class WebTools:
    """ Class for network functions """
    @staticmethod
    def get(url, expected_response=200):
        """ Submits a GET request """
        response = urllib.request.urlopen(url)
        retval = {}
        retval['response'] = response.read()
        if response.getcode() == expected_response:
            retval['success'] = True
        return retval
