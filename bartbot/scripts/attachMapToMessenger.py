import json
import logging 
import os

from typing import Union

from ..utils.requests import post
from ..utils.urls import MESSAGE_ATTACHMENTS_API


BART_MAP_URL="https://github.com/anwyho/bart-map/blob/master/BART_cc_map.png?raw=true"
BART_MAP_FILE = os.path.join('bartbot', 'resources', 'images', 'bart_map_id.txt')

# HACK: Improve this function to work for any given attachment

def get_map_id(forceRefresh=False) -> Union[str,None]:
    """
    Saves attachment to FB for cached map. 
    Places attachment ID into 'bartbot/resources/images/bart_map_id.txt'.
    """

    mapId = ""
    if not forceRefresh: mapId = read_local()
    if mapId == "": mapId = post_from_git()
    if mapId != "": write_local(mapId)
    else: mapId = None  # Clearly not found

    return mapId
    

def read_local() -> str:
    """Tries to read attachment ID from file"""
    try:
        with open(BART_MAP_FILE, 'r') as f:
            mapId = f.read()
    except IOError as e:
        logging.error("Couldn't retreive attachment ID from file " +  
            f"{BART_MAP_FILE}. Error: {e}")
        mapId = ""
    if not mapId.isdigit():
        logging.error("Invalid attachment ID in file")
        logging.debug(f"mapId = {mapId}")
        mapId = ""
    else:
        logging.info("Successfully read in attachment ID")

    return mapId


def post_from_git() -> str:
    """Tries to POST url of original map to Messenger Attachments"""
    data = {
    "message": {
        "attachment": {
        "type": "image", 
        "payload": {
            "is_reusable": 'true',
            "url": BART_MAP_URL }}}}

    ok, resp = post(MESSAGE_ATTACHMENTS_API, json=data)
    if ok and 'attachment_id' in resp:
        return resp['attachment_id']
    else:
        logging.error("Couldn't retrieve attachment ID from Messenger")
        logging.debug(f"resp: {json.dumps(resp,indent=2)}")
        return ""


def write_local(mapId:str) -> bool:
    """Tries to cache attachment ID to a local file"""
    try: 
        with open(BART_MAP_FILE, 'w') as f:
            f.write(mapId)
        logging.info(f"Wrote map attachment ID to file {BART_MAP_FILE}")
        return True
    except Exception as e:
        logging.error("Couldn't write attachment ID to " +  
            f"file {BART_MAP_FILE}. Received error {e}.")
    return False



if __name__ == '__main__':
    get_map_id(forceRefresh=True)