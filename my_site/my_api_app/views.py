from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from .serializers import GroupSerializer
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin
from shop_app.models import Product


@api_view()
def hello_api_view(request: Request):
    return Response({'message': 'Hello World API'})



class GroupListView(ListCreateAPIView):
    queryset = Product.objects.all().order_by('pk')
    serializer_class = GroupSerializer

    # def get(self, request: Request) -> Response:
    #     return self.list(request)
        # groups = Group.objects.all()
        # # data = [group.name for group in groups]
        # serialized = GroupSerializer(groups, many=True)
        # return Response({'groups': serialized.data})


