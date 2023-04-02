import uuid
from flask import Flask, request
from flask_smorest import abort
from db import screenshots, tags

app = Flask(__name__)


@app.get("/screenshots")
def get_screenshots():
    """Retrieve a list of all screenshots with associated tags and metadata.

    Returns:
        _type_: json
    """
    return {"screenshots": list(screenshots.values())}


@app.post("/screenshots")
def upload_screenshot():
    """Upload a new screenshot with associated tags and metadata.

    Returns:
        _type_: json
    """
    request_data = request.get_json()
    screenshot_id = uuid.uuid4().hex
    if (
        "file_path" not in request_data
        or "created_at" not in request_data
        or "tags" not in request_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'file_path', 'created_at', 'tags' are included in the JSON payload "
        )
        
    for screenshot in screenshots.values():
        if screenshot["file_path"] == request_data["file_path"]:
            abort(400, message="Screenshot already exist!")    
    
    # extract tags, store and map them with their respective tagshot
    tags_list = request_data["tags"]
    for tag in tags_list:
        if tag in tags:
            tags[tag].append(screenshot_id)
        else:
            tags[tag] = [screenshot_id]
            
    screenshot = {**request_data, "id": screenshot_id}
    screenshots[screenshot_id] = screenshot
    return screenshot, 201


@app.put("/screenshot/<string:screenshot_id>/tags")
def update_tags(screenshot_id):
    request_data = request.get_json()
    if "tags" not in request_data:
        abort(400, message="Bad request. Ensure 'tags' is in the JSON payload. ")
    tag_list = request_data["tags"]
        
    try:
        screenshot = screenshots[screenshot_id]
        for tag in tag_list:
            if tag not in screenshot["tags"]:
                screenshot["tags"].append(tag)
        
        # updating tag dictionary as well
        for tag in tag_list:
            if tag in tags:
                tags[tag].append(screenshot_id)
            else:
                tags[tag] = [screenshot_id]
                
        return screenshot
    except KeyError:
        abort(404, message="Screenshot not found.")
    

@app.get("/screenshots/<string:screenshot_id>")
def get_screenshot(screenshot_id):
    """Retrieve a specific screenshot with associated tags and metadata.

    Args:
        screenshot_id (_type_): int

    Returns:
        _type_: json
    """
    try:
        return screenshots[screenshot_id]
    except KeyError:
        abort(404, message="Screenshot not found")
        
        
@app.delete("/screenshots/<string:screenshot_id>")
def delete_tagshot(screenshot_id):
    try:
        screenshot = screenshots[screenshot_id]
        
        # deleting the screenshot
        del screenshot
        # cleaning up - removing from tags database
        tag_list = screenshot["tags"]
        for tag in tag_list:
            tags[tag].remove(screenshot_id)
        
        return {"message": "Deleted!!"}
    except KeyError:
        abort(404, message="Screenshot not found")
        
        
@app.get("/screenshots/tags")
def get_tags():
    """Retrieve a list of all tags and screenshots associated with each tag.

    Returns:
        _type_: json
    """
    return {"tags": tags}
        

@app.get("/screenshots/tags/<string:tag_name>/date/<string:date>")
def search_screenshot(tag_name, date):
    try:
        suspected_screenshots = tags[tag_name]
        
        for screenshot in screenshots.values():
            if screenshot["created_at"] == date and screenshot["id"] in suspected_screenshots:
                return screenshot
    except KeyError:
        abort(404, message="Tag not found.")            
        