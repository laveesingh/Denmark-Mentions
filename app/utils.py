import xlwt
import re
import datetime
import time

from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q

def export_to_excel(keywords, context):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="results.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')
    row_num = 0
    count_total = context['fb_comments_count'] + \
            context['fb_posts_count'] + context['yt_comments_count']
    font = xlwt.XFStyle()
    bold_font = xlwt.XFStyle()
    bold_font.bold = True
    ws.write(0, 0, "SEARCH RESULTS", bold_font)
    ws.write(0, 1, count_total, bold_font)
    ws.write(1, 0, "KEYWORDS", bold_font)
    ws.write(1, 1, keywords, bold_font)

    ws.write(4, 0, "Facebook Comments", bold_font)
    ws.write(4, 1, context['fb_comments_count'], bold_font)
    cols = ['id', 'username', 'timestamp', 'message']
    for col_num in xrange(len(cols)):
        ws.write(5, col_num, cols[col_num], bold_font)
    row_num = 6
    for comment in context['fb_comments']:
        ws.write(row_num, 0, comment.comment_id, font)
        ws.write(row_num, 1, comment.username, font)
        ws.write(row_num, 2, str(comment.timestamp), font)
        ws.write(row_num, 3, comment.message, font)
        row_num += 1

    row_num += 1
    ws.write(row_num, 0, "Facebook Posts", bold_font)
    ws.write(row_num, 1, context['fb_posts_count'], bold_font)
    row_num += 1
    cols = ['id', 'pagename', 'timestamp', 'message']
    for col_num in xrange(len(cols)):
        ws.write(row_num, col_num, cols[col_num], bold_font)
    row_num += 1
    for post in context['fb_posts']:
        ws.write(row_num, 0, post.post_id, font)
        ws.write(row_num, 1, post.pagename, font)
        ws.write(row_num, 2, str(post.timestamp), font)
        ws.write(row_num, 3, post.message, font)
        row_num += 1

    row_num += 1
    ws.write(row_num, 0, 'Youtube Comments', bold_font)
    ws.write(row_num, 1, context['yt_comments_count'], bold_font)
    row_num += 1
    cols = ['id', 'username', 'timestamp', 'video', 'comment']
    for col_num in xrange(len(cols)):
        ws.write(row_num, col_num, cols[col_num], bold_font)
    row_num += 1
    for comment in context['yt_comments']:
        ws.write(row_num, 0, comment.comment_id, font)
        ws.write(row_num, 1, comment.username, font)
        ws.write(row_num, 2, str(comment.timestamp), font)
        ws.write(row_num, 3, comment.video, font)
        ws.write(row_num, 4, comment.message, font)
        row_num += 1

    row_num += 1
    ws.write(row_num, 0, 'Tweets', bold_font)
    ws.write(row_num, 1, context['tweets_count'], bold_font)
    row_num += 1
    cols = ['id', 'username', 'timestamp', 'tweet']
    for col_num in xrange(len(cols)):
        ws.write(row_num, col_num, cols[col_num], bold_font)
    row_num += 1
    for tweet in context['tweets']:
        ws.write(row_num, 0, tweet.tweet_id, font)
        ws.write(row_num, 1, tweet.username, font)
        ws.write(row_num, 2, str(tweet.timestamp), font)
        ws.write(row_num, 3, tweet.message, font)
        row_num += 1

    wb.save(response)
    return response


def sort_by_key_occ(obj_list, keywords):
    for i in xrange(len(obj_list)):
        freq = 0
        for keyword in keywords:
            if keyword in obj_list[i].message:
                freq += 1
        obj_list[i] = (freq, obj_list[i])
    obj_list.sort(key=lambda x: x[0], reverse=True)
    for i in xrange(len(obj_list)):
        obj_list[i] = obj_list[i][1]


def highlight_occurrences(keywords, results):
    for i in xrange(len(results['fb_comments'])):
        for keyword in keywords.split():
            results['fb_comments'][i].message = results['fb_comments'][i].message.lower().replace(keyword.lower(), 
                    '<span style="background-color: yellow; ">'+keyword+'</span>')
    for i in xrange(len(results['fb_posts'])):
        for keyword in keywords.split():
            results['fb_posts'][i].message = results['fb_posts'][i].message.lower().replace(keyword.lower(), 
                    '<span style="background-color: yellow; ">'+keyword+'</span>')
    for i in xrange(len(results['yt_comments'])):
        for keyword in keywords.split():
            results['yt_comments'][i].message = results['yt_comments'][i].message.lower().replace(keyword.lower(), 
                    '<span style="background-color: yellow; ">'+keyword+'</span>')
    for i in xrange(len(results['tweets'])):
        for keyword in keywords.split():
            results['tweets'][i].message = results['tweets'][i].message.lower().replace(keyword.lower(), 
                    '<span style="background-color: yellow; ">'+keyword+'</span>')



def extract_search_elements(qstring, users):
    keywords = re.findall(r'(\w[\w\s]*)', qstring)
    users = re.findall(r'(\w[\w\s]*)', users)
    return (keywords, users)


def validate_timestamp(timestamp):
    time_tuple = datetime.datetime.strptime(timestamp, '%d-%m-%Y').timetuple()
    timestamp = time.mktime(time_tuple)
    timestamp = datetime.datetime.fromtimestamp(timestamp)
    timestamp = timezone.make_aware(timestamp)
    return timestamp


def fetch_filters(keywords, usernames, userids, timestamp):
    keywords_filter = Q()
    fbc_user_filter = Q()
    fbp_user_filter = Q()
    ytc_user_filter = Q()
    tweet_user_filter = Q()
    for keyword in keywords:
        keywords_filter |= Q(message__icontains=keyword)
    for username in usernames:
        fbc_user_filter |= Q(username__iequals=username)
        fbp_user_filter |= Q(pagename__iequals=username)
        ytc_user_filter |= Q(username__iequals=username)
        tweet_user_filter |= Q(username__iequals=username)
    for userid in userids:
        fbc_user_filter |= Q(user_id__iequals=username) | Q(page_id__iequals=username)
        fbp_user_filter |= Q(page_id__iequals=username)
        ytc_user_filter |= Q(channel_id__iequals=username)
        tweet_user_filter |= Q(user_id__iequals=username)
    if timestamp:
        timestamp_filter = Q(timestamp_gt=timestamp)
        return (keywords_filter & timestamp_filter, fbc_user_filter & timestamp_filter, fbp_user_filter & timestamp_filter, ytc_user_filter & timestamp_filter, tweet_user_filter & timestamp_filter)
    return (keywords_filter, fbc_user_filter, fbp_user_filter, ytc_user_filter, tweet_user_filter)

