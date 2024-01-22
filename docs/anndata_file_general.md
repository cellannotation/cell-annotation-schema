
# AnnData file, GENERAL 

This is a general standard for mapping the cell annotation metadata from the schema (JSON Schema) below into an [AnnData file](https://anndata.readthedocs.io/en/latest/).

This document uses the schema (JSON Schema) rendered as a markdown within [schema_proposal.md](https://github.com/evanbiederstedt/cellannotation_standard_jeremy/blob/main/schema_proposal.md)

The only fields of the AnnData file which are relevant for this are `obs` (which stores mappings key/value pairs to individual cells using a pandas DataFrame) and `uns` (which is a python dictionary storing sample-level/donor-level metadata).

**NOTE:** In this document, the field name of the JSON Schema is written as `'field_name'` while the value of the field is written as `[field_name]`. 



* [`obs` (Cell metadata)](#obs-cell-metadata), which describe each cell in the dataset
* [`uns` (Dataset metadata)](#uns-dataset-metadata), which describe the dataset as a whole


# obs (Cell metadata)

These are columns and values within a pandas DataFrame: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html


## [cellannotation_setname]

The string specified by the user for `[cellannotation_setname]` will be used as the pandas DataFrame column name (key) to encode all columns in `*.obs`.

**Format:** The column name is the string `[cellannotation_setname]` and the values are the strings of `cell_label`. Refer to the fields `cellannotation_setname` and `cell_label` in the JSON Schema.

* **column** `[cellannotation_setname]`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of `cell_label` strings, i.e. any free-text term which the author uses to annotate cells, i.e. the preferred cell label name used by the author.


## [cellannotation_setname]--cell_fullname

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'cell_fullname'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'cell_fullname'`

For example, if the user specified the cell annotation as `broad_cells1`, then the name of the column in the pandas DataFrame will be `broad_cells1--cell_fullname`. 

* **column** `[cellannotation_setname]--cell_fullname`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of `cell_fullname` strings, i.e. the full-length name for the biological entity listed in `cell_label` by the author. 


## [cellannotation_setname]--cell_ontology_term_id

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'cell_ontology_term_id'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'cell_ontology_term_id'`

* **column** `[cellannotation_setname]--cell_ontology_term_id`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of `cell_ontology_term_id` strings, i.e. the ID from either the Cell Ontology (https://www.ebi.ac.uk/ols/ontologies/cl) or from some ontology that extends it by classifying cell types under terms from the Cell Ontology 



## [cellannotation_setname]--cell_ontology_term

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'cell_ontology_term'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'cell_ontology_term'`

* **column** `[cellannotation_setname]--cell_ontology_term`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of `cell_ontology_term` strings, i.e. the human-readable name assigned to the value of `'cell_ontology_term_id'`

## [cellannotation_setname]--rationale

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'rationale'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'rationale'`

* **column** `[cellannotation_setname]--rationale`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of strings maximum length 2000, i.e. each ndarray value must be a single encoding the free-text rationale which users provide as justification/evidence for their cell annotations. 

## [cellannotation_setname]--rationale_dois

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'rationale_dois'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'rationale_dois'`

* **column** `[cellannotation_setname]--rationale_dois`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of strings, i.e. each ndarray value must be a single comma-separated string of valid publication DOIs cited by the author to support or provide justification/evidence/context for 'cell_label'.

* **example:** `'10.1038/s41587-022-01468-y, 10.1038/s41556-021-00787-7, 10.1038/s41586-021-03465-8'`

## [cellannotation_setname]--marker_gene_evidence

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'marker_gene_evidence'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'marker_gene_evidence'`

* **column** `[cellannotation_setname]--marker_gene_evidence`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of strings, i.e. each ndarray value must be a single comma-separated string of gene names explicitly used as evidence for this cell annotation. Each gene MUST be included in the matrix of the AnnData/Seurat file.

* **example:** `'TP53, KRAS, BRCA1'`

## [cellannotation_setname]--synonyms

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'synonyms'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'synonyms'`

* **column** `[cellannotation_setname]--synonyms`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of strings, i.e. each ndarray value must be a single comma-separated string of synonyms for `cell_label`

* **example:** `'neuroglial cell, glial cell, neuroglia'`



# uns (Dataset metadata)

**NOTE:** Each time a cell annotation `cellannotation_setname` is modified, these values potentially change. 

## cellannotation_schema_version

Key-value pair in the `uns` dictionary

* **key:** `cellannotation_schema_version`
* **type:** string
* **value:** The schema version, the cell annotation open standard. 
This versioning MUST follow the format `'[MAJOR].[MINOR].[PATCH]'` as defined by Semantic Versioning 2.0.0, https://semver.org/. Current version MUST follow 0.1.0

## cellannotation_timestamp

Key-value pair in the `uns` dictionary

* **key:** `cellannotation_timestamp`
* **type:** string
* **value:** The timestamp of all cell annotations published (per dataset). This MUST be a string in the format `%yyyy-%mm-%dd %hh:%mm:%ss`.

## cellannotation_version

Key-value pair in the `uns` dictionary

* **key:** `cellannotation_version`
* **type:** string
* **value:** The version for all cell annotations published (per dataset). This MUST be a string. The recommended versioning format is `'[MAJOR].[MINOR].[PATCH]'` as defined by Semantic Versioning 2.0.0, https://semver.org/


## cellannotation_url

Key-value pair in the `uns` dictionary

* **key:** `cellannotation_url`
* **type:** string
* **value:** A persistent URL of all cell annotations published (per dataset)


## author_name

Key-value pair in the `uns` dictionary

* **key:** `author_name`
* **type:** string
* **value:** This MUST be a string in the format `[FIRST NAME] [LAST NAME]`.


## author_contact

Key-value pair in the `uns` dictionary

* **key:** `author_contact`
* **type:** string
* **value:** This MUST be a valid email address of the author.

## orcid

Key-value pair in the `uns` dictionary

* **key:** `author_contact`
* **type:** string
* **value:** This MUST be a valid ORCID for the author.


## annotation_source

Python dictionary within the `uns` dictionary


#### [cellannotation_setname]--source

* **key:** `[cellannotation_setname]--source`
* **type:** python dictionary
* **value:** the rest of the dictionary as defined below

#### method


* **key:** `'method'`
* **type:** string
* **value:** `'algorithmic'`, `'manual'`, or `'both'` (If `'algorithmic'` or `'both'`, more details are required. If `'manual'`, all other values will be `NA`.)

#### algorithm_name


* **key:** `'algorithm_name'`
* **type:** string
* **value:** The name of the algorithm used

#### algorithm_version

* **key:** `'algorithm_version'`
* **type:** string
* **value:** The string of the algorithm's version, which is typically in the format '[MAJOR].[MINOR]', but other versioning systems are permitted (based on the algorithm's versioning).

#### algorithm_repo_url

* **key:** `'algorithm_repo_url'`
* **type:** string
* **value:** The string of the URL of the version control repository associated with the algorithm used (if applicable). It MUST be a string of a valid URL.


#### reference_location


* **key:** `'reference_location'`
* **type:** string
* **value:** The string of the URL pointing to the reference dataset.


