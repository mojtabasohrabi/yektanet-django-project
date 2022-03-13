class GetUserIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            request.ip = x_forwarded_for.split(',')[0]
        else:
            request.ip = request.META.get('REMOTE_ADDR')

        response = self.get_response(request)

        return response
