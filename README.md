# cell-annotation-schema

General, open-standard schema for cell annotations

## Motivation

Annotation of single cell transcriptomics data with cell types/classes is inherently variable. The reasons that authors choose to annotate some particular set of cells in a particular way is not typically represented in annotated data and there is no established standard for doing so - at best it is accessible by reading the associated paper, but as datasets information in the paper on evidence is often incomplete and hard to resonstruct.  

CAS provides a solution to this problem by allowing users to record additional metadata about individual cell type annotations, including marker genes used as evidence and details of automated annotation transfer.  The standard is represented as JSON schema as this allows all metadata to be gathered in a single, compact validatable file - which includes a link to a cell by gene matrix file of annotated data. 

However, the schema is designed so that it can be decomposed into individual tables suitable for use in dataframes/TSVs and flattened onto obs in AnnData format.

## User stories: 

https://github.com/cellannotation/cell-annotation-schema/blob/main/user_stories.md

## Contents
- General standard for annotating cell sets (JSON Schema)
- General standard - JSON Schema rendered in Markdown (derived)
- Specification of flattening to AnnData.
- Extensions for BICAN and the Cell Annotation Platform.

