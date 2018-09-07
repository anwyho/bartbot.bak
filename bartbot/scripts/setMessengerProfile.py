import logging

from typing import (List, Tuple)

from ..utils.requests import post
from ..utils.urls import MESSENGER_PROFILE_API


get_started_data = { 
    "get_started": {
        "payload":"Hello hello! Bartbot here. You can ask me about live schedules and weather [beta], or request a map I\'m constantly improving, so check back every now and then!"}}
greeting_data = {
    "greeting": [{
        "locale": "default",
        "text": "Hey {{user_first_name}}! Bartbot is here to " + \
            "help you with your BART needs. What is BART? " + \
            "Check out https://bart.gov/! " 
        }, {
        "locale": "en_US",
        "text": "A one-stop shop for all your BART needs, " + \
            "all on Messenger!" }]}
        # TODO: Support multiple locales
home_url_data = {
  "home_url" : {
     "url": "<URL_FOR_CHAT_EXTENSION>",
     "webview_height_ratio": "tall",
     "webview_share_button": "show",
     "in_test":False}}  # TODO: Set this to true in deployment
persistent_menu_data = {

}
target_audience_data = {"target_audience": { "audience_type":"all" }}
    # # Comment above and uncomment below to whitelist
    # "target_audience": { 
    #     "audience_type":"whitelist"
    #     "countries": {
    #     "whitelist": ["US", "CA"]}}}

def run_scripts(*scripts) -> List[str]:
    results = []
    for script in scripts:
        print(f"Running script {script}.")
        if script is 'get_started':
            results += get_started()[0]
        if script is 'greeting':
            results += greeting()[0]
        if script is 'home_url':
            results += home_url()[0]
        if script is 'persistent_menu':
            results += persistent_menu()[0]
        if script is 'target_audience':
            resultes += target_audience()[0]
    return results

def get_started() -> Tuple[bool,dict]:
    """Sets postback for Get Started"""
    logging.info("Setting Get Started")
    return post(MESSENGER_PROFILE_API, json=get_started_data)

def greeting() -> Tuple[bool,dict]:
    """Sets the greeting for the Get Started page"""
    logging.info("Setting greeting")
    return post(MESSENGER_PROFILE_API, json=greeting_data)

def home_url() -> Tuple[bool,dict]:
    """Sets the home URL of the bot"""
    logging.info("Setting home URL")
    return post(MESSENGER_PROFILE_API, json=home_url_data)

def persistent_menu() -> Tuple[bool,dict]:
    """Sets the style and elements of the persistent menu"""
    logging.info("Setting persistent menu")
    return post(MESSENGER_PROFILE_API, json=persistent_menu_data)

def target_audience() -> Tuple[bool,dict]:
    """Sets the audience that this bot is accessible to"""
    logging.info("Setting target audience")
    return post(MESSENGER_PROFILE_API, json=target_audience_data)



