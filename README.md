# Django Template

**[Use this template](https://github.com/shin-envy/django-template/generate)**

## Usage
first usage
```ps
$ py manage.py migrate
```

install dependencies
```ps
$ pipenv install -r requirements.txt
```

start dev server
```ps
$ py manage.py runserver
```

changing port
```ps
$ py manage.py runserver 8080
```

create app on project
```ps
$ py manage.py startapp {app name}
```

## Example Code

configure app to a url directory

```py
# app/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

```py
# polls/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

```py
# polls urls/views.py

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

```py
# app/settings

INSTALLED_APPS = [
    # add
    'polls.apps.PollsConfig'
]
```

use template for view 
```py
# polls/views.py

def index(request):
    template = loader.get_template('homepage.html') # polls/templates/homepage.html
    return HttpResponse(template.render())
```