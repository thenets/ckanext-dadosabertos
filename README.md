# CKANext DadosAbertos


## Requisitos

- Instalação limpa do Ubuntu 14.04
- Nenhum serviço trabalhando nas portas: 8080, 8888, 8800, 80, 5000
- Não ter o Apache2 e o NGINX previamente instalado


## Instalação

### 1. Instale o CKAN

  Foi utilizado um script para automatizar a instalação, que pode ser encontrado em https://github.com/thenets/Easy-CKAN .
  Instale também o DataStore e Harvest, que serão exibidos durante o processo de instalação
  
\# | Command
--- | ---
1 | `sudo su -c "apt-get update && apt-get upgrade -y"`
2 | `sudo su -c "apt-get install git-core"`
3 | `sudo su -c "cd /tmp && rm -rf ./Easy-CKAN && git clone https://github.com/thenets/Easy-CKAN.git && cd ./Easy-CKAN && ./easy_ckan.sh"`
4 | `sudo su -c "easyckan install"`


### 2. Instale o plugin CKANext Pages
  
  Este plugin é utilizado para controlar as páginas estáticas do portal.

\# | Command
--- | ---
1 | `su -s /bin/bash - ckan -c ". /usr/lib/ckan/default/bin/activate && pip install -e git+https://github.com/ckan/ckanext-pages.git#egg=ckanext-pages"`
2 | `sed -i 's/pages/ /g' /etc/ckan/default/development.ini # FIX DUPLICATE ON SECOND INSTALLATION`
3 | ` sed -i 's/ckan.plugins = /ckan.plugins = pages /g' /etc/ckan/default/development.ini`
4 | `sed -i "s/## Plugins Settings/## Plugins Settings\n\n# Pages plugin\nckanext.pages.allow_html = True\nckanext.pages.editor = ckeditor\n/g" /etc/ckan/default/development.in`

### 3. Instale o plugin CKANext DadosAbertos

\# | Command
--- | ---
1 |  `su -s /bin/bash - ckan -c ". /usr/lib/ckan/default/bin/activate && pip install -e git+https://github.com/ckan/ckanext-pages.git#egg=ckanext-pages"`
2 | `su -s /bin/bash - ckan -c ". /usr/lib/ckan/default/bin/activate && pip install -r /usr/lib/ckan/default/src/ckanext-dadosabertos/pip-requirements.txt"`
3 | `sed -i 's/dadosabertos/ /g' /etc/ckan/default/development.ini`
4 | `sed -i 's/stats text_view image_view recline_view/stats text_view image_view recline_view dadosabertos /g' /etc/ckan/default/development.ini`
5 | `su -s /bin/bash - ckan -c ". /usr/lib/ckan/default/bin/activate && cd /usr/lib/ckan/default/src/ckanext-dadosabertos && python setup.py develop"`

### 4. Inicie o servidor

\# | Desenvolvimento (porta: 5000)
--- | ---
1 | `sudo easyckan server`

\# | Produção (porta: 80)
--- | ---
1 | `sudo easyckan deploy`


## Configuração adicional

Para o recurso do WordPress funcionar, é necessário instalar nele o plugin: [WordPress REST API](https://br.wordpress.org/plugins/rest-api/)
Depois de instalado, será necessário alterar o domínio do site em WordPress:

**Arquivo:**
`/usr/lib/ckan/default/src/ckanext-dadosabertos/ckanext/dadosabertos/plugin.py`

    # Altere o método "def wordpress_posts" para a URL do WordPress desejada:
    url = "http://SEU_WORDPRESS_AQUI/ ...


