import time

import requests as http_requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import section_required

YOUTUBE_API = 'https://www.googleapis.com/youtube/v3'
CACHE_TTL   = 3600  # seconds

# Module-level in-memory cache (works fine for single-process; for multi-worker
# deployments you can swap this for Django cache / Redis)
_cache: dict = {}
_cache_ts: dict = {}


def _get(key):
    if key in _cache and time.time() - _cache_ts.get(key, 0) < CACHE_TTL:
        return _cache[key]
    return None


def _set(key, value):
    _cache[key]    = value
    _cache_ts[key] = time.time()


def _api_key():
    return getattr(settings, 'YOUTUBE_API_KEY', '')


def _channel_id():
    return getattr(settings, 'YOUTUBE_CHANNEL_ID', '')


class VideoListView(APIView):
    permission_classes = [section_required('videos')]

    def get(self, request):
        api_key    = _api_key()
        channel_id = _channel_id()
        if not api_key or not channel_id:
            return Response({'detail': 'YouTube integration not configured.'}, status=503)

        page_token = request.query_params.get('pageToken', '')
        cache_key  = f'videos:list:{page_token}'
        cached     = _get(cache_key)
        if cached:
            return Response(cached)

        # 1. Resolve the channel's uploads playlist ID
        playlist_key = f'channel:playlist:{channel_id}'
        playlist_id  = _get(playlist_key)

        if not playlist_id:
            ch_resp = http_requests.get(
                f'{YOUTUBE_API}/channels',
                params={'key': api_key, 'id': channel_id, 'part': 'contentDetails'},
                timeout=10,
            )
            if ch_resp.status_code != 200:
                return Response({'detail': 'YouTube API error.'}, status=502)
            items = ch_resp.json().get('items', [])
            if not items:
                return Response({'results': [], 'next_page_token': None, 'prev_page_token': None})
            playlist_id = items[0]['contentDetails']['relatedPlaylists']['uploads']
            _set(playlist_key, playlist_id)

        # 2. Fetch playlist items
        params = {
            'key':        api_key,
            'playlistId': playlist_id,
            'part':       'snippet',
            'maxResults': 20,
        }
        if page_token:
            params['pageToken'] = page_token

        pl_resp = http_requests.get(f'{YOUTUBE_API}/playlistItems', params=params, timeout=10)
        if pl_resp.status_code != 200:
            return Response({'detail': 'YouTube API error.'}, status=502)

        pl_data = pl_resp.json()
        results = []
        for item in pl_data.get('items', []):
            sn     = item['snippet']
            vid_id = sn['resourceId']['videoId']
            thumbs = sn.get('thumbnails', {})
            thumb  = (
                thumbs.get('maxres') or
                thumbs.get('high')   or
                thumbs.get('medium') or
                thumbs.get('default', {})
            )
            results.append({
                'id':            vid_id,
                'title':         sn.get('title', ''),
                'description':   (sn.get('description') or '')[:280],
                'thumbnail':     thumb.get('url', ''),
                'published_at':  sn.get('publishedAt', ''),
                'channel_title': sn.get('channelTitle', ''),
            })

        data = {
            'results':          results,
            'next_page_token':  pl_data.get('nextPageToken'),
            'prev_page_token':  pl_data.get('prevPageToken'),
        }
        _set(cache_key, data)
        return Response(data)


class VideoDetailView(APIView):
    permission_classes = [section_required('videos')]

    def get(self, request, video_id):
        api_key = _api_key()
        if not api_key:
            return Response({'detail': 'YouTube integration not configured.'}, status=503)

        cache_key = f'video:detail:{video_id}'
        cached    = _get(cache_key)
        if cached:
            return Response(cached)

        resp = http_requests.get(
            f'{YOUTUBE_API}/videos',
            params={
                'key':  api_key,
                'id':   video_id,
                'part': 'snippet,statistics,contentDetails',
            },
            timeout=10,
        )
        if resp.status_code != 200:
            return Response({'detail': 'YouTube API error.'}, status=502)

        items = resp.json().get('items', [])
        if not items:
            return Response({'detail': 'Video not found.'}, status=404)

        item  = items[0]
        sn    = item['snippet']
        stat  = item.get('statistics', {})
        thumbs = sn.get('thumbnails', {})
        thumb  = (
            thumbs.get('maxres') or
            thumbs.get('high')   or
            thumbs.get('medium') or
            thumbs.get('default', {})
        )

        data = {
            'id':            video_id,
            'title':         sn.get('title', ''),
            'description':   sn.get('description', ''),
            'thumbnail':     thumb.get('url', ''),
            'published_at':  sn.get('publishedAt', ''),
            'channel_title': sn.get('channelTitle', ''),
            'view_count':    stat.get('viewCount', '0'),
            'like_count':    stat.get('likeCount', '0'),
            'embed_url':     f'https://www.youtube.com/embed/{video_id}?rel=0',
        }
        _set(cache_key, data)
        return Response(data)
