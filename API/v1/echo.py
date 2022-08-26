from fastapi import APIRouter, Depends
from API.v1.auth import TokenValidator
from core.models.model import Message

router = APIRouter()
authenticate = TokenValidator()


@router.post("/", response_model=Message, dependencies=[Depends(authenticate)])
async def send_echo_message(incoming_message: Message) -> Message:
    """
    Send echo back to user.
    :param incoming_message: incoming message.
    :returns: message with Hello to the incoming.
    """
    incoming_message.message = f"Hello {incoming_message.message}"
    return incoming_message