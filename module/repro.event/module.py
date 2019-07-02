#
# Collective Knowledge (index of reproducible events)
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

def index(i):
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
    import json

    i['action']='search'
    i['add_meta']='yes'
    i['out']=''
    i['cid']=''

    r=ck.access(i)
    if r['return']>0: return r

    lst=r['lst']

    for l in lst:
        ck.out('=========================================================')

        duid=l['data_uid']
        muid=l['module_uid']
        ruid=l['repo_uid']

        ck.out('* '+duid)

        d=l['meta']
        dorig=copy.deepcopy(d)

        # Check CK repo UID with tasks
        ck_repo_uid=d['misc'].get('ck_repo_uid','')
        if ck_repo_uid!='':
           # Load repo component and take task
           r=ck.access({'action':'load',
                        'module_uoa':cfg['module_deps']['component.repo'],
                        'data_uoa':ck_repo_uid})
           if r['return']>0: return r
           dr=r['dict']
           tasks=dr.get('misc',{}).get('tasks',{})
           if len(tasks)>0:
               d['misc']['tasks']=tasks

               # Hack to check arrays
               j1=json.dumps(dorig,sort_keys=True)
               j2=json.dumps(d,sort_keys=True)

               if j1!=j2:
                  ck.out('            Index updated')

                  # Update entry
                  ii={'action':'update',
                      'module_uoa':muid,
                      'data_uoa':duid,
                      'repo_uoa':ruid,
                      'dict':d,
                      'substitute':'yes',
                      'sort_keys':'yes',
                      'ignore_update':'yes'}

                  r=ck.access(ii)
                  if r['return']>0: return r
               else:
                  ck.out('            Update SKIPPED')

    return {'return':0}

##############################################################################
# generate html

