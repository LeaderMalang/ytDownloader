from django.conf import settings
from django.http.response import HttpResponse
from rest_framework import status
from django.http.response import JsonResponse

from rest_framework.decorators import api_view



from pytube import YouTube
from pytube import Search

import os,shutil
import mimetypes



@api_view(['POST'])
def home(request):

    video={}
    allItem=''
    # obj=''
    urll = ''
    videos=[]
    total=0
    suggestions=[]
    if request.method == 'POST':

        urll = request.POST['search']
        try:

           
            search = Search(urll)
            total=len(search.results)
            resutls=search.results
            suggestions=search.completion_suggestions
            
        except Exception as e:

            print(e)
        if total>0:
            
            for res in resutls:
                allItem = res.streams.filter(progressive=True)
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
                    'title':res.title,
                    'id': res.video_id,
                    'url':res.watch_url,
                    'duration':int(res.length // 60),
                    'thumbnail':res.thumbnail_url,
                    'mylist':list(mylist) 
                }
                videos.append(video)

        context = {'videos': videos,"total":total,"search_suggestions":suggestions}
        return JsonResponse(context)
    return JsonResponse({"errors":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
    # return render(request, 'downloader/index.html', context)
# dwonload_path
@api_view(['POST'])
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