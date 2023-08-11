from rest_framework import serializers
from django.utils import timezone

from quickcheck.models import Story, Job, Comment, Poll, PollOpt, Base


class StorySerializer(serializers.ModelSerializer):
    kids = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = "__all__"
        extra_kwargs = {
            "type": {"read_only": True},
            "score": {"read_only": True},
            "descendants": {"read_only": True},
            "title": {"required": True},
            "by": {"read_only": True},
            "time": {"read_only": True},
            "HN_id": {"read_only": True},
        }

    def get_kids(self, obj) -> list:
        # return [kid.HN_id for kid in obj.kids.all()]
        return [kid.HN_id if kid.HN_id else kid.id for kid in obj.kids.all()]
    
    def create(self, validated_data):
        by = self.context["request"].user.username
        story = Story.objects.create(**validated_data, type="story", by=by, time=timezone.now(), HN_id=None)
        return story


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        extra_kwargs = {
            "type": {"read_only": True},
            "title": {"required": True},
            "by": {"read_only": True},
            "time": {"read_only": True},
            "HN_id": {"read_only": True},
            "text": {"required": True},
            "url": {"required": False},
        }


class CommentSerializer(serializers.ModelSerializer):
    kids = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "type": {"read_only": True},
            "by": {"read_only": True},
            "time": {"read_only": True},
            "HN_id": {"read_only": True},
            "parent": {"required": True},
            "text": {"required": True},
        }
    
    def get_kids(self, obj):
        return [kid.HN_id for kid in obj.kids.all()]
    

    def validate(self, attrs):
        if attrs["parent"].type not in ["story", "comment"]:
            raise serializers.ValidationError({"parent": "Parent must be of type story or comment."})
        return attrs
    
    def create(self, validated_data):
        by = self.context["request"].user.username
        comment = Comment.objects.create(**validated_data, type="comment", by=by, time=timezone.now(), HN_id=None)
        return comment


class PollSerializer(serializers.ModelSerializer):
    parts = serializers.SerializerMethodField()

    def get_parts(self, obj):
        return [part.HN_id for part in obj.parts.all()]

    class Meta:
        model = Poll
        fields = "__all__"
        extra_kwargs = {
            "type": {"read_only": True},
            "score": {"read_only": True},
            "descendants": {"read_only": True},
            "title": {"required": True},
            "by": {"read_only": True},
            "time": {"read_only": True},
            "HN_id": {"read_only": True},
            "text": {"required": True},
        }
    
    def create(self, validated_data):
        by = self.context["request"].user.username
        poll = Poll.objects.create(**validated_data, type="poll", by=by, time=timezone.now(), HN_id=None)
        return poll


class PollOptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOpt
        fields = "__all__"
        extra_kwargs = {
            "type": {"read_only": True},
            "by": {"read_only": True},
            "time": {"read_only": True},
            "HN_id": {"read_only": True},
            "parent": {"required": True},
            "score": {"read_only": True},
        }
    
    def validate(self, attrs):
        if attrs["parent"].type != "poll":
            raise serializers.ValidationError({"parent": "Parent must be of type poll."})
        return attrs
    
    def create(self, validated_data):
        by = self.context["request"].user.username
        poll_opt = PollOpt.objects.create(**validated_data, type="pollopt", by=by, time=timezone.now(), HN_id=None)
        return poll_opt


class AllItemsSerializer(serializers.ModelSerializer):
    """
    Serializer for all types ofitems. Makes it possible
    to return dynamic fields based on the type of the item.
    """

    text = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    descendants = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()
    kids = serializers.SerializerMethodField()
    parts = serializers.SerializerMethodField()

    class Meta:
        model = Base
        fields = "__all__"

    def get_text(self, obj):
        if obj.type == "job":
            return obj.job.text
        elif obj.type == "comment":
            return obj.comment.text
        elif obj.type == "poll":
            return obj.poll.text
    
    def get_title(self, obj):
        if obj.type == "story":
            return obj.story.title
        elif obj.type == "job":
            return obj.job.title
        elif obj.type == "poll":
            return obj.poll.title
    
    def get_url(self, obj):
        if obj.type == "story":
            return obj.story.url
        elif obj.type == "job":
            return obj.job.url
    
    def get_score(self, obj):
        if obj.type == "story":
            return obj.story.score
        elif obj.type == "poll":
            return obj.poll.score
        elif obj.type == "poll_opt":
            return obj.poll_opt.score
    
    def get_descendants(self, obj):
        if obj.type == "story":
            return obj.story.descendants
        elif obj.type == "poll":
            return obj.poll.descendants
    
    def get_parent(self, obj):
        if obj.type == "comment":
            return obj.comment.parent
        elif obj.type == "poll_opt":
            return obj.poll_opt.parent
    
    def get_kids(self, obj):
        if obj.type == "comment":
            return obj.comment.kids
        elif obj.type == "story":
            return obj.story.kids
    
    def get_parts(self, obj):
        if obj.type == "poll":
            return obj.poll.parts


    def to_representation(self, instance):
        instance = super().to_representation(instance)
        
        if instance["type"] == "job":
            fields_to_remove = ["score", "descendants", "parent", "kids", "parts"]

        elif instance["type"] == "story":
            instance["kids"] = [kid.HN_id if kid.HN_id else kid.id for kid in instance["kids"].all()]
            fields_to_remove = ["text", "parent", "parts"]

        elif instance["type"] == "comment":
            instance["kids"] = [kid.HN_id if kid.HN_id else kid.id for kid in instance["kids"].all()]
            if instance["parent"] is not None:
                instance["parent"] = instance["parent"].HN_id if instance["parent"].HN_id else instance["parent"].id
            fields_to_remove = ["title", "url", "score", "descendants", "parts"]

        elif instance["type"] == "poll":
            instance["parts"] = [part.HN_id if part.HN_id else part.id for part in instance["parts"].all()]
            fields_to_remove = ["parent", "kids", "url"]

        elif instance["type"] == "pollopt":
            if instance["parent"] is not None:
                instance["parent"] = instance["parent"].HN_id if instance["parent"].HN_id else instance["parent"].id
            fields_to_remove = ["text", "title", "url", "descendants", "kids"]

        else:
            fields_to_remove = []
        
        for field in fields_to_remove:
            del instance[field]
            
        return instance
