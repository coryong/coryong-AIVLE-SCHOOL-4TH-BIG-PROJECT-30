from django.db import models

class UserTable(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)  # Ideally use Django's built-in User model

    class Meta:
        db_table = 'userTable'

class PostTable(models.Model):
    user = models.ForeignKey(UserTable, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'postTable'
        
# class PostTable(models.Model):
#     user = models.ForeignKey(UserTable, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'postTable'
        
        