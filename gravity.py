import oauthlib, json
import math, time
from requests_oauthlib import OAuth1Session

def getsession(key,secret):
  return OAuth1Session(key, client_secret=secret, signature_type=oauthlib.oauth1.SIGNATURE_TYPE_QUERY)

# https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists
def gen_dict_extract(key, var):
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

#https://stackoverflow.com/questions/5956240/check-if-string-is-a-real-number
def isfloat(str):
    try:
        float(str)
    except ValueError:
        return False
    return True

# by default, Gravity Forms returns a horrendous format that has every field mentioned only by its label number
# you have to separately request the labels and apply them yourself
# naturally, you can't use admin labels on the forms to make this slightly more friendly. They don't come through the API.
# so right now I'm replacing the numeric labels with their freetext labels, which isn't ideal
# I think the field IDs actually stay static even if the labels change, so ideally there would be a mapping of id->computational label
# however that will take a long time, and since the form's format may change, I'll wait until we have somethign stabilized
# ideally I would also isolate those fields that contain duplicated information and make them more friendly
def friendlyjson(entry, labels):
    newdict=dict()
    for key,value in entry.items():
      question=""
      response=""
      if not value:
        continue
      #newdict[key]=value
      #first, look up the question using the key
      if isfloat(key):
        #find the question in the labels table
        label=gen_dict_extract(str(math.floor(float(key))),labels)
        result=next(label)
        #if the label is a dictionary, the question is actually one deeper in label
        if hasattr(result,'items'):
          response=result[key]
          question=next(label)
        else:
          question=result
      else:
        question=key
      if not response or not response==value:
        newdict[question]=value
      else:
        newdict[question]=":".join([response,value])
    return newdict


def get_form_entries(session,baseurl,formno):
  url = "".join([baseurl,"/forms","/",formno,"/entries?_labels=1"])
  r = session.get(url)
  response=r.json()
  entries=response["entries"]
  labels=response["_labels"]
  cleanedup=[]
  for entry in entries:
    cleanedup.append(friendlyjson(entry,labels))
  return cleanedup

# date format: "yyyy-mm-dd" or "yyyy-mm-dd hh:mm:ss"
# https://community.gravityforms.com/t/including-a-date-range-in-v2-rest-api-search-criteria/6953/10
def get_form_entries_created_since(session,baseurl,formno,since):
  url="".join([baseurl,"/forms","/",formno,"/entries?_labels=1&search={\"start_date\":\"",since,"\"}"])
  r = session.get(url)
  response=r.json()
  entries=response["entries"]
  labels=response["_labels"]
  cleanedup=[]
  for entry in entries:
    cleanedup.append(friendlyjson(entry,labels))
  return cleanedup

def get_forms(session,baseurl):
  url = "".join([baseurl,"/forms"])
  r = session.get(url)
  return r.json()

# date format: "yyyy-mm-dd hh:mm:ss"
def get_form_entries_updated_since(session,baseurl,formno,since):
  sincetime=time.strptime(since,"%Y-%m-%d %H:%M:%S")
  entries=get_form_entries(session,baseurl,formno)
  updatedlist=[]
  for entry in entries:
    created=time.strptime(entry['date_created'],"%Y-%m-%d %H:%M:%S")
    updated=time.strptime(entry['date_updated'],"%Y-%m-%d %H:%M:%S")
    if created != updated:
      if updated > sincetime:
        updatedlist.append(entry)
  return updatedlist
