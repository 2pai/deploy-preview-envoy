import sys
import jinja2
from ruamel.yaml import YAML
yaml = YAML(typ='safe')

## example command 
## python3 gen.py 0000000000000000000000000000000000000000 1ecfd275763eff1d6b4844ea3168962458c9f27a fitur-1
## in order $CI_COMMIT_BEFORE_SHA $CI_COMMIT_SHA $CI_COMMIT_REF_SLUG  

DOMAIN = "2pai-dev.com"

## vars as defined below
prev_sha = sys.argv[1]
curr_sha = sys.argv[2]
curr_branch = sys.argv[3]
svc_port = sys.argv[4]
status = sys.argv[5]

def value_yaml(prev,curr,branch,port):
    value_yaml = open('vars/value.yaml').read()
    val = yaml.load(value_yaml)

    # check if it's the new MR x branch & append init data
    # new MR in some branch always have prev_sha with 0000000000000000000000000000000000000000
    if prev == "0000000000000000000000000000000000000000":
        val['list_svc'].append({
            'cluster_name': branch + "-cluster",
            'route_name': branch + "-route",
            'service_name': branch + "-"+ curr, 
            'service_port': int(port),    
            'domain': [branch+'-'+curr+'.'+DOMAIN]
        })
    elif prev == curr: # If prev == curr then remove the val from the list (Assuming MR to branch master was merged, then set Makefile curr == prev)
        val['list_svc'][:] = [x for x in val['list_svc'] if not (branch + "-"+ curr == x.get('service_name'))]
    else:
        for data in val['list_svc']:
            if data['cluster_name'] == branch+"-cluster" and data['service_name'] == (branch + "-"+ prev):
                data['service_name'] = branch + "-" + curr
                data['domain'] = [branch+'-'+curr+'.'+DOMAIN]

    with open('vars/value.yaml','w') as out_yaml:
        yaml.dump(val,out_yaml) 

    return val

# generate eds & lds function based on value.yaml & args
def generate_config(prev,curr,branch,svc_port):
    val = value_yaml(prev,curr,branch,svc_port)

    eds_template = open('templates/cds.yaml.j2').read()
    lds_template = open('templates/lds.yaml.j2').read()
    eds_config = jinja2.Template(eds_template).render(val)
    lds_config = jinja2.Template(lds_template).render(val)
    if status == 'new':
        open('yaml/cds.yaml', 'w+').write(eds_config)
        open('yaml/lds.yaml', 'w+').write(lds_config)
    else:
        open('yaml/cds-new.yaml', 'w+').write(eds_config)
        open('yaml/lds-new.yaml', 'w+').write(lds_config)
        
    print("Successfully Generate YAML for envoy-proxy")
generate_config(prev_sha,curr_sha,curr_branch,svc_port)