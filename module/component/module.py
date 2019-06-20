#
# Collective Knowledge (indexing reusable research components)
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
# get index of components

def get(i):
    """
    Input:  {
              (web_vars_post)
              (web_vars_get)
              (web_vars_session)
              (skip_cid_predix) - if 'yes', skip "?cid=" prefix when creating URLs
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              html - HTML
            }

    """

    import copy
    import math
    import sys

    wvg=i.get('web_vars_get',{})
    if type(wvg)==list: wvg={}

    wvp=i.get('web_vars_post',{})
    if type(wvp)==list: wvp={}

    scp=i.get('skip_cid_prefix','')
    bscp=(scp=="yes")

    wv=copy.deepcopy(wvp)
    wv.update(wvg)

    # Page length
    length=wv.get('l','')
    dlength='10'
    if length=='': length=dlength
    ilength=int(length)

    # Page
    page=wv.get('p','')
    if page=='': page='1'
    ipage=int(page)

    # Check page name
    page_name=i.get('page_name','')
    if page_name=='':
       return {'return':1, 'error':'page_name is empty'}

    # Init URL
    url='/'+page_name
    if not bscp: 
       url+='?'
    else: 
       url+='/'
    url0=url

    # Check article
    a=wv.get('a','')

    # Check component and prepare selector
    c=wv.get('c','')
    if c=='': c='repo'

    c_uid='component.module' # Selected UID
    orig_module_uid=''

    if c=='article':
