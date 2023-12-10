from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from API.serializers import GroupSerializer, UserSerializer
from API.models import KitchenKeepOnSwitch


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]

@api_view(['GET', 'PUT'])
def kitchen_lights_keep_on(request, val=None):
    '''
    View to handle the kitchen lights keep on request. When called with a GET
    request it returns the value of the switch:
        0 - do not change light behavior
        1 - keep lights on
        2 - keep lights off
    When called with a POST request it sets the value of the switch to val.

    Parameters:
        request (request) - the request object
        val (int) - the value to set the switch to
    '''
    light_switch = None
    try:
        light_switch = KitchenKeepOnSwitch.get_instance()
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == 'GET':
        return Response({'status': 'ok', 'state': light_switch.val}, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if val is not None:
            # Update the light state
            light_switch.val = val
            light_switch.save()
            return Response({'status': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
        else:
            # Handle case where 'val' is not provided
            return Response({'status': 'error', 'message': 'No value provided'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'status': 'not ok'})