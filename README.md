# cell-annotation-schema

General, open-standard schema for cell annotations

## Background/existing standards

The [CellXGene schema](https://github.com/chanzuckerberg/single-cell-curation/tree/main/schema/) provides a widely used solution for annotating and standardising single cell expression matrices in AnnData format.  It incudes fields and guidance for recording cell type using the Cell Ontology - as annotations on single cells (AnnData `obs`). Because it is an open schema - additional fields are allowed as long as they don't duplicate or stomp on schema fields - users frequently add additional cell type annotations as free text.   These often represent more granular annotations and the terms themselves are useful to users as the typcially map to those used in paper. 

This schema is a good fit for CellXGene applications include [Discover](https://cellxgene.cziscience.com/) where it supports rendering of UMAPs by cell type and [Census](https://chanzuckerberg.github.io/cellxgene-census/) - where it supports the generation of AnnData matrices that combine cell expression profiles from across datasets based on their annotation. 

## Motivation

Annotation of single cell transcriptomics data with cell types/classes is inherently variable. The reasons that authors choose to annotate some particular set of cells in a particular way is not represented in annotated data - at best it is accessible by reading the associated paper, but as datasets information in the paper on evidence is often incomplete and hard to resonstruct.  

CAS attempts to remedy this by allowing users to record additional metadata about individual cell type annotations, including marker genes used as evidence and details of automated annotation transfer.  

## User stories: 

https://github.com/cellannotation/cell-annotation-schema/blob/main/user_stories.md

## Contents
- General standard for annotating cell sets (JSON Schema)
- General standard - JSON Schema rendered in Markdown (derived)
- Specification of flattening to AnnData.
- Extensions for BICAN and the Cell Annotation Platform.

