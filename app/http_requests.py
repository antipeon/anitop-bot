import requests

MAX_PER_PAGE = 50

def GetData(shows_number):
    """GetData(shows_number) -> list[obj.json]"""

    # query
    query = '''
    query GetTop($sort: [MediaSort], $page: Int, $perPage: Int) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media(sort: $sort) {
                    title {
                        english
                        romaji
                    }
                    coverImage {
                        extraLarge
                    }
            }
        }
    }
    '''

    # query variables
    variables = {
        'sort': 'POPULARITY_DESC',
        'page': 1,
        'perPage': shows_number
    }

    url = 'https://graphql.anilist.co'

    # HTTP Api request
    total_full_pages = shows_number // MAX_PER_PAGE
    last_page_left = shows_number % MAX_PER_PAGE
    variables['perPage'] = min(MAX_PER_PAGE, shows_number)
    responses = list()

    for i in range(total_full_pages):
        responses.append(requests.post(url, 
            json={'query': query, 'variables': variables}).json())
        variables['page'] += 1

    if last_page_left > 0:
        last_el = requests.post(url, 
            json={'query': query, 'variables': variables}).json()
        items = last_el['data']['Page']['media']
        del items[last_page_left:len(items)]
        last_el['data']['Page']['media'] = items
        responses.append(last_el)
    
    return responses


cover_size = 'extraLarge'


def ParseData(data_list):
    """ParseData(data_list) -> messages"""
    messages = list()
    for data in data_list:
        items = data['data']['Page']['media']
        for item in items:
            messages.append([item['title']['english'], item['title']['romaji'],
                            item['coverImage'][cover_size]])
    return messages
