from __future__ import print_function
from bs4 import BeautifulSoup
import re

template_file = open("/tmp/rest_template.py", "wb")
print('import re', file=template_file)
print('import json',file=template_file)
print('server_url = ' + '\'http://www.commusoft4.co.uk/webservice_dev.php\'', file=template_file)
print('token_key = ' + '\'IVC-Bz_FHcb8TsY9raQdIUFm-B16Up3czJxS5IYXG3N6QeHN9XQtLWOOvm6bsoFbtufj_8MqmKb92z0V5yyeqw\'', file=template_file)

print("""class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
""", file=template_file)

print('', file=template_file)

print("""class BaseObjects:
    pass
""", file=template_file)

print("""class BaseCRUDObjects(BaseObjects):
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

""", file=template_file)
filelocation = '/media/harish/storage/code/python/regex/APIdoc.html'
filecontent = open(filelocation)
soup = BeautifulSoup(filecontent)

for div in soup.find_all("div", { "id" : "section" }):
    t = div.h1.string
    base_class_name = t.replace(" ", "")
    #print "base class is :" + base_class_name

    for li in div.find_all("li"):
        for h2 in li.find_all("h2"):
            #print h2.string
            path = h2.string
            title_additional_params = re.findall('\{([A-Za-z0-9]+)\}', h2.string)
            if title_additional_params:
                for additional_param in title_additional_params :
                    if 'By' in base_class_name:
                        base_class_name = base_class_name + 'And' + additional_param.title() ;

                    else :
                        base_class_name = base_class_name + 'By' + additional_param.title() ;

            #print "class name is : " + base_class_name
            print('',file=template_file )
            print('class ' + base_class_name + '(BaseCRUDObjects):' , file=template_file)
            print('    ' + 'url' + ' = ' + '\'' + path + '\'', file=template_file)
            for form in li.find_all('form'):
                rest_endpoint = form.get('action')
                method_name = form.get('method')
                function_name = ''
                array_name = ''
                param_list = []
                i = 0
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
                                    #print "method name or class name " + method_name.lower() +  title_search.group(1).title()+'s'
                                    array_name = title_search.group(1)
                                    #function_name = method_name.lower() +  title_search.group(1).title()
                                    function_name = title_search.group(1).title()
                    title_additional_params = re.findall('\{([A-Za-z0-9]+)\}',rest_endpoint )
                    if title_additional_params:
                        for additional_param in title_additional_params :
                            if 'By' in function_name:
                                function_name = function_name + 'And' + additional_param.title() ;
                            else :
                                function_name = function_name + 'By' + additional_param.title() ;

                    #print
                    #print 'class ' + method_name.title() +  function_name + ':'
                    #print '    ' + array_name + ' = AutoVivification()'
                    #print '    ' + 'url' + ' = ' + '\'' + rest_endpoint + '\''
                    #for param in param_list:
                    #    print '    ' + param + ' = \'\''

                    #print 'class ' + base_class_name + ':'
                    print('    ' + 'def ' + method_name.lower() + 'Params' + '(self, document):', file=template_file)
                    #print('    ' + '    ' + 'url' + ' = ' + '\'' + path + '\'', file=template_file)
                    #refactor thr following
                    if (method_name.lower() == "put" or method_name.lower() == "post" ):
                        print('    ' + '    ' + array_name + ' = AutoVivification()', file=template_file)

                    if (method_name.lower() == "put" or method_name.lower() == "post" or method_name.lower() == "delete"):
                        for param in param_list:
                            keys = re.search('(\[.*\])',param , re.IGNORECASE)
                            if keys:
                                #print('    ' + '    ' + param + ' = \'\'', file=template_file
                                print('    ' + '    ' + param + ' = document'  + keys.group(1).replace("description", "descriptionText") , file=template_file)
                            else :
                                #check if descriptionText replacement is unncessecary
                                print('    ' + '    ' + param + ' = document[\''  + param.replace("description", "descriptionText") + '\']' , file=template_file)
                    if (method_name.lower() == "put" or method_name.lower() == "post"):
                        print('    ' + '    ' + array_name + ' = {\'' + array_name + '\' :' + array_name +'}' , file=template_file  )
                    if (method_name.lower() == "put" or method_name.lower() == "post" or method_name.lower() == "delete"):
                        print("""
        path = self.url
        url_params = re.findall('\{([A-Za-z0-9]+)\}',path)
        if url_params:
            for url_param  in url_params :
                print '{' + url_param + '}'
                path = path.replace('{' + url_param + '}',str(eval(url_param)))
        self.url = path
        """, file=template_file)
                        print('    ' + '    ' + 'return ' + array_name, file=template_file)
                    else :
                        print('    ' + '    ' + 'return', file=template_file)
                    print('',file=template_file )

            base_class_name = t.replace(" ", "") # resetting base class name to give place for next fresh h2
