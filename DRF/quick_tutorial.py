Requests
_____________________________________________________________________________________________

request.data
request.query_params
request.parsers
request.accepted_renderer
request.user
request.auth
request.authenticators
request.method
request.content_type, request.META.get('HTTP_CONTENT_TYPE')
request.stream


Responses
_____________________________________________________________________________________________

Response(data, status=None, template_name=None, headers=None, content_type=None)
response = Response()
response.data
response.status_code
response.content
response.template_name
response.accepted_renderer
response.accepted_media_type
response.renderer_context
response['cache-control'] = 'no-cache'
response.render()

Views
_____________________________________________________________________________________________

Decorators:
@api_view(['GET' 'POST'])
@renderer_classes(...)
@parser_classes(...)
@authentication_classes(...)
@permission_classes(...)
# Each of these decorators takes a single argument which must be a list or tuple of classes.
@schema(CustomAutoSchema()) or @schema(None)

Serializers
_____________________________________________________________________________________________

































