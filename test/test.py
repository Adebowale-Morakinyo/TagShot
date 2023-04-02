images = {1: {'name': 'a', 'age': 12}, 2:{'name': 'b', 'age': 10}}

image_id = 2
tags_list = ['fun', 'app', 'sad']
tags = {'fun': [1], 'meme': [2]}

for tag in tags_list:
    if tag in tags:
        tags[tag].append(image_id)
    else:
        tags[tag] = [image_id]
        
print(tags)

tags["fun"].remove(1)
    
for tag in tags.values():
    print(tag)
