from rest_framework import serializers
from .models import Event, Attendee, Sponsor, AgendaItem
from accounts.serializers import UserSerializer,UserSmallSerializer
from wish_and_offers.serializers import WishSmallSerializer, OfferSmallSerializer

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['id', 'name', 'logo', 'website']

class AgendaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendaItem
        fields = ['id', 'time', 'title', 'description', 'speaker','date']

class AttendeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Attendee
        fields = ['id', 'user', 'registration_date']

class AttendeeSmallSerializer(serializers.ModelSerializer):
    user = UserSmallSerializer(read_only=True)

    class Meta:
        model = Attendee
        fields = ['id', 'user']

class EventListSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    attendees_count = serializers.SerializerMethodField()
    

    class Meta:
        model = Event
        fields = ['id', 'title', 'start_date', 'end_date', 'location', 'organizer', 'attendees_count', 'thumbnail']

    def get_attendees_count(self, obj):
        return obj.attendees.count()

class EventDetailSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    attendees = AttendeeSmallSerializer(many=True, read_only=True)
    wishes = WishSmallSerializer(many=True, read_only=True)
    offers = OfferSmallSerializer(many=True, read_only=True)
    sponsors = SponsorSerializer(many=True, read_only=True)
    agenda_items = AgendaItemSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'location', 'organizer', 
                  'attendees', 'sponsors', 'agenda_items', 'created_at', 'updated_at', 'thumbnail','wishes','offers']