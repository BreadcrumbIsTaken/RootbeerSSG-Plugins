from rootbeer.signals import after_render_index
from rootbeer.utils import rb_create_path_if_does_not_exist

@after_render_index.connect
def rb_render_blog_page_index(sender) -> None:
    template = sender.env.get_template('blog.html')
    rb_create_path_if_does_not_exist(f'{sender.out_dir}/{sender.blog_dir}')
    with open(f'{sender.out_dir}/{sender.blog_dir}/index.html', 'w', encoding='utf-8') as blog_index:

        blog_index.write(
            template.render(
                posts=sender.posts,
                config=sender.config,
                rootbeer=sender,
            )
        )