from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from django.http.response import HttpResponse
# import requests
# from isodate import parse_duration
from pytube import YouTube
# from pytube import Playlist
import os,shutil
import mimetypes

# SAVE_PATH = "C:\\python_projects\\ytDjango\\Downloader\\yt\\static\\videos\\"


def home(request):

    video={}
    allItem=''
    obj=''
    urll = ''
    if request.method == 'POST':

        urll = request.POST['ytUrl']
        try:

            obj = YouTube(urll)
            #.filter(file_extension='mp4')
            allItem = obj.streams.filter(progressive=True)
        except Exception as e:

            print(e)
        itag = []
        vformat = []
        for Item in allItem:

            try:

                if Item.resolution and int(Item.resolution[:-1]) not in vformat:
                    itag.append(Item.itag)
                    vformat.append(int(Item.resolution[:-1]))
            except Exception as e:

                print(e)

        vformat.sort(reverse=True)

        mylist = zip(itag, vformat)
        video = {
            'title':obj.title,
            'id': obj.video_id,
            'url':urll,
            'duration':int(obj.length // 60),
            'thumbnail':obj.thumbnail_url,
            'mylist': mylist
        }
        # videos.append(video)

    context = {'video': video}

    return render(request, 'downloader/home.html', context)
# dwonload_path

def download(request, id):

    if request.method == 'POST':

        choice = request.POST['choice']
        urll = f'https://www.youtube.com/watch?v={id}'
        try:

            obj = YouTube(urll).streams.get_by_itag(choice).download(settings.STATIC_ROOT)
        except Exception as e:
            print(e)
    path = open(obj, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(obj)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    path.close()
    #delete file 
    try:
        if os.path.isfile(obj) or os.path.islink(obj):
            os.unlink(obj)
        elif os.path.isdir(obj):
            shutil.rmtree(obj)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (obj, e))
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=video_download.mp4"
    # Return the response value
    return response
    # return redirect('home')


# def playlist(request):

#     return render(request, 'downloader/playlist.html', context={})

# def playlistDownload(request):
#     if request.method == 'POST':
#         url = request.POST['searchField']
#         playlistr = Playlist(url)
#         for video in playlistr:
#             video.streams.get_highest_resolution().download('')
#     return redirect('playlistt')