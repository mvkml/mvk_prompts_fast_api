from fastapi import APIRouter
"""
This module defines the main API router for the application.
It imports the FastAPI APIRouter and includes the `api_pt_router` from the Portuguese API module
under the `/api_pt` prefix. This allows all endpoints defined in `api_pt_router` to be accessible
under the `/api_pt` path.
Attributes:
    api_router (APIRouter): The main API router that includes sub-routers for different API sections.
"""
from app.api.api_pt.api_pt import api_pt_router
from app.api.api_pt.api_lc_pt import api_lc_pt_fastapi
from app.api.api_pt.api_lc_pt_01_ft import api_lc_pt_01_fastapi
from app.api.api_pt.api_lc_pt_02_fe import api_lc_pt_02_fe_router
from app.api.api_pt.api_lc_pt_03_ff import api_lc_pt_03_ff_router
from app.api.api_pt.api_lc_pt_04_ff import api_lc_pt_04_ff_router

from app.api.api_cpt.api_lc_cpt_01_ft import api_lc_cpt_01_ft_router


api_router = APIRouter()
api_router.include_router(api_pt_router, prefix="/api_pt")
api_router.include_router(api_lc_pt_fastapi, prefix="/api_lc_pt")
api_router.include_router(api_lc_pt_01_fastapi, prefix="/api_lc_pt_01")
api_router.include_router(api_lc_pt_02_fe_router, prefix="/api_lc_pt_02_fe")
api_router.include_router(api_lc_pt_04_ff_router, prefix="/api_lc_pt_04_ff")
api_router.include_router(api_lc_pt_03_ff_router, prefix="/api_lc_pt_03_ff")
api_router.include_router(api_lc_cpt_01_ft_router, prefix="/api_lc_cpt_01_ft")



