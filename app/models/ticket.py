from pydantic import BaseConfig, BaseModel, constr, UUID4
from typing import List, Optional
from datetime import datetime
from enum import Enum

class EventTypeEnum(str, Enum):
    created = 'tickerCreated'
    updated = 'ticketUpdated'
    closed = 'ticketClosed'

class EventStatusEnum(str, Enum):
    new = 'new'
    assigned = 'assigned'
    closed = 'closed'

class TicketComment(BaseModel):
    author: constr(max_length= 50)
    comment: constr(max_length= 1000)
    eventTime: datetime

class TicketEventData(BaseModel):
    assignee: constr(max_length=80) = ''
    comment: constr(max_length= 1000) = ''
    description: constr(max_length=5000)
    status : EventStatusEnum
    title: constr(max_length=200)

class TicketEvent(BaseModel):
    event: TicketEventData

    eventAuthor: constr(max_length= 50)
    eventTime: datetime
    eventType: EventTypeEnum
    eventId: UUID4
    ticketId: UUID4

class Ticket(BaseModel):
    assignee: Optional[constr(max_length=80)]
    description: constr(max_length=5000)
    status : EventStatusEnum
    title: constr(max_length=200)
    ticketId: UUID4

    comments: List[TicketComment] = []
    history: List[TicketEvent] = []




# class EventCreate(BaseModel):
#     eventAuthor: constr(max_length= 50)
#     eventTime: datetime
#     eventType: EventTypeEnum


class TicketCreate(BaseModel):
    author: constr(max_length= 50)
    description: constr(max_length=5000)
    status : str
    title: constr(max_length=200)

class TicketResponse(TicketCreate):
    ticketId: UUID4