import json

books = json.load(open('results/04c47b5985b04dddab73ae4d27b244ae.json'))
reviews = json.load(open('results/fcf928c404f94ab495777840dd01b835.json'))
rev = {r['purchase_id']: r for r in reviews}

def author_name(a):
    if not a:
        return 'Unknown'
    try:
        return json.loads(a).get('name', 'Unknown')
    except Exception:
        return a

out = []
for b in books:
    pid = 'purchaseid_' + b['book_id'].split('_')[1]
    assert pid in rev, pid
    det = b['details'] or ''
    english = 'English' in det
    out.append({
        'book_id': b['book_id'],
        'title': b['title'],
        'author': author_name(b['author']),
        'categories': b['categories'],
        'english_mentioned': english,
        'avg_rating': rev[pid]['avg_rating'],
        'num_reviews': rev[pid]['n'],
    })

out.sort(key=lambda x: x['title'])
print(json.dumps(out, indent=2, ensure_ascii=False))
print('Non-English candidates:', [o['title'] for o in out if not o['english_mentioned']])
