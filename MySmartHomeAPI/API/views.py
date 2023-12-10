from django.contrib.auth.models import Group, User
from rest_framework import mixins, permissions, viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from API.serializers import GroupSerializer, UserSerializer, KitchenLightSerializer
from API.models import KitchenKeepOnSwitch


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]


class KitchenLightViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    A viewset for viewing and updating the state of the kitchen lights.

    The kitchen lights can be in one of the following states:
    - 0: Do not change light behavior
    - 1: Keep lights on
    - 2: Keep lights off

    This viewset provides two main HTTP methods:
    - GET: To retrieve the current state of the kitchen lights.
    - PUT: To update the state of the kitchen lights.
    """

    permission_classes = [permissions.IsAuthenticated]  # Add your desired permissions
    queryset = KitchenKeepOnSwitch.objects.all()
    serializer_class = KitchenLightSerializer

    def get_object(self):
        """
        Returns the singleton instance of the kitchen light.
        Overridden to handle singleton pattern.
        """
        return KitchenKeepOnSwitch.get_instance()

    def list(self, request):
        """
        Handle GET requests for the kitchen light's state.

        Returns a response with the current state of the kitchen lights.
        """
        light_switch = self.get_object()
        serializer = KitchenLightSerializer(light_switch)
        #return Response({'status': 'ok', 'state': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.data)
    
    # def retrieve(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    
    # @action(detail=False, methods=['put'])
    # def set_state(self, request, *args, **kwargs):
    #     """
    #     Handle PUT requests to update the kitchen light's state.
    #     ...
    #     """
    #     return self.update(request, *args, **kwargs)
    
    def put(self, request, pk=None):
        """
        Update the state of the kitchen light.
        Overridden to handle singleton pattern.
        """
        light_switch = self.get_object()
        serializer = self.get_serializer(light_switch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get_view_name(self):
        """
        Returns a more descriptive name for the browsable API.
        """
        return "Kitchen Light Switch"