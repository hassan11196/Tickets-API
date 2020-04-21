
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Body, Depends, Path, Query
from slugify import slugify
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_200_OK
)
from pydantic import constr
import uuid
from uuid import UUID
from ...models.ticket import TicketCreateResponse, EventTypeEnum, ManyTicketsResponse,EventStatusEnum, TicketCreateRequest, Ticket, TicketEvent, TicketEventData,TicketUpdateRequest, TicketUpdateResponse, TicketComment
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
        new_ticket: TicketCreateRequest = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
):

    try:
        ticket_dict = new_ticket.dict()
        ticket_dict['ticketId'] = uuid.uuid4()

        if new_ticket.status != EventStatusEnum.new:
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
                eventType = EventTypeEnum.created,
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

@router.get(
    "/tickets",
    response_model=ManyTicketsResponse,
    tags=["tickets"],
    status_code=HTTP_200_OK,
)
async def get_tickets(
        status: Optional[EventStatusEnum] = None,
        limit: Optional[int] = 0,
        offset: Optional[int] = 0,
        assignee: Optional[constr(max_length=80)] = None,
        db: AsyncIOMotorClient = Depends(get_database),
):
    tickets: ManyTicketsResponse = []
    
    print('check if assignee or status params are present')
    if assignee == None and status == None:
        ticket_docs = db[database_name][ticket_collection_name].find({} ,limit = limit, skip= offset)
    elif assignee and status:
        ticket_docs = db[database_name][ticket_collection_name].find({'assignee':assignee, 'status':status} ,limit = limit, skip= offset)
    elif status:
        ticket_docs = db[database_name][ticket_collection_name].find({'status':status} ,limit = limit, skip= offset)
    elif assignee:
        ticket_docs = db[database_name][ticket_collection_name].find({'assignee':assignee} ,limit = limit, skip= offset)


    print('Convert Dict objects retreived from db to Tickets Object')
    async for ticket in ticket_docs:
        print(type(ticket))
        tickets.append(
            Ticket(
                **ticket
            )
        )
    print(tickets)

    return create_aliased_response(ManyTicketsResponse(tickets = tickets))

    
@router.patch("/tickets/{ticketId}", response_model=Ticket, tags=["tickets"])
async def update_ticket(
        ticketId:  str = Path(..., min_length=1),
        ticket_update: TicketUpdateRequest = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
):


    print(ticketId)
    ticket = await db[database_name][ticket_collection_name].find_one({'ticketId': UUID(ticketId)})

    
    if not ticket :
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"ticket with TicketId '{ticketId}' not found",
        )

    if ticket_update.status == EventStatusEnum.closed:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=f"ticket with TicketId '{ticketId}' is closed",
        )

    if ticket_update.assignee is not None:
        print(ticket_update.status)
        if ticket_update.status is not EventStatusEnum.assigned:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT,
                detail=f"ticket assigne provided but ticket status assigned is not provided",
            )
    if ticket_update.status is EventStatusEnum.assigned:
        if ticket_update.assignee is None:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT,
                detail=f"ticket status assigned is provided but ticket assignee is not provided",
            )
    if ticket_update.author is None:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=f"Please Provide Ticket Update Author",
        )

    ticket = Ticket(**ticket)

    print('Check if description')
    if ticket_update.description:
        ticket.description = ticket_update.description
    print('Check if status')
    if ticket_update.status:
        ticket.status = ticket_update.status
    print('Check if title')
    if ticket_update.title:
        ticket.title = ticket_update.title
    print('Check if comment')
    if ticket_update.comment:
        ticket.comments.append(
            TicketComment(
                author = ticket_update.author,
                eventTime = datetime.now(),
                comment = ticket_update.comment
            )
        )
    print('Check if assignee')
    if ticket_update.assignee:
        ticket.assignee = ticket_update.assignee
    print('Add to History')  
    ticket.history.append(
            TicketEvent(
                event = TicketEventData(**ticket_update.dict()),
                eventAuthor =  ticket_update.author,
                eventTime = datetime.now(),
                eventType = EventTypeEnum.closed if ticket_update.status == EventStatusEnum.closed else EventTypeEnum.updated,
                eventId = uuid.uuid4(),
                ticketId= ticketId
            )
        )

    await db[database_name][ticket_collection_name].replace_one({'ticketId': UUID(ticketId)}, ticket.dict())
    
    # print(ticket_update)
    return create_aliased_response(TicketUpdateResponse({**ticket_update.dict(), 'ticketId':ticketId }))
