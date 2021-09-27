# learn360 fabfile
import sys, os, boto3
from fabric.api import env, run, cd, local, prompt, sudo
from fabric.colors import red, green
from fabric.decorators import runs_once
from fabric.api import settings


if os.getenv('EC_DEP_KEY_PROD') or os.path.exists('learn360.pem'):
	env.user = 'ubuntu'
	env.key_filename = os.getenv('EC_DEP_KEY_PROD', 'learn360.pem')
else:
	env.use_ssh_config = True


def fetch_ec2_instances_from_aws():
	try:
		ec2 = boto3.resource('ec2', 'ap-south-1')
		running_instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name','Values': ['running']}])
		running_aws_public_ips = []
		for instance in running_instances:
			for tag in instance.tags:
				if 'Name'in tag['Key']:
					name = tag['Value']
					if name == 'Entrance360 Autoscale Group':
						running_aws_public_ips.append(instance.public_ip_address)
		return running_aws_public_ips
	except Exception as e:
		print("Not deploying on auto scaling grouping, credentials not provided. \nMake sure to full deploy if deploying on ASG")
		return []


roles = {
	'master': [
		'',
	],
	'staging': [
		'',
	],
	'lms': [
		''
	],
	'analytics': [
		''
	],
	'varnish':[
		''
	]
}

roles['master'] += fetch_ec2_instances_from_aws()

env.roledefs = roles
code_dir_master = '/home/ubuntu/main/learn360'


def prod():
	env.hosts = roles['master']
	env.code_dir =  code_dir_master

def staging():
	env.hosts = roles['staging']
	if os.getenv('EC_DEP_KEY_STAGING') or os.path.exists('learn360_staging.pem'):
		env.key_filename = os.getenv('EC_DEP_KEY_STAGING', 'learn360_staging.pem')
	env.code_dir = code_dir_master

def staging2():
	env.hosts = roles['staging']
	if os.getenv('EC_DEP_KEY_STAGING') or os.path.exists('learn360_staging.pem'):
		env.key_filename = os.getenv('EC_DEP_KEY_STAGING', 'learn360_staging.pem')
	env.code_dir = '/home/ubuntu/main/learn362'

def staging3():
	env.hosts = roles['staging']
	if os.getenv('EC_DEP_KEY_STAGING') or os.path.exists('learn360_staging.pem'):
		env.key_filename = os.getenv('EC_DEP_KEY_STAGING', 'learn360_staging.pem')
	env.code_dir = '/home/ubuntu/main/env3/projects/learn363'

def staging4():
	env.hosts = roles['staging']
	if os.getenv('EC_DEP_KEY_STAGING') or os.path.exists('learn360_staging.pem'):
		env.key_filename = os.getenv('EC_DEP_KEY_STAGING', 'learn360_staging.pem')
	env.code_dir = '/home/ubuntu/main/learn364'


def service(name, action):
	valid_names = ["es", "nginx", "redis-server", "celery", "gunicorn_learn360", "gunicorn_learn362", "gunicorn_learn363"]
	if name not in valid_names:
		sys.stderr.write("%s is not a valid name. Name must be any one of %s." % (name, ",".join(valid_names)))
		exit()

	valid_actions = ["start", "stop", "restart", "reload", "status"]
	if action not in valid_actions:
		sys.stderr.write("%s is not a valid action. Action must be any one of %s." % (action, ",".join(valid_actions)))
		exit()

	if name in ["celery", "gunicorn_learn360", "gunicorn_learn362", "gunicorn_learn363"]:
		run("sudo supervisorctl " + action + " " + name)
	else:
		if name == "es":
			daemon_name = "elasticsearch"
		else:
			daemon_name = name
		run("sudo service " + daemon_name + " " + action)


