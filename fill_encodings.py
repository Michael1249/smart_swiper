from memo.url_memo import memo
import face_recognition
from utils import convertUrlToName, execTask
import image_loader
import os


def fillEncodings(accurate=5):
    urls = memo.getURLs()

    def Task(progress):
        for i, url in enumerate(urls):
            progress.update(i + 1)
            img_path = 'images/' + convertUrlToName(url)
            if memo.getUrlData(url)['encoding'] != [] or not os.path.isfile(img_path):
                continue

            img = face_recognition.load_image_file(img_path)

            locations = face_recognition.face_locations(img)

            if len(locations) == 1:
                encoding = list(face_recognition.face_encodings(
                    img, known_face_locations=locations, num_jitters=accurate)[0])

                memo.upd_urls({url: {'encoding': encoding}})
            else:
                memo.remove_urls([url])

    execTask(name='calculate encodings:', size=len(urls), task=Task)


if __name__ == '__main__':
    image_loader.load()
    fillEncodings()
