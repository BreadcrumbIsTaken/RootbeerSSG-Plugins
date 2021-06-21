from rootbeer.signals import after_render_archive
from rootbeer.utils import rb_create_and_or_clean_path
from slug import slug

@after_render_archive.connect
def rb_render_tag_index(sender):
    
    rb_create_and_or_clean_path(f'{sender.out_dir}/tags')
        
    list_of_tags = []
    for i in range(len(sender.posts)):
        if 'tags' in sender.posts[i]['metadata']:
            for tag in sender.posts[i]['metadata']['tags']:
                if tag not in list_of_tags:
                    tags_dict = {}
                    tags_dict['name'] = tag
                    tags_dict['slug'] = slug(tag)
                    tags_dict['url'] = f'tags/{tags_dict["slug"]}'
                list_of_tags.append(tags_dict)
    # Tags
    tag_template = sender.env.get_template('tags.html')
    with open(f'{sender.out_dir}/tags/index.html', 'w', encoding='utf-8') as file:
        file.write(
            tag_template.render(
                config=sender.config, 
                content=sender.content, 
                tags=list_of_tags, 
                rootbeer=sender
                )
            )

@after_render_archive.connect
def rb_render_tags(sender):
    post_with_the_tag = {}
    for i in range(len(sender.posts)):
        for tag in sender.posts[i]['metadata']['tags']:
            if tag in post_with_the_tag.keys():      #Checking if the tags are already in the dict
                post_with_the_tag[tag].append(sender.posts[i])
            else:    #Adding the remaining to the dict
                post_with_the_tag[tag] = [sender.posts[i]]
                
    tag_page_template = sender.env.get_template('tag.html')
    for tag in post_with_the_tag.keys():
        rb_create_and_or_clean_path(f'{sender.out_dir}/tags/{slug(tag)}/')
        with open(f'{sender.out_dir}/tags/{slug(tag)}/index.html', 'w', encoding='utf-8') as file:
            file.write(
                tag_page_template.render(
                    config=sender.config, 
                    content=sender.content, 
                    tags=post_with_the_tag[tag],
                    tag=tag,
                    rootbeer=sender
                    )
                )