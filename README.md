![Schema Validation](https://github.com/cellannotation/cell-annotation-schema/actions/workflows/schema_validator.yaml/badge.svg?branch=main)
# cell-annotation-schema

A general, open-standard schema for cell annotations and related metadata.

This effort is part of [scFAIR](https://sc-fair.org/), an initiative to standardize single-cell genomics metadata.

## Motivation

Annotation of single cell transcriptomics data with cell types/classes is inherently variable. The reasons authors choose to annotate a set of cells with a particular label are not typically represented in annotated data and there is no established standard for doing so.  For relatively simple datasets it may be possible to reconstruct this information by reading an associated publication, but as single cell transcriptomics datasets and accompanying publications become increasingly complex, doing so is becoming increasingly difficult and in many cases publications lack the necessary detail.

CAS provides a programmatically accessible standard designed to solve this problem by allowing users to record additional metadata about individual cell type annotations, including marker genes used as evidence and details of automated annotation transfer.  The standard is represented as JSON schema as this allows all metadata to be gathered in a single, compact validatable file - which includes a link to a cell by gene matrix file of annotated data. However, the schema is designed so that it can be decomposed into individual tables suitable for use in dataframes/TSVs and flattened onto obs in AnnData format.

## User stories: 

https://github.com/cellannotation/cell-annotation-schema/blob/main/docs/user_stories.md

## Examples

Examples used in testing can be browsed under: https://github.com/cellannotation/cell-annotation-schema/tree/main/examples

brain-bican contains a growing set of working taxonomies including: 

- https://github.com/brain-bican/human-brain-cell-atlas_v1_neurons

## Overview

The top level of the JSON is used to store metadata about the annotations: Author details; links to the annotated matrix file, version information etc.  This can be thought of as a table that links to a set of subtables.

The top level wraps other JSON objects (sub-tables):

1. A list of annotation objects (a table of annotations). Each annotation belongs to a named `labelset`
2. A table of labelsets - recording names, and additional metadata including a description and provenance (manual vs automated) and if automated, details of automated annotation algorithms etc.

## Core schema vs extensions

We define a core schema with a very limited set of compulsory fields.  The core schema avoids specifying that additional fields are forbidden, allowing extensions to be built and for any users to add their own customs fields as long as they don't stomp on existing fields in the specification. 

Documentation for the core and extension schemas is available at:

- [general_schema.md](https://github.com/cellannotation/cell-annotation-schema/blob/main/build/general_schema.md); Derived from [general_schema.json](https://github.com/cellannotation/cell-annotation-schema/blob/main/general_schema.json)
- [BICAN_schema.md](https://github.com/cellannotation/cell-annotation-schema/blob/main/build/BICAN_schema.md); Derived from [BICAN_schema.json](https://github.com/cellannotation/cell-annotation-schema/blob/main/build/BICAN_schema.json)
- [CAP_schema.md](https://github.com/cellannotation/cell-annotation-schema/blob/main/build/CAP_schema.md); Derived from [CAP_schema.json](https://github.com/cellannotation/cell-annotation-schema/blob/main/build/CAP_schema.json)

This repo also contains the [CAP AnnData Specification](https://github.com/cellannotation/cell-annotation-schema/blob/main/docs/cap_anndata_schema.md). Warning - PROVISIONAL - We are working to fully align this with the CAP extension.


## Releases

We publish both versioned releases and a nightly snapshot at https://github.com/cellannotation/cell-annotation-schema/releases

Release assets include a core schema file and extensions (currently for BICAN and the Cell Annotation Platform).

PyPI release is at https://pypi.org/project/cell-annotation-schema/

You can discover instructions on utilizing the PyPI package by visiting the following link https://github.com/cellannotation/cell-annotation-schema/blob/main/docs/pypi_package.md.





