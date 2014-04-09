from __future__ import print_function
from bs4 import BeautifulSoup
import re

template_file = open("/tmp/rest_template.py", "wb")

print("""import re
import json
server_url = 'http://www.commusoft4.co.uk/webservice_dev.php'
token_key = 'IVC-Bz_FHcb8TsY9raQdIUFm-B16Up3czJxS5IYXG3N6QeHN9XQtLWOOvm6bsoFbtufj_8MqmKb92z0V5yyeqw'

class AutoVivification(dict):
    def __missing__(self, missingkey):
        self[missingkey] = type(self)()
        return self[missingkey]

class BaseObjects:
    pass

class BaseCRUDObjects(BaseObjects):
    def get(self, document):
        import requests

        pass

    def post(self, document):
        import requests
        jsondoc = self.postParams(document)
        response = requests.post("%s?token=%s" %(server_url + self.url, token_key), data=json.dumps(jsondoc))
        return response

    def put(self, document):
        import requests
        jsondoc = self.putParams(document)
        response = requests.put("%s?token=%s" %(server_url + self.url, token_key), data=json.dumps(jsondoc))
        return response


    def delete(self, document):
        import requests
        self.deleteParams(document)
        response = requests.delete("%s?token=%s" %(server_url + self.url, token_key))
        return response

    def getlist(self, document):
        import requests

        pass

    def postlist(self, document):
        import requests
        jsondoc = self.postParams_list(document)
        response = requests.post("%s?token=%s" %(server_url + self.url, token_key), data=json.dumps(jsondoc))
        return response

    def putlist(self, document):
        import requests
        jsondoc = self.putParams_list(document)
        response = requests.put("%s?token=%s" %(server_url + self.url, token_key), data=json.dumps(jsondoc))
        return response


    def deletelist(self, document):
        import requests
        self.deleteParams_list(document)
        response = requests.delete("%s?token=%s" %(server_url + self.url, token_key))
        return response
""", file=template_file)

soup = BeautifulSoup(open('/media/harish/storage/code/python/regex/APIdoc.html'))

for div in soup.find_all("div", { "id" : "section" }):
    t = div.h1.string
    base_class_name = t.replace(" ", "")
    print('',file=template_file )
    print('class ' + base_class_name + '(BaseCRUDObjects):' , file=template_file)
    """
    for li in div.find_all("li"):
        for h2 in li.find_all("h2"):
            #print h2.string
            path = h2.string
            title_additional_params = re.findall('\{([A-Za-z0-9]+)\}$', h2.string)
            if title_additional_params:
                for additional_param in title_additional_params :
                    if 'By' in base_class_name:
                        base_class_name = base_class_name + 'And' + additional_param.title() ;

                    else :
                        base_class_name = base_class_name + 'By' + additional_param.title() ;


            print('',file=template_file )
            print('class ' + base_class_name + '(BaseCRUDObjects):' , file=template_file)

            print('    ' + 'url' + ' = ' + '\'' + path + '\'', file=template_file)
    """
    for form in div.find_all('form'):
        rest_endpoint = (re.search("\/api\/.*",form.get('action'))).group()
        method_name = form.get('method')
        function_name = ''
        array_name = ''
        param_list = []
        i = 0
        title_additional_params = re.findall('\{([A-Za-z0-9]+)\}$', rest_endpoint)
        if title_additional_params:
            print('    ' + 'def ' + method_name.lower() + 'Params' + '(self, document):', file=template_file)
        else :
            print('    ' + 'def ' + method_name.lower() + 'Params' + '_list' + '(self, document):', file=template_file)
        print ('        ' + 'url' + ' = ' + '\'' + rest_endpoint + '\'', file=template_file)
        if ((form.get('method') == 'POST' or form.get('method') == 'PUT' or form.get('method') == 'GET' or form.get('method') == 'DELETE')):
            for fieldset in form.find_all("fieldset", { "class" : "parameters" }):
                for input in fieldset.find_all("input", { "class" : "key" }):
                    #print input.get('value')
                    #if '[' in input.get('value'):
                    if '[' in input.get('value'):
                        temp = []
                        temp_param = input.get('value')
                        brackets = re.findall('\[([A-Za-z0-9_]+)\]',input.get('value') )
                        for bracket in brackets:
                            #print bracket\{([A-Za-z0-9]+)\}
                            temp.append(bracket)
                        for a in temp:
                            if not a.isdigit():
                                temp_param = re.sub('\[' + a + '\]' , '[\'' + a + '\']', temp_param)


                        param_list.append(temp_param)
                    else :
                        param_list.append(input.get('value'))

                    if i == 0:
                        title_search = re.search('([A-Za-z0-9]+)\[',input.get('value') , re.IGNORECASE)
                        if title_search :
                            i = 1;
                            array_name = title_search.group(1)
                            function_name = title_search.group(1).title()
            title_additional_params = re.findall('\{([A-Za-z0-9]+)\}',rest_endpoint )
            if title_additional_params:
                for additional_param in title_additional_params :
                    if 'By' in function_name:
                        function_name = function_name + 'And' + additional_param.title() ;
                    else :
                        function_name = function_name + 'By' + additional_param.title() ;
            """
            print('    ' + 'def ' + method_name.lower() + 'Params' + '(self, document):', file=template_file)
            """
            #refactor the following
            if (method_name.lower() == "put" or method_name.lower() == "post" ):
                print('    ' + '    ' + array_name + ' = AutoVivification()', file=template_file)

            if (method_name.lower() == "put" or method_name.lower() == "post" or method_name.lower() == "delete"):
                for param in param_list:
                    keys = re.search('(\[.*\])',param , re.IGNORECASE)
                    if keys:
                        print('    ' + '    ' + param + ' = document'  + keys.group(1).replace("description", "descriptionText") , file=template_file)
                    else :
                        #check if descriptionText replacement is unncessecary
                        print('    ' + '    ' + param + ' = document[\''  + param.replace("description", "descriptionText") + '\']' , file=template_file)
            if (method_name.lower() == "put" or method_name.lower() == "post"):
                print('    ' + '    ' + array_name + ' = {\'' + array_name + '\' :' + array_name +'}' , file=template_file  )
            if (method_name.lower() == "put" or method_name.lower() == "post" or method_name.lower() == "delete"):
                #change the following to a global function
                print("""
        path = url
        url_params = re.findall('\{([A-Za-z0-9]+)\}',path)
        if url_params:
            for url_param  in url_params :
                path = path.replace('{' + url_param + '}',str(eval(url_param)))
        self.url = path
""", file=template_file)
                print('    ' + '    ' + 'return ' + array_name, file=template_file)
            else :
                print('    ' + '    ' + 'return', file=template_file)
            print('',file=template_file )

    base_class_name = t.replace(" ", "") # resetting base class name to give place for next fresh h2
