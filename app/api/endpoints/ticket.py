
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Body, Depends, Path, Query
from slugify import slugify
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
import uuid

from ...models.ticket import TicketResponse, TicketCreate, Ticket, TicketEvent, TicketEventData
from ...db.mongodb import AsyncIOMotorClient, get_database
from ...core.config import database_name, ticket_collection_name
router = APIRouter()

@router.post(
    "/tickets",
    response_model=TicketResponse,
    tags=["tickets"],
    status_code=HTTP_201_CREATED,
)
async def create_new_ticket(
        new_ticket_data: TicketCreate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
):

    ticket_dict = new_ticket_data.dict()
    ticket_dict['ticketId'] = uuid.uuid4()

    if new_ticket_data.status != 'new':
        return 'Error'

    ticket = Ticket(
        description = new_ticket_data.description,
        title = new_ticket_data.title,
        status = new_ticket_data.status,
        ticketId= ticket_dict['ticketId']
    )

    ticket.history.append(
        TicketEvent(
            event = TicketEventData(**ticket_dict),
            eventAuthor =  new_ticket_data.author,
            eventTime = datetime.now(),
            eventType = 'tickerCreated',
            eventId = uuid.uuid4(),
            ticketId= ticket_dict['ticketId'] 
        )
    )



    print(ticket.dict())

    await db[database_name][ticket_collection_name].insert_one(ticket.dict())

    return TicketResponse(**ticket_dict)