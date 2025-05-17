#!/bin/sh -e

ruff check --fix ../seo
ruff format ../seo

ruff check --fix ../llm
ruff format ../llm