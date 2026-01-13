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
from app.api.api_cpt.api_lc_cpt_02_fm import api_lc_cpt_02_fm_router
from app.api.api_cpt.api_lc_cpt_02_sthm import api_lc_cpt_02_sthm_router

from app.api.api_fspt.api_lc_fspt_01_ft import api_lc_fspt_01_ft_router
from app.api.api_fspt.api_lc_fspt_02_fcpt_mp_v2 import api_lc_fspt_mp_router 
from app.api.api_user.api_user import user_router

api_router = APIRouter()
api_router.include_router(api_pt_router, prefix="/api_pt")
api_router.include_router(api_lc_pt_fastapi, prefix="/api_lc_pt")
api_router.include_router(api_lc_pt_01_fastapi, prefix="/api_lc_pt_01")
api_router.include_router(api_lc_pt_02_fe_router, prefix="/api_lc_pt_02_fe")
api_router.include_router(api_lc_pt_04_ff_router, prefix="/api_lc_pt_04_ff")
api_router.include_router(api_lc_pt_03_ff_router, prefix="/api_lc_pt_03_ff")

api_router.include_router(api_lc_cpt_01_ft_router, prefix="/api_lc_cpt_01_ft")
api_router.include_router(api_lc_cpt_02_fm_router, prefix="/api_lc_cpt_02_fm")
api_router.include_router(api_lc_cpt_02_sthm_router, prefix="/api_lc_cpt_02_sthm")

api_router.include_router(api_lc_fspt_01_ft_router, prefix="/api_lc_fspt_01_ft")
api_router.include_router(api_lc_fspt_mp_router, prefix="/api_lc_fspt_02_fcpt_mp")

api_router.include_router(user_router, prefix="/api_user")


