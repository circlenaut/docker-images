#!/usr/bin/python3

#@TODO
# - this is a placeholder

"""
Configure custom app service
"""

import os
import sys
import json
import bcrypt
import logging
import coloredlogs
import argparse
from urllib.parse import quote, urljoin
from subprocess   import run, call
from typing import Dict
import functions as func

### Enable logging
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s', 
    level=logging.INFO, 
    stream=sys.stdout)

log = logging.getLogger(__name__)

### Enable argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('--opts', type=json.loads, help='Set script arguments')
parser.add_argument('--env', type=json.loads, help='Set script environment')
parser.add_argument('--user', type=json.loads, help='Load user settings')

args, unknown = parser.parse_known_args()
if unknown:
    log.error("Unknown arguments " + str(unknown))

### Load arguments
cli_opts = args.opts
cli_env = args.env
cli_user = args.user

### Set log level
verbosity = cli_opts.get("verbosity")
log.setLevel(verbosity)
# Setup colored console logs
coloredlogs.install(fmt='%(asctime)s [%(levelname)s] %(message)s', level=verbosity, logger=log)

### Get envs
proxy_base_url = cli_env.get("PROXY_BASE_URL")
caddy_virtual_base_url = cli_env.get("CADDY_VIRTUAL_BASE_URL")

### Clean up envs
proxy_base_url = func.clean_url(proxy_base_url)
host_base_url = func.clean_url(caddy_virtual_base_url)
system_base_url = urljoin(host_base_url, proxy_base_url)

### Set workspace dirs
workspace_dir = os.path.normpath(cli_user.get("dirs").get("workspace").get("path"))
data_dir = os.path.normpath(cli_user.get("dirs").get("data").get("path"))

### Get user settings
user_name = cli_user.get("name")
user_group = cli_user.get("group")
user_password = cli_user.get("password")
user_home = cli_user.get("dirs").get("home").get("path")

def _config(app: Dict) -> Dict:
    apps_dir = os.path.normpath(cli_user.get("dirs").get("apps").get("path"))
    
    app_name = app.get("name")
    app_bind_addr = app.get("bind_addr")
    app_base_url = func.clean_url(app.get("base_url"))
    app_root_dir = app.get("root_dir") if app.get("root_dir") else os.path.join(apps_dir, app_name)
    app_username = app.get("user")
    app_password = app.get("password")
    
    ### Set final base url
    full_base_url = urljoin(system_base_url, app_base_url)
    application = app.get("name")
    log.info(f"{application} base URL: '{full_base_url}'")
    
    if not os.path.exists(app_root_dir): 
        os.makedirs(app_root_dir)
        log.warning(f"fixing permissions for '{user_name}' on '{app_root_dir}'")
        func.recursive_chown(apps_dir, user_name, user_group)
        
    config_dir = os.path.join(user_home, ".config", application)
    if not os.path.exists(config_dir):
        log.info(f"creating app config direcotry: '{config_dir}'")
        os.makedirs(config_dir)
        
    ### Generate password hash
    if not app_username == None:
        if not app_password == None: 
            password = app_password.encode()
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password, salt).decode('utf-8')
            log.info(f"{application} password: '{app_password}'")
            log.info(f"{application} hashed password: '{hashed_password}'")
        else:
            log.warning(f"{application} password not set for : '{app_username}'")
    else:
        log.warning(f"{application} user not set")

    ### Create config template
    config_file = {
        "admin": app_username,
        "logging": {},
        "name": application,
        "host": "localhost",
        "port": app_bind_addr.split(":",1)[1],
        "proto": "http",
        "base_url": full_base_url,
    }
    
    # Create symlink to workspace
    link_path = os.path.join(workspace_dir, os.path.basename(app_root_dir))
    if os.path.exists(app_root_dir) and not os.path.exists(link_path):
        log.info(f"symlinking '{app_root_dir}'' to '{link_path}'")
        os.symlink(app_root_dir, link_path)
        
    ### Write config file
    config_path = os.path.join(config_dir, "settings.json")
    config_json = json.dumps(config_file, indent = 4)
    
    with open(config_path, "w") as f: 
        f.write(config_json)
        
    # fix permissions
    log.info(f"setting permissions on '{config_dir}' to '{user_name}:{user_group}'")
    func.recursive_chown(config_dir, user_name, user_group)

    ### Display final config
    log.debug(f"{application} config: '{config_path}'")
    log.debug(func.capture_cmd_stdout(f'cat {config_path}', cli_env))

[_config(app) for app in cli_user.get("apps")]




