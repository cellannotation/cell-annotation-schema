# General Cell Annotation Open Standard

*A general, open-standard schema for cell annotations which records connections, types, provenance and evidence.
This is designed not to tie-in to a single project (i.e. no tool-specific fields in core schema),and allows for extensions to support ad hoc user fields, new formal schema extensions, and project/tool specific metadata.*

## Properties

- **`cellannotation_schema_version`** *(string)*: The schema version, the cell annotation open standard. Current version MUST follow 0.1.0
This versioning MUST follow the format `'[MAJOR].[MINOR].[PATCH]'` as defined by Semantic Versioning 2.0.0, https://semver.org/.
- **`cellannotation_timestamp`** *(string)*: The timestamp of all cell annotations published (per dataset). This MUST be a string in the format `'%yyyy-%mm-%dd %hh:%mm:%ss'`.
- **`cellannotation_version`** *(string)*: The version for all cell annotations published (per dataset). This MUST be a string. The recommended versioning format is `'[MAJOR].[MINOR].[PATCH]'` as defined by Semantic Versioning 2.0.0, https://semver.org/.
- **`cellannotation_url`** *(string)*: A persistent URL of all cell annotations published (per dataset). .
- **`author_name`** *(string)*: This MUST be a string in the format `[FIRST NAME] [LAST NAME]`.
- **`author_contact`** *(string)*: This MUST be a valid email address of the author.
- **`orcid`** *(string)*: This MUST be a valid ORCID for the author.
- **`labelset`** *(array)*
  - **Items**: Refer to *[#/definitions/Annotation](#definitions/Annotation)*.

  
## Definitions

- <a id="definitions/automated_annotation"></a>**`automated_annotation`** *(object)*: A set of fields for recording the details of the automated annotation algorithm used.\n(Common 'automated annotation methods' would include PopV, Azimuth, CellTypist, scArches, etc.)
  - **`algorithm_name`** *(string, required)*: The name of the algorithm used. It MUST be a string of the algorithm's name.
  - **`algorithm_version`** *(string, required)*: The version of the algorithm used (if applicable). It MUST be a string of the algorithm's version, which is typically in the format '[MAJOR].[MINOR]', but other versioning systems are permitted (based on the algorithm's versioning).
  - **`algorithm_repo_url`** *(string, required)*: This field denotes the URL of the version control repository associated with the algorithm used (if applicable). It MUST be a string of a valid URL.
  - **`reference_location`** *(string)*: This field denotes a valid URL of the reference dataset used to do annotation transfer (if applicable). This should be the URL of data portal location or other repository. 
This MUST be a string of a valid URL. The concept of a 'reference' specifically refers to 'annotation transfer' algorithms, whereby a 'reference' dataset is used to transfer cell annotations to the 'query' dataset.
- <a id="definitions/Annotation"></a>**`Annotation`** *(object)*: A collection of fields recording a cell type/class/state annotation on some set os cells, supporting evidence and provenance. As this is intended as a general schema, compulsory fields are kept to a minimum. However, tools using this schema are encouarged to specify a larger set of compulsory fields for publication. 
<<<<<<< HEAD
  
=======
	
>>>>>>> 3ea53462fa5fdf0bf7ec5b0b5801f4b03c738438
  Note: This schema deliberately allows for additional fields in order to support ad hoc user fields, new formal schema extensions and project/tool specific metadata.
  - **`cellannotation_set`** *(string, required)*: The unique name of the set of cell annotations. 
Each cell within the AnnData/Seurat file MUST be associated with a 'cell_label' value in order for this to be a valid 'cellannotation_set'.
  - **`cell_label`** *(string, required)*: This denotes any free-text term which the author uses to annotate cells, i.e. the preferred cell label name used by the author. Abbreviations are exceptable in this field; refer to 'cell_fullname' for related details. 
Certain key words have been reserved:
    - `'doublets'` is reserved for encoding cells defined as doublets based on some computational analysis
    - `'junk'` is reserved for encoding cells that failed sequencing for some reason, e.g. few genes detected, high fraction of mitochondrial reads
    - `'unknown'` is explicitly reserved for unknown or 'author does not know'
    - `'NA'` is incomplete, i.e. no cell annotation was provided
  - **`cell_fullname`** *(string)*: This MUST be the full-length name for the biological entity listed in `cell_label` by the author. (If the value in `cell_label` is the full-length term, this field will contain the same value.) 
