import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.base import c, g, h, model

# Dependence for Wordpress_Post
import requests, json, BeautifulSoup 
from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer
from ckan.plugins import IRoutes


# ============================================
# Get the most popular groups
# ============================================
def most_popular_groups():
    # '''Return a sorted list of the groups with the most datasets.'''

    # Get a list of all the site's groups from CKAN, sorted by number of
    # datasets.
    groups = toolkit.get_action('group_list')(
        data_dict={'sort': 'package_count desc', 'all_fields': True})

    # Truncate the list to the 10 most popular groups only.
    groups = groups[:10]

    return groups




# ============================================
# Get most recent datasets (NOT WORKING)
# ============================================
def most_recent_datasets():
        """Sets the c.most_recent_datasets variable for a template to render.
        """
        import ckan.lib.dictization as d
        from ckan.logic import get_action
        from sqlalchemy import desc

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}
  
        #model = context['model']
        query = model.Session.query(model.Package, model.Activity)
        query = query.filter(model.Activity.object_id==model.Package.id)
        query = query.filter(model.Activity.activity_type == 'new package')
        query = query.filter(model.Package.state == 'active')
        query = query.order_by(desc(model.Activity.timestamp))
        query = query.limit(5)
        most_recent_from_bd = query.all()

        #Query:
        #select act.activity_type, act.timestamp, pck.name
        #from activity act
        #join package pck on pck.id = act.object_id
        #where act.activity_type = 'new package' and pck.state = 'active' order by act.timestamp desc;
        
        #Trace of how i got to the final line =p
        #model_dictize.package_dictize
        #obj_list_dictize
        #recent_dict = model_dictize.package_dictize(most_recent_from_bd, context)

        most_recent_datasets = [
            (
                g.site_url + '/dataset/' + dataset.name,
                #cls.limita_tamanho(dataset.title, 46),
                dataset.title,
                #cls.limita_tamanho(dataset.author, 28),
                dataset.author,
                #cls.tempo_atras(activity.timestamp),
                activity.timestamp.isoformat(),
            )   for dataset, activity in most_recent_from_bd]

        most_recent_datasets = []
        for dataset, activity in most_recent_from_bd:
            dataset.link = 'dataset/' + dataset.name
            dataset.time = activity.timestamp.strftime("%d/%m/%Y")
            most_recent_datasets.append(dataset)


        return most_recent_datasets




# ============================================
# Get News from Wordpress
# ============================================
def wordpress_posts(type_content="", custom=10):
    # Get all posts
    if (type_content == "all"):
        url = "http://dadosabertos.thenets.org/wp-json/wp/v2/posts?per_page="+str(custom)
        posts = requests.get(url).json()
        return (posts)

    # Get single post
    if "noticias" in h.full_current_url():
        items_url = h.full_current_url().split('/')
        items_url.pop() # remove slug
        post_id = items_url.pop() # get post id
        url = "http://dadosabertos.thenets.org/wp-json/wp/v2/posts/"+str(post_id)
        r = requests.get(url)
        print (url)
        return (r.json())
    pass



# ============================================
# Get Pages from Wordpress
# ============================================
def wordpress_pages(type_content="", custom=10):
    # Get single post
    if "paginas" in h.full_current_url():
        items_url = h.full_current_url().split('/')
        page_slug = items_url.pop() # get page slug
        url = "http://dadosabertos.thenets.org/wp-json/wp/v2/pages?filter[name]="+str(page_slug)+"&_embed"
        r = requests.get(url)
        return (r.json()[0])
    pass



 



 

 
# ============================================
# Main plugin class
# ============================================
class DadosabertosPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    implements(IConfigurer, inherit=True)
    implements(IRoutes, inherit=True)


    # Declare that this plugin will implement ITemplateHelpers.
    plugins.implements(plugins.ITemplateHelpers)
    
    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'dadosabertos')

    def after_map(self, map):
        map.connect('/noticias/{id}/{slug}',
                    controller='ckanext.dadosabertos.controller:NoticiasController',
                    action='index',
                    id=0)

        map.connect('/paginas/{slug}',
                    controller='ckanext.dadosabertos.controller:PaginasController',
                    action='index')
        return map



    def get_helpers(self):
        '''Register all functions

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {'dadosabertos_most_popular_groups': most_popular_groups,
            'dadosabertos_most_recent_datasets': most_recent_datasets,
            'dadosabertos_wordpress_posts': wordpress_posts,
            'dadosabertos_wordpress_pages': wordpress_pages,
            'dadosabertos_BeautifulSoup': BeautifulSoup.BeautifulSoup }