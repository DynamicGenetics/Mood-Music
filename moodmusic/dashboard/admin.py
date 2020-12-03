from django.contrib import admin
from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from social_django.models import Nonce, Association

# Using dashboard as a central admin panel editor

admin.site.site_header = "Mood Music Admin Dashboard"

# Deregister models that we don't actually want on the admin side
admin.site.unregister(Group)
# Unused parts of Django All Auth (allauth.socialaccount)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialApp)
# Unused parts of Python Social Auth (social_django)
admin.site.unregister(Nonce)
admin.site.unregister(Association)
