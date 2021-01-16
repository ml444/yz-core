#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth:
@date: 2020-9-13
@desc: ...
"""
from fastapi import FastAPI
from src.settings import settings
from src.apps.myapp import views as hello_views
# from src.app import views as hello_views

# from src.apps import node
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# # Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

app.include_router(hello_views.router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8080)