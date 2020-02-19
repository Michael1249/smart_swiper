from memo.url_memo import memo
import face_recognition
from utils import convertUrlToName
import image_loader
import progressbar


def fillEncodings(accurate=5):
    urls = memo.getURLs()
    bar = progressbar.ProgressBar(maxval=len(urls),
                                  widgets=['calculate encodings:', progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

    bar.start()
    for i, url in enumerate(urls):
        bar.update(i + 1)
        if memo.getUrlData(url)['encoding'] != []:
            continue

        img = face_recognition.load_image_file(
            'images/' + convertUrlToName(url))

        locations = face_recognition.face_locations(img)

        if len(locations) == 1:
            encoding = list(face_recognition.face_encodings(
            img, known_face_locations = locations, num_jitters=accurate)[0])
        
            memo.upd_urls({url: {'encoding': encoding}})
        else:
            memo.remove_urls([url])
    bar.finish()


if __name__ == '__main__':
    image_loader.load()
    fillEncodings()
