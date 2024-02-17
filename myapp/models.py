from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Posts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    title=models.CharField(max_length=200)
    post_image=models.ImageField(upload_to="post_pics",null=True,blank=True)
    description=models.CharField(max_length=200,null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(User,related_name="likes")

    def __str__(self) -> str:
        return self.title

class Stories(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="story")
    title=models.CharField(max_length=200)
    picture=models.ImageField(upload_to="story_pics",null=True,blank=True)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comment")
    text=models.CharField(max_length=400)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text
    

class UserProfile(models.Model):
    profile_picture=models.ImageField(upload_to="profile_pics",null=True,blank=True)
    bio=models.CharField(max_length=200)
    dob=models.DateField()
    phone=models.CharField(max_length=200)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    following=models.ManyToManyField(User,related_name="followings")
    block=models.ManyToManyField(User,related_name="blocks")
    saved_post=models.ManyToManyField(Posts,related_name="postsave")

    def __str__(self) -> str:
        return self.user.username