# Requirements
```

This project is about the search videos from youtube by providing a search term.Bot will return a list of videos.User can download any video using video id and resolution.
```

## Getting Started

### Virtual Environment
```
python -m venv env
```
#### Activate the virtual environment
##### Linux Environment
```
source ./env/bin/activate
```
##### Windows Environment
```
.\env\Script\activate
```
### installing requirements 
 ```
pip install -r requirements.txt
 ```

 #### Start Bot 

 ```
 python manage.py runserver
 ```

  #### Rest Api's

##### Search Videos 

return a list of Videos 


 ```
 Method POST 

 URL /search

 Body formdata 

 search =Coke Studio


 ```

##### Download Videos 

  ```
 Method POST 

 URL /download/<VideoID>

 Body formdata 

 choice =22


 ```