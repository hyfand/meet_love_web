from flask_uploads import UploadSet, IMAGES

photos = UploadSet('photos', IMAGES)
potrait = UploadSet('potrait', IMAGES)