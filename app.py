import logging
from typing import Iterator, Annotated

from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session

from shortypy.domain.link import (
    LinkRepository,
    LinkNotFoundError
)
from shortypy.infrastructure.sqlite.database import SessionLocal, create_tables
from shortypy.infrastructure.sqlite.link import (
    LinkRepositoryImpl,
    LinkQueryServiceImpl,
    LinkCommandUseCaseUnitOfWorkImpl
)
from shortypy.application.link import (
    LinkReadModel,
    LinkCreateModel,
    LinkQueryService,
    LinkQueryUseCase,
    LinkQueryUseCaseImpl,
    LinkCommandUseCase,
    LinkCommandUseCaseImpl,
    LinkCommandUseCaseUnitOfWork
)
from shortypy.application.code_generation import CodeGeneratorImpl
from shortypy.presentation.schema.link import ErrorLinkNotFound

logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event('startup')
async def on_startup():
    create_tables()


def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_link_query_usecase(session: Annotated[Session, Depends(get_session)]) -> LinkQueryUseCase:
    query_service: LinkQueryService = LinkQueryServiceImpl(session)
    return LinkQueryUseCaseImpl(query_service)


def get_link_command_usecase(session: Annotated[Session, Depends(get_session)]) -> LinkCommandUseCase:
    repository: LinkRepository = LinkRepositoryImpl(session)
    uow: LinkCommandUseCaseUnitOfWork = LinkCommandUseCaseUnitOfWorkImpl(
        session, repository
    )

    return LinkCommandUseCaseImpl(uow, CodeGeneratorImpl(5))


@app.post(
    '/shorten',
    response_model=LinkReadModel,
    status_code=status.HTTP_201_CREATED,
    tags=['Shorten']
)
async def create_shorten_link(
        data: LinkCreateModel,
        link_command_usecase_instance: Annotated[LinkCommandUseCase, Depends(get_link_command_usecase)]
):
    try:
        link = link_command_usecase_instance.create_link(data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return link


@app.get(
    '/shorten/{code}',
    response_model=LinkReadModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorLinkNotFound
        }
    },
    tags=['Shorten']
)
async def get_shorten_link(
        code: str,
        link_query_usecase_instance: Annotated[LinkQueryUseCase, Depends(get_link_query_usecase)]
):
    try:
        link = link_query_usecase_instance.fetch_link_by_id(code)
    except LinkNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link with code {code} was not found"
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return link