NOTE: any reserved word used in the field 'cell_label' MUST match the value of this field. 
    
    **EXAMPLE 1:** Given the matching terms 'LC' and 'luminal cell' used to annotate the same cell(s), then users could use either terms as values in the field 'cell_label'. However, the abbreviation 'LC' CANNOT be provided in the field 'cell_fullname'. 
    
    **EXAMPLE 2:** Either the abbreviation 'AC' or the full-length term intended by the author 'GABAergic amacrine cell' MAY be placed in the field 'cell_label', but as full-length term naming this biological entity, 'GABAergic amacrine cell' MUST be placed in the field 'cell_fullname'.
  - **`cell_ontology_term_id`** *(string)*: This MUST be a term from either the Cell Ontology (https://www.ebi.ac.uk/ols/ontologies/cl) or from some ontology that extends it by classifying cell types under terms from the Cell Ontology e.g. the Provisional Cell Ontology (https://www.ebi.ac.uk/ols/ontologies/pcl) or the Drosophila Anatomy Ontology (DAO) (https://www.ebi.ac.uk/ols4/ontologies/fbbt).
    
    NOTE: The closest available ontology term matching the value within the field 'cell_label' (at the time of publication) MUST be used. For example, if the value of 'cell_label' is 'relay interneuron', but this entity does not yet exist in the ontology, users must choose the closest available term in the CL ontology. In this case, it's the broader term 'interneuron' i.e.  https://www.ebi.ac.uk/ols/ontologies/cl/terms?obo_id=CL:0000099.
  - **`cell_ontology_term`** *(string)*: This MUST be the human-readable name assigned to the value of 'cell_ontology_term_id'.
  - **`cell_ids`** *(array)*: List of cell barcode sequences/UUIDs used to uniquely identify the cells within the AnnData/Seurat matrix. Any and all cell barcode sequences/UUIDs MUST be included in the AnnData/Seurat matrix.
    - **Items** *(string)*: Cell barcode sequences/UUIDs used to uniquely identify the cells within the AnnData/Seurat matrix. Any and all cell barcode sequences/UUIDs MUST be included in the AnnData/Seurat matrix.
  - **`rationale`** *(string)*: The free-text rationale which users provide as justification/evidence for their cell annotations. 
    Researchers are encouraged to use this field to cite relevant publications in-line using standard academic citations of the form `(Zheng et al., 2020)` This human-readable free-text MUST be encoded as a single string.
    All references cited SHOULD be listed using DOIs under rationale_dois. There MUST be a 2000-character limit.
  - **`rationale_dois`** *(array)*: A list of valid publication DOIs cited by the author to support or provide justification/evidence/context for 'cell_label'.
    - **Items** *(string)*
  - **`marker_gene_evidence`** *(array)*: List of gene names explicitly used as evidence for this cell annotation. Each gene MUST be included in the matrix of the AnnData/Seurat file.
    - **Items** *(string)*: Gene names explicitly used as evidence, which MUST be in the matrix of the AnnData/Seurat file.
  - **`synonyms`** *(array)*: This field denotes any free-text term of a biological entity which the author associates as synonymous with the biological entity listed in the field 'cell_label'.
    In the case whereby no synonyms exist, the authors MAY leave this as blank, which is encoded as 'NA'. However, this field is NOT OPTIONAL.
    - **Items** *(string)*: List of synonyms.
  - **`provenance`** *(object)*
    - **`method`** *(string)*: This field denotes the method used for creating the cell annotations. This MUST be one of the following strings: `'algorithmic'`, `'manual'`, or `'both'` .
    - **`automated_annotation`** *(object)*: Refer to *[#/definitions/automated_annotation](#definitions/automated_annotation)*.




## CAP-specific fields

- **category_text** *(string)*: The free-text term denoting a biological entity which the author associates as a 'class' or 'broader term' for the value/term in the field\n.This field MAY be 'NA' if the author cannot associate free-text classes to the value/term in 'cell_label'. However, this field is NOT OPTIONAL.

- **category_ontology_term_id** *(string)*: Every value in the field 'category_text' MUST be associated with the closest available ontology term, following the same logic detailed for the field 'cell_label'.

- **category_ontology_term** *(string)*: This MUST be the human-readable name assigned to the value of 'category_ontology_term_id'




