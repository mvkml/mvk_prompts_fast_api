from fastapi import APIRouter
from app.api.api_state.api_buffer_memory import router_buffer_memory

sub_base_router_state = APIRouter(prefix="/State",tags=["State"])
sub_base_router_state.include_router(router_buffer_memory, prefix="/buffer_memory")



