from .models import File, Folder
from shorturl.models import ShortUrl
from .tasks import zip_files, delete_folder

from django.contrib.sites.models import Site
from django.conf import settings

import os, shutil

# expected file types which should be zipped if received alone,
# more content-types will be added in future
content_types = [
    "application/x-shellscript",
    "text/html",
]

# to check if a single file should be zipped or not
def should_be_zipped(file):
    return file.content_type in content_types


# checking the size of files received(total size of 200MB is allowed)
def check_files_size(files):
    totalSize = 0
    for f in files:
        totalSize += f.size
        if totalSize > 200000000 or f.size > 200000000:  # size in bytes
            return False

    return True


# verify all the files and save them
def verify_data(form, files):
    context = {}

    if form.is_valid:
        folder = Folder.objects.create()
        sizeValid = check_files_size(files)

        if not sizeValid:  # checking if size>200MB
            delete_folder.delay(
                folder.name
            )  # deleting the folder if size>200MB(in the background)

            context["message"] = "Size of files is greater than 200MB"
            return False, context

        # create files if size acceptable
        for f in files:
            File.objects.create(file=f, folder=folder)

        # zipping multiple files, and some files(if received alone) of some selected content types
        if len(files) > 1 or should_be_zipped(files[0]):
            success = zip_files.delay(
                name=folder.name
            )  # sheduling the task in background

            if not success:  # if files could not be zipped
                delete_folder.delay(
                    folder.name
                )  # deleting the folder in the background
                context["message"] = "Files could not be zipped. Please try again..."
                return False, context

            folder.zipped = True
        folder.save()
        context["folder_id"] = folder.name

        return True, context  # finaly returning the status and folder id
    else:
        context["message"] = "Data not valid. Please try again..."
        return False, context


# fetch url for the files
def fetch_url(name, scheme):
    try:
        folder = Folder.objects.get(name=name)

        current_site = Site.objects.get_current()
        url = f"{scheme}://{current_site.domain}{settings.MEDIA_URL}"

        if folder.zipped:
            url += f"{folder.name}.zip"
        else:
            url += f"{folder.file_set.first().file}"

        short_url = ShortUrl.objects.create(link=url)
        short_url = f"{current_site.domain}/{short_url.id}"

        folder.delete()
        context = {"url": short_url}

    except:
        context = {"message": "Requeste resource doesn't exist."}
        return False, context

    return True, context
