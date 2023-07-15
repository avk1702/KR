from typing import Self


class Note:

    def __init__(self, id, title, text, created_date, updated_date):
       
       self.id = id
       self.title = title
       self.text = text
       self.created_date = created_date
       self.updated_date = updated_date

import json
from datetime import datetime


class Notes:
    def __init__(self):
        self.notes = []
    
    def addNote(self, title, text):
        id = len(self.notes) + 1
        created_date = datetime.now()
        updated_date  = datetime.now()
        self.notes.append(Note(id, title, text, created_date, updated_date ))

    def deleteNote(self, id):
        for note in self.notes:
            if note.id == id:
                self.notes.remove(note)

    def editNote(self, id, title, text):
        for note in self.notes:
            if note.id == id:
                note.title = title
                note.text = text
                note.updated_date = datetime.now()

    def readNote(self, id):
        for note in self.notes:
            if note.id == id:
                return note
            
    def saveNotes(self, filename):
        with open(filename, 'w') as outfile:
            data = {"notes": []}
            for note in self.notes:
                note_json = {
                    "id": note.id,
                    "title": note.title,
                    "text": note.text,
                    "created_date":note.created_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_date":note.updated_date.strftime("%Y-%m-%d %H:%M:%S")
                }
                data["notes"].append(note_json)
            
            json.dump(data, outfile)

    def loadNotes(self, filename):
        with open(filename) as infile:
            data = json.load(infile)
            notes = []
            for note_json in data["notes"]:
                id = note_json["id"]
                title = note_json["title"]
                text = note_json["text"]
                created_date = datetime.strptime(note_json["created_date"],"%Y-%m-%d %H:%M:%S")
                updated_date = datetime.strptime(note_json["updated_date"],"%Y-%m-%d %H:%M:%S")

                notes.append(id, title, text, created_date, updated_date)
            
            self.notes = notes

    def filtrationByDate(self, from_date, to_date):
        from_date = datetime.strptime(from_date, "%d.%m.%Y")
        to_date = datetime.strptime(to_date, "%d.%m.%Y")
        filtered_notes = []
        for note in self.notes:
            if from_date <= note.created_date <= to_date:
                filtered_notes.append(note)

        return filtered_notes
    
import argparse

notes = Notes()

parser = argparse.ArgumentParser(description='Notes application')

subparsers = parser.add_subparsers(dest='command')

add_parser = subparsers.add_parser('addNote', help='Add note')

add_parser.add_argument('-title', type=str, required=True, help='Title of note')

add_parser.add_argument('-text', type=str, required=True, help='Text of note')

delete_parser = subparsers.add_parser('deleteNote', help='Delete note')

delete_parser.add_argument('-id', type=int, required=True, help='ID of note to delete')

edit_parser = subparsers.add_parser('editNote', help='Edit note')

edit_parser.add_argument('-id', type=int, required=True, help='ID of note to edit')

edit_parser.add_argument('-title', type=str, required=True, help='New title of note')

edit_parser.add_argument('-text', type=str, required=True, help='New text of note')

read_parser = subparsers.add_parser('readNote', help='Read note')

read_parser.add_argument('-id', type=int, required=True, help='ID of note to read')

save_parser = subparsers.add_parser('saveNotes', help='Save notes to file')

save_parser.add_argument('-filename', type=str, required=True, help='Filename to save notes to')

load_parser = subparsers.add_parser('loadNotes', help='Load notes from file')

load_parser.add_argument('-filename', type=str, required=True, help='Filename to load notes from')

filtration_parser = subparsers.add_parser('filtrationByDate', help='Filter notes by date')

filtration_parser.add_argument('-from', type=str, required=True, help='Start date to filter notes(dd.mm.yyyy)')

filtration_parser.add_argument('-to', type=str, required=True, help='End date to filter notes(dd.mm.yyyy)')


args = parser.parse_args()

if args.command == 'addNote':
    notes.addNote(args.tile, args.text)

elif args.command == 'deleteNote':
    notes.deleteNote(args.id)

elif args.command == 'editNote':
    notes.editNote(args.id, args.title, args.text)

elif args.command == 'readNote':
    note = notes.readNote(args.id)
    print(note.title)
    print(note.text)

elif args.command == 'saveNotes':
    notes.saveNotes(args.filename)

elif args.command == 'loadNotes':
    notes.loadNotes(args.filename)

elif args.command == 'filtrationByDate':
    notes_filtered = notes.filtrationByDate(args.from_date, args.to_date)
    for note in notes_filtered:
        print(note.title)
        print(note.text)

  