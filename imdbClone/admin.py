from django.contrib import admin
from .models import Torrent,Magnet
class AdminMagnet(admin.ModelAdmin):
    search_fields = ["name","imdb_id__imdb_id"]
class AdminTorrent(admin.ModelAdmin):
    search_fields = ["title","imdb_id",]
admin.site.register(Torrent,AdminTorrent)
admin.site.register(Magnet,AdminMagnet)
# Register your models here.
