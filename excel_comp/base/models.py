from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    firt_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100, blank=True)
    email = models.EmailField(unique = True)
    bio=models.TextField(null=True)
    image=models.ImageField(null= True, default = 'default.jpg', upload_to='profile_pics')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


TRACK_CHOICES = (
    ('FRONTEND', 'frontend'),
    ('BACKEND', 'backend'),
    ('FULL_STACK', 'full_stack'),
    ('PRODUCT_DESIGN', 'product_design')
)

# class Student_csv(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100)
#     phone_number = models.IntegerField()
#     track = models.CharField(max_length=20, choices = TRACK_CHOICES)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # def __str__(self):
    #     return self.first_name

class File(models.Model):
    file = models.FileField(upload_to="files")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.file.name
    
    class Meta:
        ordering = ['-created_at']

