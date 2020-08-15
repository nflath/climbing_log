from django.shortcuts import render
from django.http import HttpResponse
from .models import Location, Note
import logging
import collections
from .import_data import import_data

class SimpleLocation:
    def __init__(self):
        self.name = None
        self.children = []
        self.parent = None
        self.notes = []

def process_notes_for_date(notes_for_date):
    locations_for_date = collections.defaultdict(lambda: SimpleLocation())
    root_locations_for_date = set()
    for n in notes_for_date:
        simple_location = locations_for_date[n.location]
        simple_location.name = n.location.name
        simple_location.notes += [n]

        location = n.location
        while location.parent_location:
            parent_simple_location = locations_for_date[location.parent_location]
            parent_simple_location.name = location.parent_location.name

            if simple_location not in parent_simple_location.children:
                parent_simple_location.children += [simple_location]
            simple_location.parent = parent_simple_location

            location = location.parent_location
            simple_location = simple_location.parent

        locations_for_date[location].name = location.name

        root_locations_for_date.add(simple_location)

        print (n.date, root_locations_for_date)

    return (n.date, root_locations_for_date)

def log_by_date(request):
    print('log_by_date')
    notes = Note.objects.all().order_by('date').reverse()
    import_data()

    notes_for_date = []
    notes_collected = []

    for note in notes:
        if not notes_for_date or notes_for_date[0].date == note.date:
            notes_for_date += [note]
        else:
            notes_collected += [process_notes_for_date(notes_for_date)]
            notes_for_date = [note]
    notes_collected += [process_notes_for_date(notes_for_date)]

    for l in notes_collected:
        print(l[0])

    print(notes_collected[0])
    context = {'notes' : notes,
               'notes_collected': notes_collected}

    return render(request, "date.html", context)

def log_by_location(request,location_id = None):
    print ('log_by_location', location_id)
    locations = []
    notes = {}
    root_locations = Location.objects.filter(parent_location=None)
    if not location_id:
        locations = root_locations
        print(locations[0])
    else:
        locations = Location.objects.filter(id=location_id)

    for location in root_locations:
        notes[location.id] = Note.objects.filter(location_id=location.id)
        for child_location in location.child_location.get_queryset():
            notes[child_location.id] = Note.objects.filter(location_id=child_location.id)
    print(notes)
    context = {'locations' : locations,
               'root_locations' : root_locations,
               'current_location' : locations[0],
               'notes' : notes}

    return render(request, "location_list.html", context)

def location_list(request):
    return log_by_location(request, None)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.
