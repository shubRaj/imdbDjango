from django.db import models
from django.utils import timezone
# Create your models here.
class Torrent(models.Model):
    imdb_id =models.IntegerField(blank=True,null=True,unique=True)
    title = models.CharField(max_length=2083,null=True)
    rating = models.DecimalField(max_digits=10,decimal_places=1,null=True)
    genres = models.CharField(max_length=120,null=True)
    runtimes = models.CharField(max_length=10,null=True)
    year = models.IntegerField(null=True)
    directors = models.CharField(max_length=100,null=True)
    casts = models.TextField(null=True)
    cover = models.URLField(null=True)
    plot = models.TextField(null=True)
    added_on=models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        return self.title
    class Meta:
        ordering=["-added_on"]
class Magnet(models.Model):
    imdb_id = models.ForeignKey(Torrent,on_delete=models.CASCADE,related_name="torrent_magnet")
    name=models.CharField(max_length=2083)
    seeders = models.IntegerField(default=0)
    leechers = models.IntegerField(default=0)
    size = models.CharField(max_length=10,blank=True,null=True)
    magnet = models.TextField(blank=True,null=True)
    def __str__(self):
        return f"{self.imdb_id.title} magnet link"