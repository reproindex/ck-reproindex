#
# Collective Knowledge (index of CK soft detection plugins)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin
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

    dd=d.get('dict',{})

    if 'misc' not in d: d['misc']={}
    misc=d['misc']

    repo_url1_full=misc.get('repo_url1','')

    data_uoa=misc.get('data_uoa','')
    data_uid=misc.get('data_uid','')

    module_uoa=misc.get('module_uoa','')
    module_uid=misc.get('module_uid','')

    name=dd.get('soft_name','')
    misc['soft_name']=name

    cus=dd.get('customize',{})

    ad=dd.get('auto_detect','')
    if ad!='yes': ad='no'
    misc['auto_detect']=ad

    ep=cus.get('env_prefix','')
    misc['env_prefix']=ep

    xhos=dd.get('only_for_host_os_tags',[])
    xtos=dd.get('only_for_target_os_tags',[])

    tmpl=dd.get('template','')
    template=dd.get('template_type','')
    if tmpl=='yes' and template=='':
       template='yes'

    misc['template']=template

    tags=dd.get('tags',[])
    ytags=','.join(tags)

    misc['tags']=tags
    misc['stags']=ytags

    yhos=''
    ytos=''

    for q in xhos:
        if yhos!='': yhos+=','
        yhos+=q

    for q in xtos:
        if ytos!='': ytos+=','
        ytos+=q

    if yhos=='':
       yhos='any'
    else:
       yhos=yhos.replace('linux','linux,macos')

    if ytos=='':
       ytos='any'
    else:
       ytos=ytos.replace('linux','linux,macos')

    misc['host_os']=yhos
    misc['target_os']=ytos

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

    template=llmisc.get('template','')

    repo_url1=llmisc.get('repo_url1','')
    repo_url2=llmisc.get('repo_url2','')
    repo_url3=llmisc.get('repo_url3','')

    desc=lldict.get('soft_name','')

    duoa=llmisc.get('data_uoa','')
    duid=llmisc.get('data_uid','')

    ruoa=llmisc.get('repo_uoa','')
    ruid=llmisc.get('repo_uid','')

    muoa=llmisc.get('module_uoa','')

    ad=llmisc.get('auto_detect','')
    ep=llmisc.get('env_prefix','')

    h=''
    if desc!='':
       h+='<i> - '+desc+'</i>\n'

    host_os=llmisc.get('host_os','')
    target_os=llmisc.get('target_os','')

    stags=llmisc.get('stags','').replace(',',', ')

    h=''
    if desc!='':
       h+='<i> - '+desc+'</i>\n'

    run_cmds=lldict.get('run_cmds',{})

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

    to_get=llmisc.get('to_get','')
    if to_get!='':
       h+='<b>How to get:</b> <span style="color:#2f0000">'+to_get+'</span><br>\n'

    if template!='':
       h+='<b>Template:</b> '+template+'<br>\n'

    h+='<b>Auto detection:</b> '+ad+'<br>\n'

    h+='<b>Environment var: </b> '+ep+'<br>\n'

    h+='<b>Host&nbsp;OS:</b> '+host_os+'<br>\n'

    h+='<b>Target&nbsp;OS:</b> '+target_os+'<br>\n'

    h+='<b>Tags:</b> '+stags+'<br>\n'

    h+='</div>\n'

    h1=''

    if repo_url3!='':
       h1+='[&nbsp;<a href="'+repo_url3+'" target="_blank">detection plugin</a>&nbsp;] \n'
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
