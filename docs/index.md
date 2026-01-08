# apokatastasis

Apokatastasis is an experimental static site generator targeting the very
specific needs of academic publishing.

## Goals

This project is an attempt to work towards building infrastructure for single-
source, plain-text publishing in an academic context.

## Design

Generally, we should work with the pandoc-flavored markdown standard.
It is well-established in academic circles, and we can use pandoc to convert
our markup into binary objects (PDFs, EPUB, etc.)

This site should support the use of "markup extensions." These are elements
that are customized by user to abstract certain elements that are then compiled
down into JATSXML/HTML/etc. i.e., epigraphs, ORCID links, etc.

This site should _not_ be prescriptive in its syntax and use. We will leave
that work to those good people who maintain the standards. This will simply
build infrastructure that complies with those standards.

When users generate markup (particularly JATSXML) that is _not_ valid, we
should warn the user. We want to make doing things right as easy as possible
and make doing things wrong as hard as possible.

## Getting Started

clone this repository

`cd apokatastasis/journal`

`uv run fastapi dev manage.py` <- Better CLI tooling needed
