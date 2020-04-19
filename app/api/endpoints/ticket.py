
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
    HTTP_200_OK
)
import uuid
from uuid import UUID
from ...models.ticket import TicketCreateResponse, TicketCreate, Ticket, TicketEvent, TicketEventData
from ...db.mongodb import AsyncIOMotorClient, get_database
from ...core.config import database_name, ticket_collection_name
from ...core.utils import create_aliased_response
router = APIRouter()

@router.post(
    "/tickets",
    response_model=TicketCreateResponse,
    tags=["tickets"],
    status_code=HTTP_201_CREATED,
)
async def create_new_ticket(
        new_ticket: TicketCreate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
):

    try:
        ticket_dict = new_ticket.dict()
        ticket_dict['ticketId'] = uuid.uuid4()

        if new_ticket.status != 'new':
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Input Validation failed"
            )

        ticket = Ticket(
            description = new_ticket.description,
            title = new_ticket.title,
            status = new_ticket.status,
            ticketId= ticket_dict['ticketId']
        )

        ticket.history.append(
            TicketEvent(
                event = TicketEventData(**ticket_dict),
                eventAuthor =  new_ticket.author,
                eventTime = datetime.now(),
                eventType = 'tickerCreated',
                eventId = uuid.uuid4(),
                ticketId= ticket_dict['ticketId'] 
            )
        )



        print(ticket.dict())

        await db[database_name][ticket_collection_name].insert_one(ticket.dict())

        return create_aliased_response(TicketCreateResponse(**ticket_dict))
    except:
        raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Input Validation failed"
            )


@router.get(
    "/tickets/{ticketId}",
    response_model=Ticket,
    tags=["tickets"],
    status_code=HTTP_200_OK,
)
async def get_ticket_by_ticketId(
        ticketId:  str = Path(..., min_length=1),
        db: AsyncIOMotorClient = Depends(get_database),
):
    print(ticketId)
    ticket = await db[database_name][ticket_collection_name].find_one({'ticketId': UUID(ticketId)})

    
    if not ticket :
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"ticket with TicketId '{ticketId}' not found",
        )

    return create_aliased_response(Ticket(**ticket))


    