from .models import Location, Note
import datetime

def import_data():
    Note.objects.all().delete()
    Location.objects.all().delete()
    date = None
    date_txt = None
    locations = []
    indent = 0


    location_map = {}
    for line in open("C:/Users/flat0/Dropbox/logs/climbing_outdoors_trunc.org").readlines():
        if line[0] == "*":
            date = line[3:3+10]
            locations = []
            date_txt = line[3:3+10]
            date = datetime.datetime.strptime(date,"%Y-%m-%d").date()
            indent = 0
        else:
            i = 0
            while line[i] == " ":
                i += 1
            if i >= indent:
                if i == indent and i != 0:
                    locations = locations[:-1]
                locations += [line[0:line.find("-")].strip()]
                location = None
                if locations[-1] in location_map:
                    location = location_map[locations[-1]]
                else:
                    parent_location = None
                    if len(locations) > 1:
                        parent_location = location_map[locations[-2]]
                    location = Location(
                        location_type = "area",
                        name = locations[-1],
                        parent_location = parent_location)
                    location_map[locations[-1]] = location
                    location.save()

                if "-" in line:
                    comment = line[line.find("-")+1:].strip()
                    note = Note(note_type="text",
                                content=comment,
                                location=location,
                                date=date)
                    note.save()


                indent = i
