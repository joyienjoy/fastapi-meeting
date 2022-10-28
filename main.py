from typing import Optional
import uvicorn
from fastapi import FastAPI, Depends
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from responses import Response

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        print(e)
    finally:
        db.close()


class meeting_room(BaseModel):
    conference_room_name : str
    no_of_seats : int = Field(gt=0, lt=51, description="The capacity must be between 1-50")
    is_Projector_or_TV_availability : bool
    locations : Optional[str]
    active : bool

@app.get("/")
async def read_all_meeting_room(db: Session = Depends(get_db)):
    try:
        data=db.query(models.meeting_room).all()
        if data is not None:
            return Response(data, 'Meeting Rooms retrieved successfully', False)
        return Response('meeting Room does not exist', 'Response Failed', True)

    except Exception as e:
        print(e)


@app.get("/meeting_room/{meetingroom_id}")
async def read_meeting_room_by_id(meeting_room_id: int, db: Session = Depends(get_db)):
    if meeting_room_id <= 0:
        return Response('Invalid meeting room id', 'Response Failed', True)
    try:
        data = db.query(models.meeting_room) \
            .filter(models.meeting_room.id == meeting_room_id) \
            .first()
    except Exception as e:
        print(e)
    if data is not None:
        return Response(data, f'Meeting Rooms retrieved successfully',False)
    return Response('The Meeting Room does not exist', 'Response Failed', True)


@app.get("/get_available_meetingrooms")
async def read_availability_meeting_room(meeting_room_availability: bool,db: Session = Depends(get_db)):
    try:
        data = db.query(models.meeting_room) \
            .filter(models.meeting_room.active == meeting_room_availability) \
            .all()
    except Exception as e:
        print(e)
    if data is not None:
        return Response(data, f'Meeting Rooms retrieved successfully', False)
    return Response('The Meeting Room does not exist','Response Failed',True)

@app.post("/")
async def create_meeting_room(meeting_room: meeting_room, db: Session = Depends(get_db)):
    try:
        meeting_room_model = models.meeting_room()
        meeting_room_model.conference_room_name = meeting_room.conference_room_name
        meeting_room_model.no_of_seats = meeting_room.no_of_seats
        meeting_room_model.is_Projector_or_TV_availability = meeting_room.is_Projector_or_TV_availability
        meeting_room_model.locations = meeting_room.locations
        meeting_room_model.active = meeting_room.active

        db.add(meeting_room_model)
        db.commit()
    except Exception as e:
        print(e)
    return Response(f'New meeting room with name {meeting_room_model.conference_room_name} is get added',
                    'Meeting Room added successfully', False)

@app.put('/{meetingroom_id}')
async def update_meeting_room(meeting_room_id:int, meeting_room: meeting_room,db:Session = Depends(get_db)):
    if meeting_room_id <= 0:
        return Response('Invalid meeting room id', 'Response Failed', True)
    try:
        meeting_room_model= db.query(models.meeting_room)\
            .filter(models.meeting_room.id == meeting_room_id)\
            .first()
    except Exception as e:
        print(e)

    if meeting_room_model is None:
        return Response(f'No Meeting Room found with this id : {meeting_room_id}', 'Meeting Room not updated', True)


    meeting_room_model.conference_room_name = meeting_room.conference_room_name
    meeting_room_model.no_of_seats = meeting_room.no_of_seats
    meeting_room_model.is_Projector_or_TV_availability = meeting_room.is_Projector_or_TV_availability
    meeting_room_model.locations = meeting_room.locations
    meeting_room_model.active = meeting_room.active

    db.add(meeting_room_model)
    db.commit()
    print(meeting_room_model)
    return Response(f'New meeting room with id : {meeting_room_id} is get updated',
                    'Meeting Room updated successfully', False)

@app.delete("/{meetingroom_id}")
async def delete_meeting_room(meeting_room_id: int, db: Session = Depends(get_db)):
    if meeting_room_id <= 0:
        return Response('Invalid meeting room id', 'Response Failed', True)
    try:
        data=meeting_room_model = db.query(models.meeting_room) \
            .filter(models.meeting_room.id == meeting_room_id) \
            .first()
    except Exception as e:
        print(e)
    if meeting_room_model is None:
        return Response(f'No Meeting room found with this id : {meeting_room_id}','Meeting room not deleted', True)

    db.query(models.meeting_room) \
        .filter(models.meeting_room.id == meeting_room_id) \
        .delete()

    db.commit()
    return Response(data, f'Meeting Room {meeting_room_id} deleted successfully', False)


@app.put('/room/{meetingroom_id}')
async def release_meeting_room(meeting_room_id:int,db:Session = Depends(get_db)):
        if meeting_room_id <= 0:
            return Response('Invalid meeting room id','Response Failed',True)

        try:
            meeting_room_model= db.query(models.meeting_room)\
                .filter(models.meeting_room.id == meeting_room_id)\
                .first()
        except Exception as e:
            print(e)

        if meeting_room_model is not None:
            if meeting_room_model.active is False:
                meeting_room_model.active= True
                db.add(meeting_room_model)
                db.commit()
                return Response(f'Meeting room with id {meeting_room_id} is get free', 'Meeting Room update successful', False)
            if meeting_room_model.active is True:
                return Response('This meeting room is already free','Response Failed',True)
            return Response('Meeting room does not exist','Response Failed',True)
        return Response('Meeting room does not exist','Response Failed',True)

@app.post('/meetingroom/{meetingroom_id}')
async def book_meeting_room(meeting_room_id:int,db:Session = Depends(get_db)):

        if meeting_room_id <= 0:
            return Response('Invalid meeting room id', 'Response Failed', True)
        try:
            meeting_room_model= db.query(models.meeting_room)\
                .filter(models.meeting_room.id == meeting_room_id)\
                .first()
        except Exception as e:
            print(e)

        if meeting_room_model is not None:
            if meeting_room_model.active is True:
                meeting_room_model.active= False
                db.add(meeting_room_model)
                db.commit()
                return Response(f'Meeting room with id {meeting_room_id} is get booked',
                                'Meeting Room update successful', False)
            if meeting_room_model.active is False:
                return Response('This meeting room is already booked', 'Response Failed', True)
            return Response('Meeting room does not exist', 'Response Failed', True)
        return Response('Meeting room does not exist', 'Response Failed', True)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="error", reload = True)
    print("running")
