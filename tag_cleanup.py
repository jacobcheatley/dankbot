from cogs.utils import database
from sys import argv
import asyncio
import os

threshold = int(argv[1])

tags_db = database.Database('tags.json')
tags_dict = tags_db.all()
new_db = database.Database('tags-new.json')

async def do_things():
    for tag_name, tag_info in tags_dict.items():
        if tag_info['uses'] > threshold:
            await new_db.put(tag_name, tag_info)

        await new_db.save()


loop = asyncio.get_event_loop()
loop.run_until_complete(do_things())
os.remove('tags.json')
os.rename('tags-new.json', 'tags.json')
