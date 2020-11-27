from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from . import imdbFetcher
from imdb import IMDb
from .torrentScrapper import TorrentInfo
import re
from django.contrib import messages
from .models import Magnet,Torrent
class Home(View):
    regex = re.compile("\d+")
    def get(self,request,*args,**kwargs):
        imdbid = kwargs.get("id")
        if imdbid and (len(imdbid)>=7 and len(imdbid)<=9)and self.regex.search(imdbid) is not None:
            if Torrent.objects.filter(imdb_id=imdbid).exists():
                torrent = Torrent.objects.get(imdb_id=imdbid)
            else:
                ia = IMDb()
                movie = ia.get_movie(imdbid)
                plot = movie.get("plot"," ")[0]
                rating = movie.get("rating","0.0")
                genres = ",".join(movie.get("genres",[]))
                runtimes="".join(movie.get("runtimes",[]))
                year = movie.get("year",2000)
                directors = ",".join([director.get("name","") for director in movie.get("directors",[])])
                casts = ",".join([cast.get("name","") for cast in movie.get("cast",[])])
                cover=movie.get("cover url")
                title = movie.get("title","none").lower().replace(":","")
                torrents = TorrentInfo(title)
                torrents.num_pages(pages=1)
                torrents = torrents.json()
                imdb_id=Torrent.objects.create(imdb_id=int(imdbid),title=title,plot=plot,genres=genres,rating=rating,runtimes=runtimes,year=year,directors=directors,casts=casts,cover=cover)
                for torrent in range(1,len(torrents)+1):
                    ndx = str(torrent)
                    name=torrents[ndx].get("name").lower()
                    if title in name and str(year) in name:
                        Magnet.objects.create(imdb_id=imdb_id,name=torrents[ndx].get("name"),seeders=torrents[ndx].get("seeders"),leechers=torrents[ndx].get("leechers"),size=torrents[ndx].get("size"),magnet=torrents[ndx].get("url"))
                torrent = Torrent.objects.get(imdb_id=imdbid)
            return render(request,"imdbClone/detail.html",{"torrent":torrent})
        elif imdbid:
            messages.add_message(request,messages.WARNING,"Invalid ID",fail_silently=True)
        return render(request,"imdbClone/home.html")
    def post(self,request,*args,**kwargs):
        objects = [obj for obj in imdbFetcher.ImdbApi(request.POST.get("query")).json() if obj.get("i") and self.regex.search(obj.get("id")) and not obj.get("id").startswith("nm")]
        paginate = Paginator(objects,6)
        if request.POST.get("page"):
            objects = paginate.page(request.POST.get("page"))
        else:
            objects = paginate.page(1)
        return render(request,"imdbClone/home.html",{"objects":objects})