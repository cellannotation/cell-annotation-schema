![Schema Validation](https://github.com/cellannotation/cell-annotation-schema/actions/workflows/schema_validator.yaml/badge.svg?branch=main)
# cell-annotation-schema

General, open-standard schema for cell annotations

## Motivation

Annotation of single cell transcriptomics data with cell types/classes is inherently variable. The reasons that authors choose to annotate a set of cells with a particular label are not typically represented in annotated data and there is no established standard for doing so.  For relatively simple datasets it may be possible to reconstruct this information by reading an associated publication, but as single cell transcriptomics datasets and accompanying publications become increasingly complex, doing so is becoming increasingly difficult and in many cases publications lack the necessary detail.

CAS provides a programmatically accessible standard designed to solve this problem by allowing users to record additional metadata about individual cell type annotations, including marker genes used as evidence and details of automated annotation transfer.  The standard is represented as JSON schema as this allows all metadata to be gathered in a single, compact validatable file - which includes a link to a cell by gene matrix file of annotated data. However, the schema is designed so that it can be decomposed into individual tables suitable for use in dataframes/TSVs and flattened onto obs in AnnData format.

## User stories: 

https://github.com/cellannotation/cell-annotation-schema/blob/main/user_stories.md

## Examples

Examples used in testing can be browsed under: https://github.com/cellannotation/cell-annotation-schema/tree/main/examples


## Overview

The top level of the JSON is used to store metadata about the annotations it contains: Author details; links to the annotated matrix file, version information etc.  This can be thought of as a table the links to a set of subtables.

The top level wraps other JSON objects (sub-tables):

1. A list of annotation objects (a table of annotations). Each annotation belongs to a named `labelset`
2. A table of labelsets - recording names, and additional metadata including a description and provenance (manual vs automated) and if automated, details of automated annotation algorithms etc.

## Core schema vs extensions

We define a core schema with a very limited set of compulsory fields.  The core schema avoids specifying that additional fields are forbidden, allowing extensions to be built and for any users to add their own customs fields as long as they don't stomp on existing fields in the specification. 

## Releases

We publish both versioned releases and a nightly snapshot at https://github.com/cellannotation/cell-annotation-schema/releases

Release assets include a core schema file and extensions (currently for BICAN and the Cell Annotation Platform).

PyPI release is at https://pypi.org/project/cell-annotation-schema/

You can discover instructions on utilizing the PyPI package by visiting the following link https://github.com/cellannotation/cell-annotation-schema/blob/main/docs/pypi_package.md

## Contents
- General standard for annotating cell sets (JSON Schema)
- General standard - JSON Schema rendered in Markdown  - WARNING - MAY BE OUT OF DATE - DERIVATION NOT CURRENTLY AUTOMATED
- Specification of flattening to AnnData. -  WARNING - MAY BE OUT OF DATE - DERIVATION NOT CURRENTLY AUTOMATED
- Extensions for BICAN and the Cell Annotation Platform.



