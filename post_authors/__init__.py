from rootbeer.signals import after_render_archive
from rootbeer.utils import rb_create_and_or_clean_path
from slug import slug

@after_render_archive.connect
def rb_post_authors_plugin(sender):
    posts_author_wrote = {}
    for i in range(len(sender.posts)):
        for author in sender.config['authors']:
            if author == sender.posts[i]['metadata']['author']:
                if author in posts_author_wrote.keys():      #Checking if the tags are already in the dict
                    posts_author_wrote[author].append(sender.posts[i])
                else:    #Adding the remaining to the dict
                    posts_author_wrote[author] = [sender.posts[i]]
            else:
                posts_author_wrote[author] = []
    
    # Authors page
    authors_template = sender.env.get_template('authors.html')
    rb_create_and_or_clean_path(f'{sender.out_dir}/authors/')
    with open(f'{sender.out_dir}/authors/index.html', 'w', encoding='utf-8') as file:
        file.write(
            authors_template.render(
                config=sender.config, 
                content=sender.content, 
                authors=sender.config['authors'],
                rootbeer=sender
                )
            )
        
    # Author page
    author_template = sender.env.get_template('author.html')
    for author in sender.config['authors'].keys():
        rb_create_and_or_clean_path(f'{sender.out_dir}/authors/{slug(author)}')
        with open(f'{sender.out_dir}/authors/{slug(author)}/index.html', 'w', encoding='utf-8') as file:
            author_pfp = f'img/author_pfp/author_{author}.png'
            file.write(
                author_template.render(
                    config=sender.config, 
                    content=sender.content, 
                    author_name=author, 
                    pfp=author_pfp, 
                    posts=posts_author_wrote[author], 
                    author=sender.config['authors'][author],
                    rootbeer=sender
                    )
                )