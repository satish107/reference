Tutorial 1: Serialization

serialization: First serialize data into python native datatypes and then use JSONRenderer to render into json format
	serializer = SnippetSerializer(snippet)
	serializer.data
	content = JSONRenderer().render(serializer.data)

deserialization: 
	import io
	stream = io.BytesIO(content)
	data = JSONParser().parse(stream)
	serializer = SnippetSerializer(data=data)

we restore those native datatypes into a fully populated object instance.
	serializer = SnippetSerializer(data=data)
	serializer.is_valid()
	# True
	serializer.validated_data
	# OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
	serializer.save()
	# <Snippet: Snippet object>

Using queryset with many=True

serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data
# [OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]

print(repr(serializer)) # To show all the fields with representation

#########################################################################################################################################

Tutorial 2: Requests and Responses

Request objects

request.POST  # Only handles form data.  Only works for 'POST' method.
request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.

Response objects

REST framework also introduces a Response object, which is a type of TemplateResponse that takes unrendered content 
and uses content negotiation to determine the correct content type to return to the client.

return Response(data)  # Renders to content type as requested by the client.

status code names
always return status codes name instead of only code like
return Response(serializer.data, status=status.HTTP_201_CREATED)
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

Wrapping API views
REST framework provides two wrappers you can use to write API views.
# class based views and function based views
# 1. The @api_view decorator for working with function based views.
# 2. The APIView class for working with class-based views.

# The wrappers also provide behaviour such as returning 405 Method Not Allowed responses when appropriate, and handling any ParseError exceptions that occur when accessing request.data with malformed input.

@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Adding optional format suffixes to our URLs

"""
To take advantage of the fact that our responses are no longer hardwired to a single content type 
let's add support for format suffixes to our API endpoints. Using format suffixes gives us URLs 
that explicitly refer to a given format, and means our API will be able to handle URLs such as 
http://example.com/api/items/4.json.
"""
def snippet_list(request, format=None):
def snippet_detail(request, pk, format=None):

# in urls
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = format_suffix_patterns(urlpatterns)

# Rewriting our API using class-based views

class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Using mixins
from rest_framework import mixins
from rest_framework import generics

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# Detail
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
"""
Pretty similar. Again we're using the GenericAPIView class to 
provide the core functionality, and adding in mixins to provide the .retrieve(), .update() and .destroy() actions.
"""
# Using generic class-based views
from rest_framework import generics

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


Tutorial 4: Authentication & Permissions
"""
REST framework includes a number of permission 
classes that we can use to restrict who can access a given view. In this case the one 
we're looking for is IsAuthenticatedOrReadOnly, which will ensure that authenticated requests get read-write access, 
and unauthenticated requests get read-only access.
"""
from rest_framework import permissions
permission_classes = [permissions.IsAuthenticatedOrReadOnly]

path('api-auth/', include('rest_framework.urls'))
"""
The 'api-auth/' part of pattern can actually be whatever URL you want to use.
Now if you open up the browser again and refresh the page you'll see a 'Login' link in the top right of the page. 
If you log in as one of the users you created earlier, you'll be able to create code snippets again.
"""

# Object level permissions
"""
Really we'd like all code snippets to be visible to anyone, 
but also make sure that only the user that created a code snippet is able to update or delete it.
To do that we're going to need to create a custom permission.
"""
from rest_framework import permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
"""
Now we can add that custom permission to our snippet instance endpoint, 
by editing the permission_classes property on the SnippetDetail view class:
"""
permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]