#       c_uid='repro.article'
       c_uid='b56ccd54ac2b15b9'
    elif c=='event':
       c_uid='c528f82d6ee43a79'

    r=ck.access({'action':'load',
                 'module_uoa':'cfg',
                 'data_uoa':'component'})
    if r['return']>0: return r
    rd=r['dict']

    if c=='article':
       di=rd.get('index_articles',[])
       selector=a
       selector_key='a'
    elif c=='event':
       di=rd.get('index_events',[])
       selector=a
       selector_key='a'
    else:
       di=rd.get('index',[])
       selector=c
       selector_key='c'

    r=create_selector({'list':di, 'c':selector, 'url':url, 'key':selector_key})
    if r['return']>0: return r
    hc=r['html']

    if r.get('c_uid','')!='': c_uid=r['c_uid']
    if r.get('orig_module_uid','')!='': orig_module_uid=r['orig_module_uid']
    if r.get('url','')!='' and r.get('url','')!=url: url=r['url']

    # Check if CID
    cid=wv.get('cid','')
    d_uoa=''
    if cid!='':
       r=ck.parse_cid({'cid':cid})
       if r['return']==0:
          c_uid=r.get('module_uoa','')
          d_uoa=r.get('data_uoa','')
          selector=''

    # Parse search string
    q=wv.get('q','')
    q=q.encode('utf8')

    if '"' in q:
       q1=q.split('"')
    else:
       q1=q.split(' ')
    qs=[]
    for q in q1:
        if q!='':
           if q.startswith(' '):
              q3=q.strip().split(' ')
              q2=[]
              for q in q3:
                  q2.append(q.strip().lower())
           else:
              q2=[q.strip().lower()]
           qs+=q2

    try:    from urllib.parse import urlencode
    except: from urllib import urlencode # pragma: no cover

    qq=urlencode({'q':q})
    if sys.version_info[0]>2: qq=qq.encode('utf8')

    url+='&'+qq

    if ilength!=dlength:
       url+='&l='+str(ilength)

    # Search via CK
    ii={"action":"list",
        "module_uoa":c_uid,
        "add_meta":"yes",
        "filter_func_addr":getattr(sys.modules[__name__],'search_filter'),
        "search_dict":qs}
    if d_uoa!='':
       ii['data_uoa']=d_uoa

    r=ck.access(ii)
    if r['return']>0: return r

    lst=r['lst']
    ep=r['elapsed_time']

    # Extra processing if article and selector != ""
    if c=='article':
       if selector=='-': selector=''
       if selector!='':
          lselector=selector.split(',')
          lst1=[]
          for l in lst:
              tags=l['meta'].get('tags',[])
              for ll in lselector:
                  if ll in tags:
                     lst1.append(l)
          lst=lst1
       # Sort by title
       lst=sorted(lst, key=lambda x: (x.get('meta',{}).get('misc',{}).get('title','').lower()))
    else:
       # Sort by data alias
       lst=sorted(lst, key=lambda x: x.get('meta',{}).get('misc',{}).get('data_uoa','').lower())

    llst=len(lst)

    x=''
    if llst==0 or llst>1: x='s'
    h=''
    if llst!=1:
       h='<center>'+str(llst)+' result'+x+' ('+("%.3f" % float(ep))+' seconds)<br></center>\n'

    # List
    j1=(ipage-1)*ilength
    j2=((ipage)*ilength)-1
    if j2>=llst: j2=llst-1

    # Go through the pruned list
    number_of_entries=(j2-j1+1)
    for j in range(j1,j2+1):
        jj=j+1

        ll=lst[j]

        llm=ll['meta']

        llmisc=llm.get('misc',{})

        duoa=llmisc.get('data_uoa','')
        duid=llmisc.get('data_uid','')
        if duid=='':
           duid=ll['data_uid']

        muid=llmisc.get('module_uid','')
        muoa=llmisc.get('module_uoa','')

        r=ck.access({'action':'html',
                     'module_uoa':c_uid,
                     'dict':ll,
                     'url':url0,
                     'skip_cid_prefix':scp,
                     'number_of_entries':number_of_entries})
        if r['return']>0: return r

        hh=r['html']
        hh1=r.get('html1','')
        article=r.get('article','')

        xcid=c_uid+':'+duid

        h+='<div id="ck_entries">\n'
        prfx=''
        if not bscp: prfx='cid='

        xurl1='<a href="'+url0+prfx+xcid+'"><span style="color:#2f0000;"><b>'
        xurl2='</b></span></a>'

        if llst==1:
           if article!='':
              h+=xurl1+article+xurl2+'\n'
           else:
              h+=xurl1+muoa+':'+duoa+xurl2+'\n'
        else:
           if article!='':
              h+=str(jj)+') '+xurl1+article+xurl2+'\n'
           else:
              h+=str(jj)+') '+xurl1+duoa+xurl2+'\n'

        h+=hh

        # Extra links
        url_help=cfg['url_ck_github_components']+cfg['module_deps']['module']+'_'+orig_module_uid

        h+='<div id="ck_entries_space4"></div>\n'
        h+='<div id="ck_downloads">\n'

        if orig_module_uid!='':
           h+='[&nbsp;<a href="'+url_help+'" target="_blank">help</a>&nbsp;] \n'

        if c=='article' or c=='event':
           y=cfg['url_rr_github_components2']
        else:
           y=cfg['url_rr_github_components']
        h+='[&nbsp;<a href="'+y+'.'+c+'/'+duid+'/.cm/meta.json" target="_blank">index</a>&nbsp;]&nbsp;&nbsp; \n'

        if hh1!='':
           h+=hh1

        h+='</div>\n'

        h+='</div>\n'

        h+='<div id="ck_entries_space4"></div>\n'

    # Get page index
    tpages=int(math.ceil(float(llst)/float(ilength)))

    if tpages>1:
       h+='<p>Pages:&nbsp;&nbsp;&nbsp; '
       h1=''
       for p in range(0, tpages):
           rp=p+1

           url1=url
           if ilength!=dlength:
              url1+='&p='+str(rp)

           x1='<a href="'+url1+'">'
           x2='</a>'
           if rp==ipage:
              x1=''
              x2=''

           if h1!='': h1+=' '
           h1+=x1+str(p+1)+x2

       if (ipage+1)<=tpages:
          url1=url
          url1+='&p='+str(ipage+1)

          h1+='&nbsp;&nbsp;&nbsp; <a href="'+url1+'">Next</a>\n'

       h+=h1

    return {'return':0, 'len':llst, 'html':h, 'html_c':hc}

##############################################################################
# index components

