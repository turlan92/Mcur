from django.db import models

class PiImage(models.Model):
    camera = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='pi_images/%Y/%m/%d/')
    timestamp = models.DateTimeField(blank=True, null=True)  # время Pi
    received = models.DateTimeField(auto_now_add=True)       # время сервера

    def __str__(self):
        return f"{self.camera} | {self.timestamp or self.received}"
