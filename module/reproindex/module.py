#
# Collective Knowledge (main reprodindex module)
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
# request research validation

def request(i):
    """
    Input:  {
              (request) - text of request
              (ck_user) - CK user
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    wvp = i.get('web_vars_post', {})

    r = ck.access({'action': 'find', 
                   'module_uoa': cfg['module_deps']['misc'], 
                   'data_uoa': cfg['request_uoa']})
    if r['return'] == 0:
        p = r['path']
    else:
        if r['return'] != 16: return r
        r = ck.access({'action': 'add', 'module_uoa': cfg['module_deps']['misc'], 
           'data_uoa': cfg['request_uoa']})
        if r['return'] > 0: return r
        p = r['path']

    r = ck.get_current_date_time({})
    if r['return'] > 0: return r

    a = r['array']

    fname = str(a['date_year'])
    x = str(a['date_month'])
    if len(x) == 1:
        x = '0' + x

    fname += x
    x = str(a['date_day'])
    if len(x) == 1:  x = '0' + x
    fname += x

    r = ck.gen_tmp_file({'suffix': '.json', 'prefix': '', 'remove_dir': 'yes'})
    if r['return'] > 0: return r

    fname += '-' + r['file_name']

    pfname = os.path.join(p, fname)

    dd = {'request': wvp.get('request', ''), 'ck_user': wvp.get('ck_user', '')}

    r = ck.save_json_to_file({'json_file': pfname, 'dict': dd})
    if r['return'] > 0: return r

    return {'return': 0}
