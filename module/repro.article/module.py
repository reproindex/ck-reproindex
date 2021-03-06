#
# Collective Knowledge (index of reproducible articles)
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

    short=i.get('short','')

    llm=d.get('meta',{})

    llmisc=llm.get('misc',{})
    lldict=llm.get('dict',{})

    repo_url1=llmisc.get('repo_url1','')
    repo_url2=llmisc.get('repo_url2','')
    repo_url3=llmisc.get('repo_url3','')

    duoa=llmisc.get('data_uoa','')
    duid=llmisc.get('data_uid','')

    ruoa=llmisc.get('repo_uoa','')
    ruid=llmisc.get('repo_uid','')

    muid=llmisc.get('module_uid','')
    muoa=llmisc.get('module_uoa','')

    #Main
    title=llmisc.get('title','')
    authors=llmisc.get('authors','')
    where=llmisc.get('where','')
    paper_pdf_url=llmisc.get('paper_pdf_url','')
    paper_doi_url=llmisc.get('paper_doi_url','')
    artifact_doi_url=llmisc.get('artifact_doi_url','')

    workflow=llmisc.get('workflow','')
    workflow_url=llmisc.get('workflow_url','')

    h=''
    article=''
    if title!='':
       article='<b>'+title+'</b>'

    if authors!='':
       h+='<div id="ck_entries_space4"></div>\n'
       h+='<i>'+authors+'</i>\n'

    baaa=llmisc.get('badge_acm_artifact_available','')
    baaf=llmisc.get('badge_acm_artifact_functional','')
    baar=llmisc.get('badge_acm_artifact_reusable','')
    barr=llmisc.get('badge_acm_results_reproduced','')
    barp=llmisc.get('badge_acm_results_replicated','')

    badges=''
    if baaa!='':
       badges+=' <a href="http://cTuning.org/ae/reviewing.html#artifacts_available"><img src="https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_available_dl.jpg" width="64"></a>'
    if baaf!='':
       badges+=' <a href="http://cTuning.org/ae/reviewing.html#artifacts_functional"><img src="https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_evaluated_functional_dl.jpg" width="64"></a>'
    if baar!='':
       badges+=' <a href="http://cTuning.org/ae/reviewing.html#artifacts_reusable"><img src="https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_evaluated_reusable_dl.jpg" width="64"></a>'
    if barr!='':
       badges+=' <a href="http://cTuning.org/ae/reviewing.html#results_validated"><img src="https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/results_reproduced_dl.jpg" width="64"></a>'
    if barp!='':
       badges+=' <a href="http://cTuning.org/ae/reviewing.html#results_validated"><img src="https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/results_replicated_dl.jpg" width="64"></a>'

    if workflow.lower()=='ck':
       x1=''
       x2=''
       if workflow_url!='':
          x1='<a href="'+workflow_url+'">'
          x2='</a>'
       badges+=' '+x1+'<img src="https://ctuning.org/ae/stamps/ck-workflow.png" width="100">'+x2


    if badges!='':
       h+='<div id="ck_entries_space4"></div>\n'
       h+='<center>'+badges+'</center>\n'

    h1=''
    if short!='yes':
       h+='<div style="background-color:#efefef;margin:5px;padding:5px;">\n'

       url0=i.get('url','')
       urlc=url0.replace('index.php','c.php') # Needed for components
#       x1=''
#       x2=''
#       if url0!='' and ruid!='':
#          prfx=''
#          if not bscp: prfx='cid='
#          x1='<a href="'+url0+prfx+cfg['module_deps']['component.repo']+':'+ruid+'" target="_blank">'
#          x2='</a>'
#       h+='<b>Repo name:</b> '+x1+ruoa+x2+'<br>\n'

       where_url=llmisc.get('where_url','')
       if where!='':
          x1=''
          x2=''
          if where_url!='':
             x1='<a href="'+where_url+'">'
             x2='</a>'
          h+='<b>Where published:</b> '+x1+where+x2+'<br>\n'

       if paper_doi_url!='':
          x=paper_doi_url
          j=paper_doi_url.find('doi.org/')
          if j>0: x=paper_doi_url[j+8:]
          h+='<b>Article DOI:</b> <a href="'+paper_doi_url+'">'+x+'</a><br>\n'

       if paper_pdf_url!='':
          h+='<b>Article:</b> <a href="'+paper_pdf_url+'">PDF</a><br>\n'

       if artifact_doi_url!='':
          x=artifact_doi_url
          j=artifact_doi_url.find('doi.org/')
          if j>0: x=artifact_doi_url[j+8:]
          h+='<b>Artifact DOI:</b> <a href="'+artifact_doi_url+'">'+x+'</a><br>\n'

       uaa=llmisc.get('unified_artifact_appendix','')
       if uaa!='':
          h+='<b>Unified artifact appendix:</b> <a href="'+uaa+'">Link</a><br>\n'

       arts=llmisc.get('artifact_sources','')
       arts_url=llmisc.get('artifact_sources_url','')

       if arts_url!='':
          x=arts_url
          if arts!='': x=arts
          h+='<b>Artifact before standardization:</b> <a href="'+arts_url+'">'+x+'</a><br>\n'


       if workflow_url!='':
          x=workflow_url
          y='Automated workflow'
          if workflow!='': 
             x=workflow
             if x=='CK': 
                x='Link'
                y='Standardized CK workflow'
          h+='<b>'+y+':</b> <a href="'+workflow_url+'">'+x+'</a>\n'

          ck_repo_uid=llmisc.get('ck_repo_uid','')
          if ck_repo_uid!='':
             prfx=''
             if not bscp: prfx='cid='
             x=urlc+prfx+cfg['module_deps']['component.repo']+':'+ck_repo_uid
             h+=' (<a href="'+x+'">ReproIndex</a>)\n'

          h+='<br>\n'

       tasks=llmisc.get('tasks',{})
       if len(tasks)>0:
          h+='<b>Standardized CK pipelines (programs):</b><br>\n'
          h+='<div style="margin-left:20px;">\n'
          h+=' <ul>\n'
          for tuid in tasks:
              tt=tasks[tuid]
              tuoa=tt.get('data_uoa','')
              if tuoa!='':
                 prfx=''
                 if not bscp: prfx='cid='
                 x='<a href="'+urlc+prfx+cfg['module_deps']['component.program']+':'+tuid+'" target="_blank">'+tuoa+'</a>'
                 h+='  <li><span style="color:#2f0000;">'+x+'</li>\n'

          h+=' </ul>\n'
          h+='</div>\n'

       results=llmisc.get('results','')
       results_url=llmisc.get('results_url','')
       if results_url!='':
          x=results_url
          if results!='': x=results
          h+='<b>Reproducible results:</b> <a href="'+results_url+'">'+x+'</a><br>\n'

       some_results_replicated=llmisc.get('some_results_replicated','')
       if some_results_replicated=='yes':
          h+='<b>Some results replicated:</b> &#10004;<br>\n'

       rurl=llmisc.get('reproducibility_url','')
       if rurl!='':
          x='Link'
          if 'acm' in rurl.lower() or 'ctuning' in rurl.lower():
             x='ACM and cTuning'
          h+='<b>Reproducible  methodology:</b> <a href="'+rurl+'">'+x+'</a><br>\n'

       results_dashboard_url=llmisc.get('results_dashboard_url','')
       if results_dashboard_url!='':
          x=results_dashboard_url
          j=x.find('://')
          if j>=0:
             x=x[j+3:]
          h+='<b>Dashboard with results:</b> <a href="'+results_dashboard_url+'">'+x+'</a><br>\n'

       h+='</div>\n'

       # Extras
       h1=''

       if paper_doi_url!='':
          h1+='[&nbsp;<a href="'+paper_doi_url+'" target="_blank">paper</a>&nbsp;] \n'

