#
# Collective Knowledge (index of CK modules)
#
# 
# 
#
# Developer: 
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# add index

def add_index(i):
    """
    Input:  {
              dict - index dict
              meta - original CK entry meta
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import copy

    d=i['dict']
    m=i['meta']

    repo_url1_full=d['misc'].get('repo_url1','')

    data_uoa=d['misc'].get('data_uoa','')
    data_uid=d['misc'].get('data_uid','')

    module_uoa=d['misc'].get('module_uoa','')
    module_uid=d['misc'].get('module_uid','')

    xworkflow=m.get('workflow','')
    workflow=m.get('workflow_type','')
    if xworkflow=='yes' and workflow=='':
       workflow='yes'

    d['misc']['workflow']=workflow
    d['misc']['actions']={}

    actions=m.get('actions',{})

    if len(actions)>0:
       for q in sorted(actions):

           qq=actions[q]

           d['misc']['actions'][q]={}

           if repo_url1_full!='':
              # Get API!
              l=-1
              rx=ck.get_api({'module_uoa':data_uid, 'func':q})
              if rx['return']==0:
                 l=rx['line']

              if l!=-1:
                 d['misc']['actions'][q]['url_api']=repo_url1_full+'#L'+str(l)

    return {'return':0}

##############################################################################
# generate html

def html(i):
    """
    Input:  {
              (skip_cid_predix) - if 'yes', skip "?cid=" prefix when creating URLs
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    d=i.get('dict',{})

    scp=i.get('skip_cid_prefix','')
    bscp=(scp=="yes")

    llm=d.get('meta',{})

    llmisc=llm.get('misc',{})
    lldict=llm.get('dict',{})

    workflow=llmisc.get('workflow','')

    repo_url1=llmisc.get('repo_url1','')
    repo_url2=llmisc.get('repo_url2','')

    desc=lldict.get('desc','')

    duoa=llmisc.get('data_uoa','')
    duid=llmisc.get('data_uid','')

    ruoa=llmisc.get('repo_uoa','')
    ruid=llmisc.get('repo_uid','')

    muoa=llmisc.get('module_uoa','')

    h=''
    if desc!='':
       h+='<i> - '+desc+'</i>\n'

    actions1=lldict.get('actions',{})
    actions2=llmisc.get('actions',{})

    h+='<div style="background-color:#efefef;margin:5px;padding:5px;">\n'

    url0=i.get('url','')
    x1=''
    x2=''
    if url0!='' and ruid!='':
       prfx=''
       if not bscp: prfx='cid='
       x1='<a href="'+url0+prfx+cfg['module_deps']['component.repo']+':'+ruid+'" target="_blank">'
       x2='</a>'
    h+='<b>Repo name:</b> '+x1+ruoa+x2+'<br>\n'

    if workflow!='':
       h+='<b>Workflow:</b> '+workflow+'<br>\n'

    to_get=llmisc.get('to_get','')
    if to_get!='':
       h+='<b>How to get:</b> <span style="color:#2f0000">'+to_get+'</span><br>\n'

    if len(actions1)>0:
       h+='<b>Actions:</b><br>\n'
       h+='<div style="margin-left:20px;">\n'
       h+=' <ul>\n'
       for a in actions1:
           x=actions1[a]
           ad=x.get('desc','')
           y=actions2.get(a,{})
           au=y.get('url_api','')

           h+='  <li><span style="color:#2f0000;">ck <i>'+str(a)+'</i> '+duoa+'</span> - '+ad
           if au!='':
              h+=' [<a href="'+au+'"><b><span style="color:#2f0000;">API</span></b></a>]\n'

       h+=' </ul>\n'
       h+='</div>\n'
    h+='</div>\n'

    h1=''

    if repo_url1!='':
       h1+='[&nbsp;<a href="'+repo_url1+'" target="_blank">code</a>&nbsp;] \n'
    if repo_url2!='':
       h1+='[&nbsp;<a href="'+repo_url2+'" target="_blank">meta</a>&nbsp;]\n'

    return {'return':0, 'html':h, 'html1':h1}

##############################################################################
# index components

def index(i):
    """
    Input:  {
              (data_uoa) - specific component to index (otherwise check all)
              (share)    - if 'yes', add to Git
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    # Clean input to pass to component
    for k in ['cids', 'cid', 'xcids']:
        if k in i: del(i[k])

    duoa=i.get('data_uoa','')

    i['module_uoa']=cfg['module_deps']['component']
    i['data_uoa']=work['self_module_uid']
    i['component_uoa']=duoa

    return ck.access(i)

##############################################################################
# find specific components

def get(i):
    """
    Input:  {
              (data_uoa)      - if not UID, search for specific UOA inside dicts
              (s) or (string) - search string
              (all)           - if 'yes', show repo and path
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    # Clean input to pass to component
    for k in ['cids', 'cid', 'xcids']:
        if k in i: del(i[k])

    duoa=i.get('data_uoa','')

    i['action']='get_from_cmd'
    i['module_uoa']=cfg['module_deps']['component']
    i['data_uoa']=work['self_module_uid']
    i['component_uoa']=duoa

    return ck.access(i)
