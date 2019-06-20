#
# Collective Knowledge (index of CK repositories)
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
    import os

    d=i['dict']
    m=i['meta']

    dd=d.get('dict',{})

    if 'misc' not in d: d['misc']={}
    misc=d['misc']

    repo_url1_full=misc.get('repo_url1','')
    repo_url2_full=misc.get('repo_url2','')
    repo_url3_full=misc.get('repo_url3','')

    data_uoa=misc.get('data_uoa','')
    data_uid=misc.get('data_uid','')

    module_uoa=misc.get('module_uoa','')
    module_uid=misc.get('module_uid','')

    # Find real repo and get .ckr.json
    ckr={}
    rx=ck.access({'action':'where',
                  'module_uoa':cfg['module_deps']['repo'],
                  'data_uoa':data_uoa})
    if rx['return']==0: 
       pckr=os.path.join(rx['path'], ck.cfg['repo_file'])
       if os.path.isfile(pckr):
          rx=ck.load_json_file({'json_file':pckr})
          if rx['return']>0: return rx

          rxd=rx['dict']

          dx=rxd['dict']

          if 'path' in dx:
             del(dx['path'])

          real_repo_uid=rxd['data_uid']

          # Check if mismatch of real uid and current one (old bug - should be fixed now)
          if real_repo_uid!=data_uid:
             ck.out('')
             ck.out('WARNING: repo UID mismatch for '+data_uoa+' ('+real_repo_uid+' != '+data_uid+')')
             ck.out('')
          else:
             ckr=dx

    misc['ckr']=ckr

    # Check program workflows (pipelines of CK components) with tasks
    r=ck.access({'action':'list',
                 'repo_uoa':data_uoa,
                 'module_uoa':cfg['module_deps']['program']})
    if r['return']==0:
       tlst=r['lst']
       misc['tasks']={}
       for t in tlst:
           misc['tasks'][t['data_uid']]={'data_uoa':t['data_uoa']}

    # Get UIDs for repo deps
    repo_deps=ckr.get('repo_deps',{})
    for rd in repo_deps:
        xruoa=rd.get('repo_uoa','')
        r=ck.access({'action':'load',
                     'module_uoa':cfg['module_deps']['repo'],
                     'data_uoa':xruoa})
        if r['return']==0:
           xruid=r['data_uid']
           rd['repo_uid']=xruid

    # Check extra info
    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['cfg'],
                 'data_uoa':cfg['cfg-list-of-repos']})
    if r['return']==0:
       dx=r['dict']

       d1=dx.get(data_uid,{})
       if len(d1)>0:
          d=d1.get('dict',{})

          url=d.get('url','')
          external_url=d.get('external_url','')
          rd=d.get('repo_deps',{})

          ld=d.get('desc','')
          ld=ld.replace('$#repo_url#$',repo_url3_full)

          misc['desc']=ld

          workflow_desc=d.get('workflow_desc','')
          
          workflow_desc=workflow_desc.replace('$#repo_url#$',repo_url3_full)

          if d.get('ck_artifact','')!='' or d.get('reproducible_article','')=='yes' or d.get('passed_artifact_evaluation','')=='yes':
             if workflow_desc!='': workflow_desc+='<p>'
             workflow_desc+='reproducible&nbsp;paper\n'
             if d.get('passed_artifact_evaluation','')=='yes':
                workflow_desc+='-&nbsp;passed&nbsp;<a href="http://cTuning.org/ae">Artifact&nbsp;Evaluation</a>:\n'
                workflow_desc+='<p><center><img src="https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_evaluated_reusable_dl.jpg" width="64"></center>\n'

          misc['workflow_desc']=workflow_desc

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

    url0=i.get('url','')

    llm=d.get('meta',{})

    llmisc=llm.get('misc',{})
    lldict=llm.get('dict',{})

    ckr=llmisc.get('ckr',{})
    repo_deps=ckr.get('repo_deps',{})

    repo_url1=llmisc.get('repo_url1','')
    repo_url2=llmisc.get('repo_url2','')
    repo_url3=llmisc.get('repo_url3','')

    # Removing everything before tree
    url=repo_url3
    j=url.find('/tree/')
    if j>=0:
       url=url[:j]

    desc=llmisc.get('desc','')

    duoa=llmisc.get('data_uoa','')
    duid=llmisc.get('data_uid','')

    ruoa=llmisc.get('repo_uoa','')
    ruid=llmisc.get('repo_uid','')

    muoa=llmisc.get('module_uoa','')

    h=''

    h+='<div style="background-color:#efefef;margin:5px;padding:5px;">\n'

    if desc!='':
       h+='<b>Description:</b><br>\n'
       h+='<div style="margin-left:20px;">\n'
       h+=' '+desc+'\n'
       h+='</div>\n'

    to_get=llmisc.get('to_get','')
    if to_get!='':
       h+='<b>How to get:</b>\n'
       h+='<div style="margin-left:20px;">\n'
       h+='<span style="color:#2f0000">'+to_get+'</span><br>\n'
       h+='</div>\n'

    workflow_desc=llmisc.get('workflow_desc','')
    if workflow_desc!='':
       h+='<b>Workflow:</b><br>\n'
       h+='<div style="margin-left:20px;">\n'
       h+=' '+workflow_desc+'\n'
       h+='</div>\n'

    if len(repo_deps)>0:
       h+='<b>Dependencies on other repositories:</b><br>\n'
       h+='<div style="margin-left:20px;">\n'
       h+=' <ul>\n'
       for rd in repo_deps:
           ruoa=rd.get('repo_uoa','')
           ruid=rd.get('repo_uid','')
           if ruoa!='':
              x1=''
              x2=''
              if url0!='' and ruid!='':
                 prfx=''
                 if not bscp: prfx='cid='
                 x1='<a href="'+url0+prfx+work['self_module_uid']+':'+ruid+'" target="_blank">'
                 x2='</a>'
              h+='  <li>'+x1+'<span style="color:#2f0000;">'+str(ruoa)+'</span>'+x2+'</li>\n'

       h+=' </ul>\n'
       h+='</div>\n'

    tasks=llmisc.get('tasks',{})
    if len(tasks)>0:
       h+='<b>Tasks (program workflows):</b><br>\n'
       h+='<div style="margin-left:20px;">\n'
       h+=' <ul>\n'
       for tuid in tasks:
           tt=tasks[tuid]
           tuoa=tt.get('data_uoa','')
           if tuoa!='':
              prfx=''
              if not bscp: prfx='cid='
              x='<a href="'+url0+prfx+cfg['module_deps']['component.program']+':'+tuid+'" target="_blank">'+tuoa+'</a>'
              h+='  <li><span style="color:#2f0000;">'+x+'</li>\n'

       h+=' </ul>\n'
       h+='</div>\n'

    h+='</div>\n'

    h1=''

    if url!='':
       h1+='[&nbsp;<a href="'+url+'#readme" target="_blank">repo readme</a>&nbsp;]\n'
       h1+='[&nbsp;<a href="'+url+'" target="_blank">repo</a>&nbsp;]\n'

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
