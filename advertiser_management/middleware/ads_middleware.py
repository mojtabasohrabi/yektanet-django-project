from advertiser_management.models import Ad, View, Click


class GetUserIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            request.ip = x_forwarded_for.split(',')[0]
        else:
            request.ip = request.META.get('REMOTE_ADDR')

        request_path = request.path
        if request_path == '/ads/':
            all_ads = Ad.objects.all()
            for ad in all_ads.iterator():
                View.insert_view(ad.id, request.ip)
        elif "click" in request_path:
            ad_id = request_path.find("click/")
            Click.insert_click(ad_id, request.ip)

        response = self.get_response(request)

        return response
