from django.db import models

class BehaviourSwitch(models.Model):
    '''
    Model to represent a switch with a value that changes the behaviour of a device. 
    The value can be used to store the state of the switch. The default should be
    no change (0).
    '''
    val = models.IntegerField(default=0)

    # ensure singleton
    def save(self, *args, **kwargs):
        if not self.pk and BehaviourSwitch.objects.exists():
            # If trying to save a new instance and an instance already exists, raise an error
            raise Exception("An instance of this switch already exists.")
        return super(BehaviourSwitch, self).save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        '''
        Getter for singleton instance
        '''
        instance, created = cls.objects.get_or_create(pk=1)
        return instance
    
    class Meta:
        abstract = True

class KitchenKeepOnSwitch(BehaviourSwitch):
    '''
    Model to represent the switch that controls the 'keep-on' behaviour of the kitchen lights.
    '''
    pass