def deploy(collect_static='y', install_reqs='y', migrate='y', restart_nginx='n', restart_server='y', branch='master', fetch_branch='n'):

	collect_static = (collect_static == 'y')
	install_reqs = (install_reqs == 'y')
	migrate = (migrate == 'y')
	restart_server = (restart_server == 'y')
	restart_nginx = (restart_nginx == 'y')
	fetch_branch = (fetch_branch == 'y')

	if env.host_string in roles['master'] or env.host_string in roles['staging'] and branch=='master':
		if branch != 'master':
			sys.stderr.write('Only master can be deployed on prod server')
			exit()
		print(green("Deploying " + str(branch) + " on master"))

	elif env.host_string in roles['staging']:
		print(green("Deploying " + str(branch) + " on " + str(env)))

	else:
		sys.stderr.write('No server selected')
		exit()

	with cd(env.code_dir):
		print(green("Found Code Directory : " + str(env.code_dir)))
		if fetch_branch:
			print(green("Updating Branches.."))
			run("sudo git fetch --all")
		print(green("Fetching Branch.."))

		run("sudo git checkout -f")
		run("sudo git checkout {}".format(branch))

		if env.host_string in roles['master'] or env.host_string in roles['staging']:
			repo_url = "git@gitlab.entrance360.com:root/learn361.git {branch}".format(branch=branch)
			run("sudo su ubuntu -c 'git pull " + repo_url+" --no-edit'")
		else:
			sys.stderr.write('Select the correct deployment machine')
			exit()

		print(green("Deleting Pyc files.."))
		run("sudo find . -name '*.pyc' -delete")

		# #code to check migrations
		# num_migrations = run("python manage.py showmigrations --list | grep '\[ ] ' | wc -l")
		# if num_migrations and int(num_migrations) >0:
		#     print(green("We have pending migrations... migrating now"))
		#     migrate = True

		if install_reqs:
			print(green("Installing Requirements.."))
			if env.code_dir == '/home/ubuntu/main/env3/projects/learn363':
				run("/home/ubuntu/main/env3/bin/pip3 install -r requirements.txt")
			elif env.code_dir == '/home/ubuntu/main/learn362':
				run("sudo pip install -r old_requirements.txt")
			else:
				run("sudo pip install -r requirements.txt")

		if collect_static:
			print(green("Collecting Static Files.."))
			if env.code_dir == '/home/ubuntu/main/env3/projects/learn363':
				run("/home/ubuntu/main/env3/bin/python3 manage.py collectstatic --noinput -i ckeditor")
			else:
				run_collect_static()

		if migrate:
			print(green("Starting Migrations.."))
			if env.code_dir == '/home/ubuntu/main/env3/projects/learn363':
				run("/home/ubuntu/main/env3/bin/python3 manage.py migrate")
			else:
				run_migrate()
			print(green("Migrations done.."))

		if restart_server:
			print(green("Restarting Gunicorn and Celery.."))
			run("sudo supervisorctl restart all")

		if restart_nginx:
			print(green("Restarting nginx.."))
			run("sudo service nginx restart")

		print(green("Code Deployed Successfully :D"))


def exit():
	sys.stderr.write("\nAborting.\n")
	sys.exit(1)

@runs_once
def run_collect_static():
	run("sudo python manage.py collectstatic --noinput -i ckeditor")


@runs_once
def run_migrate():
	run("sudo python manage.py migrate")

#Restarts gunicorn
def kg():
	run("sudo supervisorctl restart gunicorn_learn360")

##################################################################################################################################

# Overview and Tutorial

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

local is used for local server
run is used for remote server

env.hosts = ['my_server']

def test():
	# This function is used for failure handling
    with settings(warn_only=True):
        result = local('./manage.py test my_app', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()

def deploy():
    code_dir = '/srv/django/myproject'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone user@vcshost:/path/to/repo/.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")

################################################################################################################################

The Environment Dictionary, env

Full List env vars

env.abort_exception() # Override the behaviour of printing error message
env.abort_on_prompts() # when True, forcing Fabric to abort whenever it would prompt for input.
env.all_hosts() # default = [], Set by fab to the full host list for the currently executing command. For informational purposes only.
env.always_use_pty() # default = True, When set to False, causes run/sudo to act as if they have been called with pty=False.
env.colorize_error() # default = False, When set to True, error output to the terminal is colored red and warnings are colored magenta to make them easier to see.
env.combine_stderr() # default = True
env.command() # default = None
env.command_prefixes()




