def index(i):
    """
    Input:  {
              (data_uoa)        - specify which components to index (module name); if "", take from cfg:component
              (target_repo_uoa) - if "", use "reproindex"

              (component_uoa)   - index specific component

              (share)           - if 'yes', add to Git
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import copy
    import json

    o=i.get('out','')

    tr_uoa=i.get('target_repo_uoa','')
    if tr_uoa=='': tr_uoa='reproindex'

    share=i.get('share','')

    # Check which components to index
    qduoa=i.get('data_uoa','')
    if qduoa!='':
       r=ck.access({'action':'load',
                    'module_uoa':cfg['module_deps']['module'],
                    'data_uoa':qduoa})
       if r['return']>0: return r
       qduoa=r['data_uid']

    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['cfg'],
                 'data_uoa':'component'})
    if r['return']>0: return r
    components=r['dict']['index']

    component_uoa=i.get('component_uoa','')

    for cc in components:
        name=cc["name"]
        c_uid=cc["uid"]
        cm_uid=cc["orig_module_uid"]

        if qduoa!='' and c_uid!=qduoa:
           continue

        ck.out('==========================================================')
        ck.out('Indexing component: '+name)
        ck.out('')

        # Search for components
        ii={}
        ii['action']='list'
        ii['module_uoa']=cm_uid
        ii['add_meta']='yes'
        ii['time_out']=-1

        if component_uoa!='':
           ii['data_uoa']=component_uoa

        rx=ck.access(ii)
        if rx['return']>0: return rx

        ll=sorted(rx['lst'], key=lambda k: k['data_uoa'])

        repo_url={}
        repo_private={}

        private=''
        num=0

        h=''

        for l in ll:
            ln=l['data_uoa']
            ln_uid=l['data_uid']

            lm_uoa=l['module_uoa']
            lm_uid=l['module_uid']

            lr=l['repo_uoa']
            lr_uid=l['repo_uid']

            url=''
            if lr=='default':
               url='https://github.com/ctuning/ck/tree/master/ck/repo'
            elif lr_uid in repo_url:
               url=repo_url[lr_uid]
            else:
               rx=ck.load_repo_info_from_cache({'repo_uoa':lr_uid})
               if rx['return']>0: return rx
               url=rx.get('dict',{}).get('url','')

               if url!='' and url.startswith('git@'):
                  url=url.replace(':','/').replace('git@','https://')

               repo_private[lr_uid]=rx.get('dict',{}).get('private','')
               repo_url[lr_uid]=url

            # Check if indexing repository (slightly different mechanism from all other components)
            skip=False
            if lm_uoa=='repo':
               lm=l['meta']

               if 'path' in lm: 
                  real_path=lm.get('path','')

                  del(lm['path'])

                  ppr=os.path.join(real_path, '.ckr.json')

                  rz=ck.load_json_file({'json_file':ppr})
                  if rz['return']==0: 
                     lm=rz['dict'].get('dict',{})

                  print (lm)

               private=lm.get('private','')

               skip_indexing=lm.get('skip_from_index','')
               remote=lm.get('remote','')
               url=lm.get('url','')

               if url!='' and url.startswith('git@'):
                  url=url.replace(':','/').replace('git@','https://')

               if url=='' or private=='yes' or skip_indexing=='yes' or remote=='yes' or ln=='default' or ln=='local' or ln in ck.cfg.get('skip_repos',[]):
                  skip=True

            elif not (lr not in ck.cfg.get('skip_repos',[]) and repo_private.get(lr_uid,'')!='yes' and url!=''):
               skip=True

            print (skip)

            if not skip:
               num+=1

               ck.out('  '+str(num)+') '+ln)

               # Check if entry already exists
               ddd={}
               ddd_exist={}
               exist=False
               r=ck.access({'action':'load',
                            'module_uoa':c_uid,
                            'data_uoa':ln_uid,
                            'repo_uoa':tr_uoa})
               if r['return']>0 and r['return']!=16: return r
               if r['return']==0: 
                  ddd=r['dict']
                  ddd_exist=copy.deepcopy(ddd)
                  exist=True

               # General vars
               lm=l['meta']
               ld=lm.get('desc','')

               # Info about repo
               if lm_uoa!='repo' and lr=='default':
                  to_get=''
               elif url.find('github.com/ctuning/')>0:
                  x=lr
                  if lm_uoa=='repo': x=ln
                  to_get='ck pull repo:'+x
               else:
                  to_get='ck pull repo --url='+url

               repo_url1_full=''
               repo_url2_full=''
               repo_url3_full=''
               if url!='':
                  url2=url

                  if url2.endswith('.git'):
                     url2=url2[:-4]

                  if '/tree/master/' not in url2:
                     url2+='/tree/master/'+lm_uoa+'/'
                  else:
                     url2+='/'+lm_uoa+'/'

                  if lm_uoa=='module':
                     repo_url1_full=url2+ln+'/module.py'
                  elif lm_uoa=='repo':
                     if lm.get('skip_from_index','')=='yes':
                        continue
                     repo_url3_full=url2+ln
                  else:
                     repo_url3_full=url2+ln

                  repo_url2_full=url2+ln+'/.cm/meta.json'

               # Update dict
               ddd['dict']=copy.deepcopy(lm)
               ddd['misc']={'repo_url1':repo_url1_full,
                            'repo_url2':repo_url2_full,
                            'repo_url3':repo_url3_full,
                            'data_uoa':ln,
                            'data_uid':ln_uid,
                            'repo_uoa':lr,
                            'repo_uid':lr_uid,
                            'module_uoa':lm_uoa,
                            'module_uid':lm_uid,
                            'to_get':to_get}

               # Add specific info per component
               r=ck.access({'action':'add_index',
                            'module_uoa':c_uid,
                            'dict':ddd,
                            'meta':lm})
               if r['return']>0: return r

               # Add/update entry
               ii={'module_uoa':c_uid,
                   'data_uoa':ln_uid,
                   'repo_uoa':tr_uoa,
                   'dict':ddd,
                   'substitute':'yes',
                   'sort_keys':'yes'}

               if exist:
                  ii['action']='update'
                  ii['ignore_update']='yes'

                  # Hack to check arrays
                  j1=json.dumps(ddd_exist,sort_keys=True)
                  j2=json.dumps(ddd,sort_keys=True)

                  if j1!=j2:
                     ck.out('            Index updated; UID: '+ln_uid )
                     r=ck.access(ii)
                     if r['return']>0: return r
                  else:
                     ck.out('            Update SKIPPED; UID: '+ln_uid)

               else:
                  ii['action']='add'

                  ii['share']=share

                  r=ck.access(ii)
                  if r['return']>0: return r

                  new_uid=r['data_uid']
                  ck.out('            Generated UID: '+new_uid)
 

        ck.out('')
        ck.out('  Total components: '+str(num))
        ck.out('')

    return {'return':0}

##############################################################################
# search filter

def search_filter(i):

    meta=i.get('meta',{})
    sd=i.get('search_dict',[])

    skip='yes'

    if len(sd)==0:
       skip='no'

    for s in sd:
        for k in meta:
            if not search_filter_recursive(meta[k],s):
               skip='no'
               break

    return {'return':0, 'skip':skip}

##############################################################################
# search filter (recursive)

def search_filter_recursive(v,s):
    skip=True

    if type(v)==list:
       for k in v:
          if not search_filter_recursive(k,s):
             skip=False
             break
    elif type(v)==dict:
        for k in v:
            if not search_filter_recursive(v[k],s):
               skip=False
               break
    else:
        try:
            v=str(v).lower()
        except:
            pass

        if s in v:
           skip=False

    return skip

##############################################################################
# create selector

def create_selector(i):

    di=i['list']
    c=i['c']
    url=i['url']
    key=i.get('key','')
    if key=='': key='c'

    hc=''

    c_uid=''
    orig_module_uid=''

    for q in di:
        name=q['name']
        xid=q.get('id','')
        uid=q.get('uid','')

        hc+='<option value="'+xid+'"'
        if xid==c:
           hc+=' selected'
           c_uid=uid
           orig_module_uid=q.get('orig_module_uid','')
           url+='&'+key+'='+xid
        hc+='>'+name+'</option>\n'

    return {'return':0, 'html':hc, 'c_uid':c_uid, 'orig_module_uid':orig_module_uid, 'url':url}

##############################################################################
# get component from CMD

def get_from_cmd(i):
    """
    Input:  {
              (data_uoa)      - component module UOA
              (component_uoa) - component UOA (not UID!)
              (s) or (string) - search string
              (all)           - if 'yes', show repo and path
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import sys

    # Parse search string
    s=i.get('s','')
    if s=='': s=i.get('string','')

    if '"' in s:
       s1=s.split('"')
    else:
       s1=s.split(' ')
    ss=[]
    for s in s1:
        if s!='':
           if s.startswith(' '):
              s3=s.strip().split(' ')
              s2=[]
              for s in s3:
                  s2.append(s.strip().lower())
           else:
              s2=[s.strip().lower()]
           ss+=s2

    # Other vars
    muoa=i.get('data_uoa','')

    duoa=i.get('component_uoa','')
    duid=''
    if ck.is_uid(duoa):
       duid=duoa
       duoa=''

    xall=i.get('all','')

    # Search
    ii={"action":"list",
        "module_uoa":muoa,
        "add_meta":"yes",
        "filter_func_addr":getattr(sys.modules[__name__],'search_filter'),
        "search_dict":ss}
    if duid!='':
       ii['data_uoa']=duid
    r=ck.access(ii)
    if r['return']>0: return r

    lst=r['lst']
    ep=r['elapsed_time']

    # Sort by name
    lst=sorted(lst, key=lambda x: x.get('meta',{}).get('misc',{}).get('data_uoa',''))

    for ll in lst:
        muoa=ll['module_uoa']
        ruoa=ll['repo_uoa']

        llm=ll['meta']
        misc=llm.get('misc',{})

        misc_duoa=misc.get('data_uoa','')

        if duoa!='' and misc_duoa!=duoa:
           continue

        xduid=ll['data_uid']

        p=muoa+':'+xduid
        if xall=='yes':
           p=ruoa+':'+p+' ('+misc_duoa+') - '+ll['path']

        ck.out(p)

    return {'return':0}
