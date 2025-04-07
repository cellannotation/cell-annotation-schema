![Schema Validation](https://github.com/cellannotation/cell-annotation-schema/actions/workflows/schema_validator.yaml/badge.svg?branch=main)
# Cell Annotation Schema

A general, open-standard schema for cell annotations and related metadata.

This effort is part of [scFAIR](https://sc-fair.org/), an initiative to standardize single-cell genomics metadata.

## Overview

Single-cell genomics has revolutionized our understanding of cellular diversity and heterogeneity by providing large-scale datasets that offer insights into molecular biology. As the field of single-cell genomics expands rapidly, the production of single-cell data is increasing exponentially. However, this growth has highlighted the need for standardized methods to track, annotate, and report the acquired data. The lack of standardization makes the reuse and transfer of single-cell data challenging. Therefore, establishing a schema to register all metadata information related to single-cell genomics data is essential.

The purpose of the Cell Annotation Schema (CAS) is to serve as a guideline for scientists to organize their cell type annotation metadata in a standardized manner. This standardization facilitates seamless data sharing, aids in understanding the rationale behind specific cell type classifications, and provides additional information necessary for data analysis. It also allows scientists working on specific cell types to reference evidence behind these annotations and apply it to their own research.

## Motivation

The Cell Annotation Schema is an open-standard schema for cell annotations and related metadata. Its primary goals are to ensure interoperability between datasets, enable the programmatic generation of taxonomies from single-cell genomics data, and standardize information across datasets. By using the Cell Annotation Schema, scientists can collaboratively upload, annotate, and access single-cell data and associated metadata.

Annotating single-cell transcriptomics data with cell types or classes is inherently variable. The reasons authors choose to annotate a set of cells with a particular label are not typically represented in the annotated data, and no established standard exists for this process. For relatively simple datasets, it may be possible to reconstruct this information by reading the associated publication. However, as datasets and accompanying publications become increasingly complex, this reconstruction becomes difficult, and many publications lack the necessary detail. CAS addresses this problem by providing a programmatically accessible standard that allows users to record additional metadata about individual cell type annotations, including marker genes used as evidence and details of automated annotation transfers.


## User stories: 

For more information please visit the [User Stories](https://github.com/cellannotation/cell-annotation-schema/blob/main/docs/user_stories.md)

## Examples

Examples used in testing can be found [here](https://github.com/cellannotation/cell-annotation-schema/tree/main/examples)

## Structure

Single-cell data is usually stored as an [RDS file](https://www.jumpingrivers.com/blog/arrow-rds-parquet-comparison/) (for use in R) or an [AnnData file](https://anndata.readthedocs.io/en/latest/) (for use in Python). Single-cell sequencing data present their annotations nested into taxonomies, where cells are classified under specific cluster sets, clusters, or subclusters. These levels of metadata can be found in the AnnData file or stored using the JSON schema by saving the annotation information in a single .json file. The Cell Annotation Schema stores single-cell sequencing information in one .json file, which consolidates all metadata into a compact, validatable format. This file includes a link to a cell-by-gene matrix file of annotated data. The .json file can store text information regarding the rationale for annotating specific cells, the evidence papers, the taxonomy layer, and more.

The top level of the JSON file stores metadata about the annotations, such as author details, links to the annotated matrix file, and version information. This can be viewed as a table that links to a set of subtables (Figure 1).

<img src="/Users/aa37/Documents/GitHub/cell-annotation-schema/Images/Figure_1_Author" alt="Figure 1" width="500"/>

**Figure 1: The beginning of a .json file following the Cell Annotation Schema, in here the author of the dataset, their orchid ID and the matrix_file_id from CellXGene are present.**


The top level wraps other JSON objects (subtables):

- A list of annotation objects (a table of annotations), each belonging to a named 'labelset'.
- A table of labelsets - recording names, and additional metadata including a description and provenance (manual vs automated) and if automated, details of automated annotation algorithms etc. (Figure 2).

<img src="/Users/aa37/Documents/GitHub/cell-annotation-schema/Images/Figure_2_labelset" alt="Figure 2" width="500"/>

**Figure 2: one label set in a .json file following the Cell Annotation Schema. It presents pre-determined fields needed to define the cell type.**


Authors often add additional information that does not fit into predetermined fields in the Cell Annotation Schema. The schema allows for customization by adding an 'author_annotation_fields' table (Figure 3).

<img src="/Users/aa37/Documents/GitHub/cell-annotation-schema/Images/Figure_3_author_annotation_field" alt="Figure 3" width="500"/>

**Figure 3: The extension of author annotation fields with customisable informations that are outside of the Cell Annotation Schema.**


Large single-cell sequencing datasets often cluster cells at different levels of resolution (used to build a taxonomy). The Cell Annotation Schema accommodates these clusters under the term 'labelsets' (Figure 4).

<img src="/Users/aa37/Documents/GitHub/cell-annotation-schema/Images/Figure_4_labelsets" alt="Figure 4" width="500"/>

**Figure 4: The labelsets represent the granularity of the single cell dataset showing each level of resolution. In this case it is 'subcluster', 'cluster', 'supercluster'.**


Besides storing all metadata in one .json file, the schema is designed for decomposition into individual tables suitable for use in dataframes/TSVs and for flattening onto obs in AnnData format. 

The generation, wrangling, and conversion of .json files following the Cell Annotation Schema are managed by a Python package called [cas-tools](https://github.com/cellannotation/cas-tools), which generates .json files from AnnData files and structures them according to the schema.





## Core schema vs extensions

The core schema includes a limited set of compulsory fields. It avoids prohibiting additional fields, allowing for extensions and enabling users to add custom fields as long as they do not conflict with existing fields in the specification.

Documentation for the core and extension schemas is available at:

- [general_schema.md](https://github.com/cellannotation/cell-annotation-schema/blob/main/build/general_schema.md); Derived from [general_schema.json](https://github.com/cellannotation/cell-annotation-schema/blob/main/general_schema.json)
- [BICAN_schema.md](https://github.com/cellannotation/cell-annotation-schema/blob/main/build/BICAN_schema.md); Derived from [BICAN_schema.json](https://github.com/cellannotation/cell-annotation-schema/blob/main/build/BICAN_schema.json)
- [CAP_schema.md](https://github.com/cellannotation/cell-annotation-schema/blob/main/build/CAP_schema.md); Derived from [CAP_schema.json](https://github.com/cellannotation/cell-annotation-schema/blob/main/build/CAP_schema.json)

This repo also contains the [CAP AnnData Specification](https://github.com/cellannotation/cell-annotation-schema/blob/main/docs/cap_anndata_schema.md). 


## Releases

We publish both versioned releases and a nightly snapshot at https://github.com/cellannotation/cell-annotation-schema/releases

Release assets include a core schema file and extensions (currently for BICAN and the Cell Annotation Platform).

PyPI release is at https://pypi.org/project/cell-annotation-schema/

You can discover instructions on utilizing the PyPI package by visiting the following link https://github.com/cellannotation/cell-annotation-schema/blob/main/docs/pypi_package.md.


## Taxonomies adopting the Cell Annotation Schema


brain-bican contains a growing set of working taxonomies including:

- [Human neocortex non neuronal cells](https://github.com/Cellular-Semantics/human-neocortex-non-neuronal-cells)
- [Human neocortex mge derived interneurons](https://github.com/Cellular-Semantics/human-neocortex-mge-derived-interneurons)
- [Human neocortex IT projecting excitatory neurons](https://github.com/Cellular-Semantics/human-neocortex-it-projecting-excitatory-neurons)
- [Human neocortex deep layer excitatory neurons](https://github.com/Cellular-Semantics/human-neocortex-deep-layer-excitatory-neurons)
- [Human neocortex cge derived IT](https://github.com/Cellular-Semantics/human-neocortex-cge-derived-interneurons)
- [NHP basal ganglia](https://github.com/brain-bican/nhp_basal_ganglia_taxonomy)
- [Human brain cell atlas v1 non-neuronal](https://github.com/brain-bican/human-brain-cell-atlas_v1_non-neuronal)
- [Human brain cell atas v1 neusons](https://github.com/brain-bican/human-brain-cell-atlas_v1_neurons)
- [Human neocortex middle temporal gyrus](https://github.com/brain-bican/human-neocortex-middle-temporal-gyrus)
- [Whole mouse brain](https://github.com/Cellular-Semantics/whole_mouse_brain_taxonomy)



