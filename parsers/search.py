from config import yt

from enum import Enum
from dataclasses import dataclass
from typing import Any

from exceptions import ApiServiceError


class SearchResultsItemType(Enum):
    SONG = 'song'
    VIDEO = 'video'
    ALBUM = 'album'
    ARTIST = 'artist'
    PLAYLIST = 'playlist'
    COMMUNITY_PLAYLIST = 'community_playlist'
    FEATURED_PLAYLIST = 'featured_playlist'
    UPLOADS = 'uploads'


@dataclass(slots=True, frozen=True)
class Artist:
    id: str
    name: str


@dataclass(slots=True, frozen=True)
class SearchResultsItem:
    type: SearchResultsItemType
    id: str
    title: str
    artists: list[Artist]
    duration: str
    thumbnailURL: str


class SearchSource(Enum):
    YOUTUBE = 'youtube'
    SPOTIFY = 'spotify'


def search(query: str, search_source: SearchSource)\
        -> list[SearchResultsItem]:
    match search_source:
        case SearchSource.YOUTUBE:
            return search_youtube(query)
        case SearchSource.SPOTIFY:
            return search_spotify(query)


def search_youtube(query: str) -> list[SearchResultsItem]:
    search_results = yt.search(query, 'songs')
    formatted_search_results = list(
        map(_format_search_results_item, search_results))

    return formatted_search_results


def search_spotify(query: str) -> list[SearchResultsItem]:
    return search_youtube(query)


def _format_search_results_item(response_item: dict[str, Any]) -> SearchResultsItem:
    try:
        return SearchResultsItem(
                type=response_item['resultType'],
                id=response_item['videoId'],
                title=response_item['title'],
                artists=response_item['artists'],
                duration=response_item['duration'],
                thumbnailURL=f'https://myserver.com/{_parse_image_id(response_item)}'
        )

    except (IndexError, KeyError):
        raise ApiServiceError

def _parse_image_id(response_item: dict[str, Any]) -> str:
    return response_item['thumbnails'][0]['url'].split('/')[-1]
