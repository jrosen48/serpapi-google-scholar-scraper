from serpapi import GoogleSearch

import time

import pandas as pd

# import urllib library
from urllib.request import urlopen

# import json
import json

all_articles = pd.read_csv("<add-input-file-path-with-journal-titles-journal-names-and-years-here>")
all_articles['unique_row_id'] = all_articles['index']
all_articles = all_articles.loc[1501:3054]
all_articles

df = pd.DataFrame()

for my_index in all_articles.index:
  
    time.sleep(2.5)
  
    print('working on accessing: ' + str(my_index))
  
    article_name = all_articles[all_articles.index == my_index]['name_of_article'][my_index]
    journal_name = all_articles[all_articles.index == my_index]['name_of_journal'][my_index]
    year = all_articles[all_articles.index == my_index]['year'][my_index]
    unique_row_id = all_articles[all_articles.index == my_index]['unique_row_id'][my_index]
    
    params = {
      "api_key": "<add API key from serpAPI here>",
      "device": "desktop",
      "engine": "google_scholar",
      "q": article_name,
      "hl": "en"
    }
    
    try:
      
      search = GoogleSearch(params)
      results = search.get_dict()

      tmp = pd.json_normalize(results['organic_results'][0]['resources'])
      tmp['unique_row_id'] = unique_row_id
      tmp['article_name'] = article_name
      tmp['journal_name'] = journal_name
      tmp['year'] = year
      df = df.append(tmp)


      try:
        
        url = results['organic_results'][0]['inline_links']['versions']['serpapi_scholar_link']
        
        url = url + '&api_key=6353c703629be97190577a805b97fd42f0d5c57577c2ff0d8dec3e3461c82c62'
        
        response = urlopen(url)
        
        data_json = json.loads(response.read())
        
        n_resources = data_json['search_information']['total_results']
        
        print('trying to access: ' + str(n_resources))

        for result in range(0, n_resources):

          tmp = pd.DataFrame()

          # first page
          
          try:
    
            tmp = pd.json_normalize(data_json['organic_results'][result]['resources'])
            tmp['unique_row_id'] = unique_row_id
            tmp['article_name'] = article_name
            tmp['journal_name'] = journal_name
            tmp['year'] = year
            df = df.append(tmp)
                  
          except BaseException as e:
            
            print('ERROR in accessing resources: ' + str(e))

        # second page
        
        try:

          second_url = data_json['serpapi_pagination']['next']
          second_url = second_url + '&api_key=d1f376cfbfcbebe273bf2cf2c3b9399ab5debda248319b9923f19f10809481cc'
          response = urlopen(second_url)
          second_data_json = json.loads(response.read())
          second_n_resources = data_json['search_information']['total_results']
          print('trying to access another: ' + str(second_n_resources))

          for result in range(0, n_resources):

            tmp = pd.DataFrame()

            try:

              tmp = pd.json_normalize(second_data_json['organic_results'][result]['resources'])
              tmp['unique_row_id'] = unique_row_id
              tmp['article_name'] = article_name
              tmp['journal_name'] = journal_name
              tmp['year'] = year
              df = df.append(tmp)

            except BaseException as e:

              print('ERROR in accessing resources on the second page: ' + str(e))

        except BaseException as e:

          print('ERROR: it does not appear a second page exists! ' + str(e))
              
      except BaseException as e:
        
        print('ERROR in accessing article: ' + str(e))

    except BaseException as e:

      print('ERROR in accessing first resource: ' + str(e))


df.to_csv("output-file.csv")
