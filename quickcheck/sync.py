import datetime

import requests
from django.conf import settings
from django.utils import timezone

from quickcheck.models import Story, Job, Comment, Poll, PollOpt, Base


def sync_data():
    """
    Syncs the data from Hacker News API to the database.
    """
    # Get the latest item ID from Hacker News API
    max_id = requests.get(f"{settings.HACKER_NEWS_API_URL}/maxitem.json").json()
    
    # Get the latest item ID from the database or start from the latest 100 items
    last_synced_item = Base.objects.exclude(HN_id=None).order_by("-HN_id").first()
    last_synced_item_id = last_synced_item.HN_id if last_synced_item else max_id - 100
    print("=================LAST SYNCED ITEM=================", last_synced_item_id)

    # Sync from last synced to latest item in HN
    for index in range(last_synced_item_id + 1, max_id + 1):
        print(f"Getting item {index}...")
        item = requests.get(f"{settings.HACKER_NEWS_API_URL}/item/{index}.json").json()

        if item is None: continue

        elif item["type"] == "job":
            Job.objects.create(
                HN_id=item["id"],
                type=item["type"],
                by=item.get("by"),
                time=timezone.make_aware(datetime.datetime.fromtimestamp(item.get("time"))),
                deleted=item.get("deleted", False),
                dead=item.get("dead", False),
                text=item.get("text"),
                title=item.get("title"),
                url=item.get("url"),
            )
        elif item["type"] == "story":
            Story.objects.create(
                HN_id=item["id"],
                type=item["type"],
                by=item.get("by"),
                time=timezone.make_aware(datetime.datetime.fromtimestamp(item.get("time"))),
                deleted=item.get("deleted", False),
                dead=item.get("dead", False),
                descendants=item.get("descendants"),
                score=item.get("score"),
                title=item.get("title"),
                url=item.get("url"),
            )
        elif item["type"] == "comment":
            if item.get("parent"):
                parent = Base.objects.filter(HN_id=item["parent"]).first()

            Comment.objects.create(
                HN_id=item["id"],
                type=item["type"],
                by=item.get("by"),
                time=timezone.make_aware(datetime.datetime.fromtimestamp(item.get("time"))),
                deleted=item.get("deleted", False),
                dead=item.get("dead", False),
                parent=parent,
                text=item.get("text"),
            )
        elif item["type"] == "poll":
            Poll.objects.create(
                HN_id=item["id"],
                type=item["type"],
                by=item.get("by"),
                time=timezone.make_aware(datetime.datetime.fromtimestamp(item.get("time"))),
                deleted=item.get("deleted", False),
                dead=item.get("dead", False),
                descendants=item.get("descendants"),
                score=item.get("score"),
                title=item.get("title"),
                text=item.get("text"),
            )
        elif item["type"] == "pollopt":
            if item.get("parent"):
                parent = Poll.objects.filter(HN_id=item["parent"]).first()

            PollOpt.objects.create(
                HN_id=item["id"],
                type=item["type"],
                by=item.get("by"),
                time=timezone.make_aware(datetime.datetime.fromtimestamp(item.get("time"))),
                deleted=item.get("deleted", False),
                dead=item.get("dead", False),
                parent=parent,
                score=item.get("score"),
            )
    
    print("=====================Syncing Done=====================")
