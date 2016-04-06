
# coding: utf-8

# ## Title: Using the Google API to get University Addresses
# ### Author: Meenakshi Parameshwaran
# ### Date: 05/04/16

# Note that this assigment was written in Python 3.4
# 
# University UKPRN-Name lookup from here: https://www.google.co.uk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=0ahUKEwiAzLveqPjLAhVDgg8KHYx1Dj4QFgghMAE&url=https%3A%2F%2Fwww.hesa.ac.uk%2Fdox%2Funistats%2FUNISTATS_UKPRN_lookup_20141030.xls&usg=AFQjCNG1-YuYokBm7hPDea_vo9ua3-g0pg&sig2=mY5ezIiwILVyfvLPkUrANQ&bvm=bv.118443451,d.ZWU

# In[1]:

import csv, pandas, urllib, json, os


# In[2]:

os.getcwd()


# In[3]:

os.listdir()


# In[4]:

unis = pandas.read_csv('unilookup.csv')


# In[5]:

unis.head(n=10)


# In[6]:

repl = " UK"
unis['longname'] = unis['NAME'] + repl


# In[7]:

smallunis = unis[0:10]


# In[8]:

print(smallunis)
type(smallunis)


# In[9]:

serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'


# In[10]:

uni_name = []
formatted_address = []
long_name = []
short_name = []
first_type = []
second_type = []


# In[11]:

for a in unis['longname']:
    address = a
    if len(address) < 1 : break

    url = serviceurl + urllib.parse.urlencode({'sensor':'false', 'address': address})
    print ('Retrieving', url)

    urlopened = urllib.request.urlopen(url) 

    # need to decode it for Python 3
    mydata = urlopened.readall().decode('utf-8')

    print ('Retrieved',len(mydata),'characters')

    try: jsoutput = json.loads(str(mydata))
    except: jsoutput = None
    if 'status' not in jsoutput or jsoutput['status'] != 'OK':
        print ('==== Failure To Retrieve ====')
        print (mydata)
        continue
    
#     print (json.dumps(jsoutput, indent=4))
    
    for result in jsoutput['results']:
        n = 0
        for component in result['address_components']:
            uni_name.append(address)
            formatted_address.append(result['formatted_address'])
            long_name.append(result['address_components'][n]['long_name'])
            short_name.append(result['address_components'][n]['short_name'])
            first_type.append(result['address_components'][n]['types'][0])
            try: second_type.append(result['address_components'][n]['types'][1])
            except: second_type.append("None")
            n = n + 1


#     for component in jsoutput['results'][0]['address_components']:
#         if component['types'] == "postal_code":
#             long_name.append(component['long_name'])
#             short_name.append(component['short_name'])
#             types.append(component['types'])

#     formatted_address.append(jsoutput['results'][0]['formatted_address'])
#     formatted_address.append(jsoutput['results'][0]['partial_match'])


# In[12]:

newdf = pandas.DataFrame([uni_name,formatted_address, long_name,short_name,first_type,second_type]).T


# In[13]:

newdf.columns = ['uni_name','formatted_address', 'long_name','short_name','first_type','second_type']


# In[14]:

newdf


# In[15]:

postcodes = newdf[newdf['first_type'] == "postal_code" ]


# In[16]:

newdf["first_type"].describe()


# In[33]:

postcodes = newdf[newdf['first_type'] == "postal_code" ]


# In[34]:

postcodes.describe()


# In[102]:

postcodes_new = postcodes[['uni_name', 'formatted_address', 'long_name']]


# In[103]:

postcodes_new.columns = ['uni_name', 'full_address', 'postcode']


# In[104]:

# postcodes_new


# In[105]:

import re


# In[107]:

postcodes_new['uni_name_fixed'] = postcodes_new['uni_name'].map(lambda x: x.rstrip('[,]\sUK'))


# In[108]:

postcodes_new['uni_name_fixed'] = postcodes_new['uni_name_fixed'].map(lambda x: x.rstrip(','))


# In[109]:

postcodes_new


# In[88]:

postcodes_final = postcodes_new[['uni_name_fixed', 'full_address', 'postcode']]


# In[89]:

postcodes_final


# In[63]:

postcodes_final.to_csv('postcodes_final.csv')


# In[64]:

os.listdir()

