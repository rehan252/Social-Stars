from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    post = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    post_image = models.ImageField(upload_to='post_img', null=True, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.post) + ':' + str(self.value)

    class Meta:
        unique_together = ('user', 'post', 'value')


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True,
                                     on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.add(new_friend)

    @classmethod
    def unfriend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.remove(new_friend)