#       ck_repo_uid=llmisc.get('ck_repo_uid','')
#       if ck_repo_uid!='':
#          prfx=''
#          if not bscp: prfx='cid='
#          x=urlc+prfx+cfg['module_deps']['component.repo']+':'+ck_repo_uid
#          h1+='[&nbsp;<a href="'+x+'" target="_blank">CK repository</a>&nbsp;] \n'

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
    r=ck.inp({'text':'Enter event tags without spaces and separated by comma (example: papers,papers-sysml-2019): '})
    if r['return']>0: return r
    s=r['string'].strip().lower()

    tags=s.split(',')
    d['tags']=tags

    ##########################################################
    r=ck.inp({'text':'Enter title: '})
    if r['return']>0: return r
    misc['title']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter authors separated by comma: '})
    if r['return']>0: return r
    misc['authors']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter event title (example: SysML\'19): '})
    if r['return']>0: return r
    misc['where']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter event URL: '})
    if r['return']>0: return r
    misc['where_url']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter PDF URL (if available): '})
    if r['return']>0: return r
    misc['paper_pdf_url']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter paper DOI URL: '})
    if r['return']>0: return r
    misc['paper_doi_url']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter artifact DOI URL: '})
    if r['return']>0: return r
    misc['artifact_doi_url']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter artifact sources URL: '})
    if r['return']>0: return r
    misc['artifact_sources_url']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter artifact sources type (example: GitHub, GitLab, BitBucket): '})
    if r['return']>0: return r
    misc['artifact_sources']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter URL for unified artifact appendix template (if used by this article): '})
    if r['return']>0: return r
    misc['unified_artifact_appendix']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter automated workflow URL (if used): '})
    if r['return']>0: return r
    misc['workflow_url']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter automated workflow type (example: CK): '})
    if r['return']>0: return r
    misc['workflow']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter URL with reproducible results (if available): '})
    if r['return']>0: return r
    misc['results_url']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter results format (example: CK format): '})
    if r['return']>0: return r
    misc['results']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter used methodology for reproducibility: '})
    if r['return']>0: return r
    misc['reproducibility_url']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter URL for dashboard (if used): '})
    if r['return']>0: return r
    misc['results_dashboard_url']=r['string'].strip()

    ##########################################################
    r=ck.inp({'text':'Enter CK repository UID (if used): '})
    if r['return']>0: return r
    misc['ck_repo_uid']=r['string'].strip().lower()

    ##########################################################
    r=ck.inp({'text':'Enter yes if artifact is available (ACM badges): '})
    if r['return']>0: return r
    misc['badge_acm_artifact_available']=r['string'].strip().lower()

    ##########################################################
    r=ck.inp({'text':'Enter yes if artifact is functional (ACM badges): '})
    if r['return']>0: return r
    misc['badge_acm_artifact_functional']=r['string'].strip().lower()

    ##########################################################
    r=ck.inp({'text':'Enter yes if artifact is reusable (ACM badges): '})
    if r['return']>0: return r
    misc['badge_acm_artifact_reusable']=r['string'].strip().lower()

    ##########################################################
    r=ck.inp({'text':'Enter yes if results were reproduced (ACM badges): '})
    if r['return']>0: return r
    misc['badge_acm_results_reproduced']=r['string'].strip().lower()

    ##########################################################
    r=ck.inp({'text':'Enter yes if results were replicated (ACM badges): '})
    if r['return']>0: return r
    misc['badge_acm_results_replicated']=r['string'].strip().lower()

    ##########################################################
    r=ck.inp({'text':'Enter yes if some results were replicated: '})
    if r['return']>0: return r
    misc['some_results_replicated']=r['string'].strip().lower()

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
