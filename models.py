from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, text
from database import Base

class meeting_room(Base):
    __tablename__ = "meeting_room"

    id = Column(Integer, primary_key=True, index=True)
    conference_room_name = Column(String)
    no_of_seats = Column(Integer)
    is_Projector_or_TV_availability = Column(Boolean)
    locations = Column(String)
    active = Column(Boolean, default=None)
    added_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_updated_on= Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    # created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    # updated_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
