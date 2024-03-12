from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied


class FilterRequestsMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print("REQUEST Middleware is working")
        # print("User agent is::", request.META['HTTP_USER_AGENT'])
        # blacklisted_ips = ['192.42.116.179', '192.42.116.181', '192.42.116.192',
        #                    '19.116.2.42203', '192.42.116.211', '208.105.35.90',
        #                    '216.245.101.153', '24.112.42.86', '24.153.162.170',
        #                    '24.73.199.94', '51.89.153.112', '96.69.48.11']
        #
        # if request.META['REMOTE_ADDR'] in blacklisted_ips:
        #     raise PermissionDenied

        # app-version checking

        allowed_app_versions = ['2.3.1', '2.3.2', '2.3.3', '2.3.4']
        app_version = request.META.get('HTTP_APP_VERSION')
        if app_version not in allowed_app_versions:
            raise PermissionDenied
        return None

    def process_response(self, request, response):
        print("RESPONSE Middleware is working")
        # TODO::  Check response for any sensitive data[ password,email,aadhar no. etc.]
        print("Response content::", response.content)
        return response
