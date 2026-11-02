from django.db import models

# Create your models here.
class usersign(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    gmail = models.EmailField()
    password = models.CharField(max_length=12)

class story(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    myfile = models.FileField(upload_to="MyStory")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(usersign,on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return self.title


class BlogLike(models.Model):
    user = models.ForeignKey(usersign, on_delete=models.CASCADE)
    post = models.ForeignKey(story, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class BlogComment(models.Model):
    user = models.ForeignKey(usersign, on_delete=models.CASCADE)
    post = models.ForeignKey(story, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Follow(models.Model):
    follower = models.ForeignKey(
        usersign,
        on_delete=models.CASCADE,
        related_name="following"
    )

    following = models.ForeignKey(
        usersign,
        on_delete=models.CASCADE,
        related_name="followers"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.firstname} follows {self.following.firstname}"