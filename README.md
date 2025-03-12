# My portfolio, made with django.

Feel free to clone and try the apps. Report issues also, please... :slightly_smiling_face:
# Apps:
## 1. File sharing app
A simple file sharing app, with nice features like background tasks for zipping and deleting files to reduce response time and imporve end user experience.
Multiple files are zipped in the background, meanwhile the user is served a shorturl, through a Url Shortener.
Background tasks are performed through [Celery](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html) as a Daemon(systemd), and [Redis](https://redis.io/docs/getting-started/) as task broker.

![File Share](https://github.com/vallabhtiwari/portfolio/blob/main/base/static/base/fileshare.png)

## 2. Url shortener
A simple url shortener.

![Url Shortener](https://github.com/vallabhtiwari/portfolio/blob/main/base/static/base/shorturl.png)

## P.S.:- Don't forget to check the Game :wink:
