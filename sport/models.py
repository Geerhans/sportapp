from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class BasicData(models.Model):
    Basicname = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.Basicname)
        super(BasicData, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.Basicname

class ComplicatedData(models.Model):
    BasicData = models.ForeignKey(BasicData, on_delete=models.CASCADE)
    Complicatedname = models.CharField(max_length=128)
    slug = models.SlugField(blank=True)
    def __str__(self):
        return self.Complicatedname
    
    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.Complicatedname) 
        super(ComplicatedData, self).save(*args, **kwargs)
