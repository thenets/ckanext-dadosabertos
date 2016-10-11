import ckan.plugins as p
import ckan.lib.helpers as helpers
from ckan.lib.base import c, model, request, render, h, g
from pylons import config

# DEBUG
from var_dump     import var_dump
from pprint     import pprint



class NoticiasController(p.toolkit.BaseController):
    controller = 'ckanext.noticias.controller:NoticiasController'

    def index (post):
    	#pprint(dir(post))
    	c.post = post;
        return render('noticias/index.html')