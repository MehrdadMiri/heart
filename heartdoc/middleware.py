"""
Custom HTMX middleware to detect htmx requests without external dependency.
"""
class HtmxMiddleware:
    """
    Attaches a boolean `htmx` attribute to the request,
    indicating whether it's an HTMX request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # HX-Request header is 'true' for HTMX requests
        htmx_header = request.META.get('HTTP_HX_REQUEST')
        # Some frameworks use 'HX-Request' key in headers
        if htmx_header is None:
            htmx_header = request.headers.get('HX-Request') if hasattr(request, 'headers') else None
        request.htmx = (htmx_header == 'true')
        return self.get_response(request)