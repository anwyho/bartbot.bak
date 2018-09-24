import json
import logging 
import os

from typing import Optional

from ..utils.requests import post
from ..utils.urls import MESSAGE_ATTACHMENTS_API


BART_MAP_URL="https://github.com/anwyho/bart-map/blob/master/BART_cc_map.png?raw=true"
BART_MAP_FILE = os.path.join('bartbot', 'resources', 'images', 'bart_map_id.txt')

# HACK: Improve this function to work for any given attachment

def get_map_id(forceRefresh=False, writeCache=BART_MAP_FILE) -> Optional[str]:
    """
    Saves attachment to FB for cached map. 
    Places attachment ID into 'bartbot/resources/images/bart_map_id.txt'.
    """

    mapId = None
    
    if not forceRefresh: 
        mapId = read_local()

    # Upload attachment from GitHub URL
    if mapId is None:  
        mapId = post_from_url()
        if mapId is not None: 
            write_local(mapId)

    # TODO: Upload attachment from S3 Bucket
    if mapId is None:
        mapId = post_from_S3()

    return mapId
    

def read_local() -> Optional[str]:
    """Tries to read attachment ID from file"""
    try:
        with open(BART_MAP_FILE, 'r') as f:
            mapId = f.read()

    except IOError as e:
        logging.warning("Couldn't retreive attachment ID from file " +  
            f"{BART_MAP_FILE}. Error: {e}")
        mapId = None

    else:
        if mapId.isdigit():
            logging.info("Successfully read in attachment ID")
        else:
            logging.warning("Invalid attachment ID in file")
            logging.debug(f"mapId = {mapId}")
            mapId = None
            
    finally: 
        return mapId


def post_from_url() -> Optional[str]:
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
        logging.warning("Couldn't retrieve attachment ID from Messenger")
        logging.debug(f"resp: {json.dumps(resp,indent=2)}")
        return None


def write_local(mapId:str) -> bool:
    """Tries to cache attachment ID to a local file"""
    try: 
        with open(BART_MAP_FILE, 'w') as f:
            f.write(mapId)
    except Exception as e:
        logging.warning("Couldn't write attachment ID to " +  
            f"file {BART_MAP_FILE}. Received error {e}.")
        return False
    else: 
        logging.info(f"Wrote map attachment ID to file {BART_MAP_FILE}")
        return True


def post_from_S3() -> Optional[str]:
    # TODO: Not implemented
    return None



if __name__ == '__main__':
    get_map_id(forceRefresh=True)