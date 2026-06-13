# youtube.py

from youtube_comment_downloader import YoutubeCommentDownloader

def get_comments(url):

    downloader = YoutubeCommentDownloader()

    comments = []

    for c in downloader.get_comments_from_url(url):
        comments.append(c["text"])

    return comments