"""
Main
"""
from __future__ import annotations

import argparse
import logging

from fastapi import FastAPI
import uvicorn  # type: ignore

from .routers import notes
from .auth.routers import authn, users


# command line arguments
parser = argparse.ArgumentParser(
    description="remotenote: REST API to read and write notes."
)
parser.add_argument(
    "--logfile",
    action="store",
    type=str,
    default="remotenote.log",
    help="The location on disk to write the log."
)
parser.add_argument(
    "--loglevel",
    action="store",
    type=str,
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    default="WARNING",
    help="The level of detail logged. DEBUG is the most verbose"
)
args = parser.parse_args()


# logging setup
logging.basicConfig(
    filename=args.logfile,
    encoding="utf-8",
    level=getattr(logging, args.loglevel.upper())
)


app = FastAPI()
app.include_router(authn.router)
app.include_router(users.router)
app.include_router(notes.router)

uvicorn.run("__main__:app")
