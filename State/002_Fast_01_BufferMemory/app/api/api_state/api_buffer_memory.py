from fastapi import APIRouter

router_buffer_memory = APIRouter() 


@router_buffer_memory.get("/")
async def get_default():
    return {"message": "Default response from buffer memory"}





