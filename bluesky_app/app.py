from flask import Flask, render_template
from atproto import Client
from datetime import datetime, timezone

app = Flask(__name__)

# Liste des comptes Bluesky à surveiller
accounts = ['nighdruth.bsky.social', 'parttimeyeen.bsky.social']

def parse_time(time_str):
    date_format = '%Y-%m-%dT%H:%M:%S'
    time_str_trim = time_str[:-5]
    post_time = datetime.strptime(time_str_trim, date_format).replace(tzinfo=timezone.utc)
    return post_time

def get_posts(account):
    client = Client()
    client.login('tommylrt.bsky.social', 'yApasPjC/#tMDP1,')
    try:
        # Paramètres pour récupérer 50 posts avec réponses, sans médias
        data = client.get_author_feed(
            actor=account,
            limit=50,  # Nombre de posts à récupérer
            filter="posts_with_replies",  # Par exemple, incluant les réponses
            includePins=True  # Inclure les posts épinglés
        ).feed
        print(f"Posts récupérés pour {account}: {data}")
        posts = []
        for event in data:
            post = event.post
            print(f"Post : {post}")
            if hasattr(post.record, 'created_at'):
                post_time = parse_time(post.record.created_at)
                posts.append({'post': post, 'post_time': post_time})
            else:
                print("⚠️ Pas de created_at trouvé pour ce post !")
        return posts
    except Exception as e:
        print(f"Erreur pour le compte {account}: {e}")
        return []


@app.route('/')
def index():
    all_posts = []
    for account in accounts:
        posts = get_posts(account)
        all_posts.extend(posts)
    
    # Trie les posts par date décroissante
    all_posts.sort(key=lambda x: x['post_time'], reverse=True)
    return render_template('index.html', posts=all_posts)

if __name__ == '__main__':
    app.run(debug=True)
