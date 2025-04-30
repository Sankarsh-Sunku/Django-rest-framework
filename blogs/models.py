from django.db import models

# Create your models here.
class Blog(models.Model):
    blog_title = models.CharField(max_length=200)
    blog_body = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.blog_title
    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment