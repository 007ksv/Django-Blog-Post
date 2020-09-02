from django.contrib import admin
from polls.models import Post
from polls.models import Profile

# Register your models here.
admin.site.register(Post)
admin.site.register(Profile)
