from django.db import models
from django.contrib.auth.models import User

class HydroponicSystem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hydroponic_systems')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Measurement(models.Model):
    hydroponic_system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE, related_name='measurements')
    timestamp = models.DateTimeField(auto_now_add=True)
    ph = models.DecimalField(max_digits=6, decimal_places=2)
    temperature = models.DecimalField(max_digits=6, decimal_places=2)
    tds = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"placeholder"