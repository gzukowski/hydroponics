from django.db import models
from django.contrib.auth.models import User

class HydroponicSystem(models.Model):
    """
    Model representing a hydroponic system owned by a user.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hydroponic_systems')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the HydroponicSystem model, returns the name of the system.
        """
        return f"{self.name}"
class Measurement(models.Model):
    """
    Model representing a measurement taken from a hydroponic system.
    """
    hydroponic_system = models.ForeignKey(
        HydroponicSystem,
        on_delete=models.CASCADE,
        related_name='measurements'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    ph = models.DecimalField(max_digits=6, decimal_places=2)
    temperature = models.DecimalField(max_digits=6, decimal_places=2)
    tds = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        """
        String representation of the Measurement model, returns details of the measurement.
        """
        return (
            f"Measurement at {self.timestamp}: "
            f"pH={self.ph}, Temp={self.temperature}°C, "
            f"TDS={self.tds} ppm"
        )