def html(i):
    """
    Input:  {
              (skip_cid_predix)   - if 'yes', skip "?cid=" prefix when creating URLs
              (number_of_entries) - if 1, then single entry view
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    d=i.get('dict',{})

    scp=i.get('skip_cid_prefix','')
    bscp=(scp=="yes")

    short=i.get('short','')

    single_entry=(i.get('number_of_entries','')==1)

    llm=d.get('meta',{})

    llmisc=llm.get('misc',{})
    lldict=llm.get('dict',{})

    repo_url1=llmisc.get('repo_url1','')
    repo_url2=llmisc.get('repo_url2','')
    repo_url3=llmisc.get('repo_url3','')

    duoa=d.get('data_uoa','')
    duid=d.get('data_uid','')

    ruoa=d.get('repo_uoa','')
    ruid=d.get('repo_uid','')

    muid=d.get('module_uid','')
    muoa=d.get('module_uoa','')

    url0=i.get('url','')
    # ugly -> improve url clean up
    urlc=url0.replace('events','components').replace('index.php','c.php') # Needed for components

    #Main
    title=llmisc.get('title','')

    date=llmisc.get('date','')
    date_p=llmisc.get('date_print','')

    deadline=llmisc.get('deadline','')
    deadline_p=llmisc.get('deadline_print','')

    h=''

    # Check if in sinlge_entry mode and check if there is an html file
    p=d['path']
    s=''
    ff=os.path.join(p, 'info.html')
    if os.path.isfile(ff):
       r=ck.load_text_file({'text_file':ff})
       if r['return']==0:
          s=r['string'].strip()

    if single_entry and s!='':
       article='-'

       if title!='':
          x1='<b>'
          x2='</b>'
          if single_entry:
             x1='<h2><center>'
             x2='</center></h2>'
          h+=x1+title+x2

          h+='\n<p>'+s+'\n'
    else:
       article=title

       h+='<div id="ck_entries_space4"></div>\n'

       h+='<div style="background-color:#efefef;margin:5px;padding:5px;">\n'

       event_url=llmisc.get('url','')
       if event_url=='':
          if llmisc.get('use_self_url','')=='yes':
             event_url='/event/'+duoa

       if event_url!='':
          if event_url.lower()=='tba':
             x='TBA'
          else:
             x='<a href="'+event_url+'">Link</a>'
          h+='<b>Website:</b> '+x+'<br>\n'

       x=date_p
       if x=='': x=date
       if x!='':
          h+='<b>Date:</b> '+x+'<br>\n'

       x=deadline_p
       if x=='': x=deadline
       if x!='':
#          h+='<b>Deadline:</b> <span style="color:#7f0000";>'+x+'</span><br>\n'
          h+='<b>Deadline:</b> '+x+'<br>\n'

#       x=llm.get('tags',[])
#       if len(x)!='':
#          h+='<b>CK tags:</b> '+','.join(x)+'<br>\n'

       x=llmisc.get('reproduced_papers_tags','')
       if x!='':
          h+='<b>Reproduced papers:</b> <a href="/papers/&a='+x+'">Link</a><br>\n'

       x=llmisc.get('digital_library_url','')
       if x!='':
          h+='<b>Digital library:</b> <a href="'+x+'">Link</a><br>\n'

       x=llmisc.get('report_url','')
       if x!='':
          h+='<b>Report:</b> <a href="'+x+'">Link</a><br>\n'

       x=llmisc.get('workflows',[])
       if len(x)>0:
          h+='<b>Workflows:</b><br>\n'
          h+='<ul>\n'
          for y in x:
              yn=y.get('name','')
              yc=y.get('cid','')

              prfx=''
              if not bscp: prfx='cid='
              z=urlc+prfx+yc
              h+='<li><a href="'+z+'">'+yn+'</a>\n'
          h+='</ul>\n'

       x=llmisc.get('dashboard_url','')
       if x!='':
          y=llmisc.get('dashboard_note','')
          h+='<b>Dashboard'+y+':</b> <a href="'+x+'">Link</a><br>\n'

       x=llmisc.get('notes','')
       if x!='':
          h+='<b>Notes:</b> <i>'+x+'</i><br>\n'

       h+='</div>\n'

    # Extras
    h1=''

    ck_repo_uid=llmisc.get('ck_repo_uid','')
    if ck_repo_uid!='':
       prfx=''
       if not bscp: prfx='cid='
       x=urlc+prfx+cfg['module_deps']['component.repo']+':'+ck_repo_uid
       h1+='[&nbsp;<a href="'+x+'" target="_blank">CK repository</a>&nbsp;] \n'

    return {'return':0, 'html':h, 'html1':h1, 'article':article}

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

##############################################################################
# add new index manually

def add(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    for k in ['cids', 'cid', 'xcids']:
        if k in i: del(i[k])

    o=i.get('out','')

    ruoa=i.get('repo_uoa','')
    if ruoa=='': tr_uoa='reproindex'

    i['common_func']='yes'
    i['sort_keys']='yes'

    share=i.get('share','')
    if share=='': share='yes'
    i['share']='yes'

    d=i.get('dict',{})

    if 'misc' not in d: d['misc']={}
    misc=d.get('misc',{})

    # Ask questions
    ##########################################################
    r=ck.inp({'text':'Enter event tags without spaces and separated by comma (example: events,events-challenges): '})
    if r['return']>0: return r
    s=r['string'].strip().lower()

    tags=s.split(',')
    d['tags']=tags

    ##########################################################
    r=ck.inp({'text':'Enter event name: '})
    if r['return']>0: return r
    misc['title']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter event URL: '})
    if r['return']>0: return r
    misc['url']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter date: '})
    if r['return']>0: return r
    misc['date']=r['string'].strip()

    # update dict
    i['dict']=d

    ck.out('')

    # Add entry
    r=ck.access(i)
    if r['return']>0: return r

    # Print info
    p=r['path']
    p1=os.path.join(p,'.cm/meta.json')

    ck.out('')
    ck.out('You can continue editing meta description file "'+p1+'" directly ...')

    return r
