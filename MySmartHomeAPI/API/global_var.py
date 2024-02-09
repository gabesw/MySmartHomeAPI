from rest_framework import mixins, permissions, viewsets, serializers, status
from API.models import GlobalVar
from rest_framework.response import Response

# Add a global variable to the dictionary below to make it accessible via the API.
# The format is: 'ClassName' : ('endpoint_name': str, 'descriptive_name': str, 'description': str, 'on_state': str, 'off_state': str)
global_vars = {
    "GoodMorning": ("good_morning", "\'Good Morning\' State", "A variable for storing the state of the 'Good Morning' routine on Apple Home.", "Routine has been run", "Routine has not been run"),
}

def addVarsToRouter(router):
    """
    Adds the global variables to the router. This function should be called in urls.py.
    """
    for gvar in global_vars:
        #create the names of the classes
        viewset_name = gvar + "ViewSet"
        serializer_name = gvar + "Serializer"
        model_name = gvar + "Variable"

        #unpack the tuple
        endpoint_name, descriptive_name, description, on_state, off_state = global_vars[gvar]

        #create the model
        dynamic_model = type(model_name, (GlobalVar,), {
            '__doc__': f"""
            Automatically generated Model for the {endpoint_name} variable.
            """,
            '__module__': __name__,
        })

        #define the Meta class for the serializer
        class Meta:
            model = dynamic_model
            fields = ['val']

        #define the validate function for the serializer
        def validate_val(self, value):
            """
            Check that the val is between 0 and 1.
            """
            if not (0 <= value <= 1):
                raise serializers.ValidationError("Value must be between 0 and 1.")
            return value

        #create the serializer
        dynamic_serializer = type(serializer_name, (serializers.ModelSerializer,), {
            '__doc__': f"""
            Automatically generated Serializer for the {endpoint_name} variable.
            """,

            'Meta': Meta,
            'validate_val': validate_val
        })

        #define the viewset methods
        def get_object(self):
            """
            Returns the singleton instance of the kitchen light.
            Overridden to handle singleton pattern.
            """
            return dynamic_model.get_instance()

        def list(self, request):
            """
            Handle GET requests for the variable.

            Returns a response with the current state of the variable.
            """
            variable = self.get_object()
            serializer = dynamic_serializer(variable)
            return Response(serializer.data)
        
        def put(self, request, pk=None):
            """
            Update the state of the variable.
            Overridden to handle singleton pattern.
            """
            variable = self.get_object()
            serializer = self.get_serializer(variable, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        def get_view_name(self):
            """
            Returns a more descriptive name for the browsable API.
            """
            return descriptive_name

        #create the viewset
        dynamic_viewset = type(viewset_name, (mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet), {
            #programmatically set the docstring
            '__doc__': f"""
            {description}

            Allowed states:
            - 0: (False) {off_state}
            - 1: (True) {on_state}

            This viewset provides two main HTTP methods:
            - GET: To retrieve the current state of the variable.
            - PUT: To update the variable.
            """,
            
            'permission_classes': [permissions.IsAuthenticated],
            'queryset': dynamic_model.objects.all(),
            'serializer_class': dynamic_serializer,
            'get_object': get_object,
            'list': list,
            'put': put,
            'get_view_name': get_view_name
        })
        
        #register the viewsets
        router.register(f'variables/{endpoint_name}', dynamic_viewset, basename=endpoint_name)