from django.db import models


class Meal(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)

    def __str__(self):
        return self.name
        
  #class Side(models.Model):
   # meal = models.ForeignKey(Meal, related_name='sides', on_delete=models.CASCADE)
    #name = models.CharField(max_length=100)
    #price = models.DecimalField(max_digits=6, decimal_places=2)
    
    #def __str__(self):
     #   return f"{self.name} - {self.price}"  
    
