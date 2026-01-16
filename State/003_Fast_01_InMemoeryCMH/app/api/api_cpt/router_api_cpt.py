from fastapi import APIRouter

from app.api.api_cpt.api_lc_cpt_01_ft import api_lc_cpt_01_ft_router
from app.api.api_cpt.api_lc_cpt_02_fm import api_lc_cpt_02_fm_router
from app.api.api_cpt.api_lc_cpt_02_sthm import api_lc_cpt_02_sthm_router

api_cpt_router = APIRouter(prefix="/chat_prompt", tags=["ChatPrompt"])

api_cpt_router.include_router(api_lc_cpt_01_ft_router, prefix="/api_lc_cpt_01_ft")
api_cpt_router.include_router(api_lc_cpt_02_fm_router, prefix="/api_lc_cpt_02_fm")
api_cpt_router.include_router(api_lc_cpt_02_sthm_router, prefix="/api_lc_cpt_02_sthm")

        

