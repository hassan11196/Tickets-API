from pydantic import BaseConfig, BaseModel, constr, UUID4
from typing import List, Optional
from datetime import datetime
from enum import Enum

class EventTypeEnum(str, Enum):
    created = 'ticketCreated'
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
    assignee: Optional[constr(max_length=80)] 
    comment:Optional[ constr(max_length= 1000)]
    description: Optional[constr(max_length=5000)]
    status : Optional[EventStatusEnum]
    title: Optional[constr(max_length=200)]

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


class TicketCreateRequest(BaseModel):
    author: constr(max_length= 50)
    description: constr(max_length=5000)
    status : EventStatusEnum = 'new'
    title: constr(max_length=200)

class TicketCreateResponse(TicketCreateRequest):
    ticketId: UUID4


class TicketUpdateRequest(BaseModel):
    author: Optional[constr(max_length= 50)]
    description: Optional[constr(max_length=5000)]
    status : Optional[EventStatusEnum] = 'assigned'
    title: Optional[constr(max_length=200)]
    comment:Optional[ constr(max_length= 1000)]
    assignee: Optional[constr(max_length=80)] 

class TicketUpdateResponse(TicketCreateRequest):
    ticketId: UUID4

class ManyTicketsResponse(BaseModel):
    tickets: List[Ticket]