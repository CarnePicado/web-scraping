from ws import *

if __name__ == '__main__':
    for page in range(0,6):
        if page == 0:
            res = get_text(articles)
            res = find_articles(res)
            res = parser(res)
            with open('vacancy.json', 'w', encoding='utf-8') as f:
                json.dump(res, f, ensure_ascii=False)
        else:
            res = get_text(f'{articles}&page={page}')
            res = find_articles(res)
            res = parser(res)
            with open('vacancy.json', 'a', encoding='utf-8') as f:
                json.dump(res, f, ensure_ascii=False)