from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
import requests
from datetime import datetime

db_path = r"/Users/jijiyumo/Desktop/distributed/db.xml"
tree = ET.parse(db_path)
root = tree.getroot()

def add_note(topic_name, note_text):
    timestamp = datetime.now().strftime("%m/%d/%y - %H:%M:%S")
    found_topic = None
    for topic in root.findall('topic'):
        if topic.attrib['name'] == topic_name:
            found_topic = topic
            break
    if not found_topic:
        found_topic = ET.SubElement(root, 'topic', name=topic_name)
    
    note_name = f"{note_text[:20]} {timestamp.split(' ')[0]}"
    note = ET.SubElement(found_topic, 'note', name=note_name)
    ET.SubElement(note, 'text').text = note_text
    ET.SubElement(note, 'timestamp').text = timestamp
    
    tree.write(db_path)
    return f"Note '{note_name}' added to topic '{topic_name}'."

def get_notes(topic_name):
    for topic in root.findall('topic'):
        if topic.attrib['name'] == topic_name:
            return [f"Note: {note.attrib['name']}, Text: {note.find('text').text}, Timestamp: {note.find('timestamp').text}" for note in topic.findall('note')]
    return []

def add_wikipedia_info_to_topic(topic_name, wikipedia_url):
    found_topic = None
    for topic in root.findall('topic'):
        if topic.attrib['name'] == topic_name:
            found_topic = topic
            break
    if not found_topic:
        return "Topic not found."

    if not any(info.tag == "wikipedia" for info in found_topic):
        wiki_info = ET.SubElement(found_topic, 'wikipedia')
    else:
        wiki_info = found_topic.find('wikipedia')
    wiki_info.text = wikipedia_url
    
    tree.write(db_path)
    return f"Wikipedia info added to topic '{topic_name}'."

def query_wikipedia(topic):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": topic,
        "limit": 1,
        "namespace": 0,
        "format": "json"
    }
    response = requests.get(url, params=params).json()
    if response[3]:
        return response[3][0]  # URL of the first search result
    return "No Wikipedia article found."

server = SimpleXMLRPCServer(('localhost', 8000), allow_none=True)
print("Server listening on port 8000...")
server.register_function(add_note, 'add_note')
server.register_function(get_notes, 'get_notes')
server.register_function(query_wikipedia, 'query_wikipedia')
server.register_function(add_wikipedia_info_to_topic, 'add_wikipedia_info_to_topic')

server.serve_forever()
