# General Cell Annotation Open Standard

*A general, open-standard schema for cell annotations which records connections, types, provenance and evidence.
This is designed not to tie-in to a single project (i.e. no tool-specific fields in core schema),and allows for extensions to support ad hoc user fields, new formal schema extensions, and project/tool specific metadata.*

- [Properties](#properties)

## Properties

- **`matrix_file_id`** *(string)*: A resolvable ID for a cell by gene matrix file in the form namespace:accession, e.g. CellXGene_dataset:8e10f1c4-8e98-41e5-b65f-8cd89a887122.  Please see https://github.com/cellannotation/cell-annotation-schema/registry/registry.json for supported namespaces.


- **`title`** *(string, required)*: The title of the dataset. This MUST be less than or equal to 200 characters. e.g. 'Human retina cell atlas - retinal ganglion cells'.


- **`description`** *(string)*: The description of the dataset. e.g. 'A total of 15 retinal ganglion cell clusters were identified from over 99K retinal ganglion cell nuclei in the current atlas. Utilizing previous characterized markers from macaque, 5 clusters can be annotated.'.


- **`cellannotation_schema_version`** *(string)*: The schema version, the cell annotation open standard. Current version MUST follow 0.1.0This versioning MUST follow the format `'[MAJOR].[MINOR].[PATCH]'` as defined by Semantic Versioning 2.0.0, https://semver.org/.


- **`cellannotation_timestamp`** *(string, format: date-time)*: The timestamp of all cell annotations published (per dataset). This MUST be a string in the format `'%yyyy-%mm-%dd %hh:%mm:%ss'`.


- **`cellannotation_version`** *(string)*: The version for all cell annotations published (per dataset). This MUST be a string. The recommended versioning format is `'[MAJOR].[MINOR].[PATCH]'` as defined by Semantic Versioning 2.0.0, https://semver.org/.


- **`cellannotation_url`** *(string)*: A persistent URL of all cell annotations published (per dataset). .


- **`author_list`** *(string)*: This field stores a list of users who are included in the project as collaborators, regardless of their specific role. An example list; '['John Smith', 'Cody Miller', 'Sarah Jones']'.


- **`author_name`** *(string, required)*: Primary author's name. This MUST be a string in the format `[FIRST NAME] [LAST NAME]`.


- **`author_contact`** *(string, format: email)*: Primary author's contact. This MUST be a valid email address of the author.


- **`orcid`** *(string)*: Primary author's orcid. This MUST be a valid ORCID for the author.


- **`labelsets`** *(array, required)*
    - **`name`** *(string, required)*: name of annotation key.
    - **`description`** *(string)*: Some text describing what types of cell annotation this annotation key is used to record.
    - **`annotation_method`** *(string)*: The method used for creating the cell annotations. This MUST be one of the following strings: `'algorithmic'`, `'manual'`, or `'both'` . Must be one of: `["algorithmic", "manual", "both"]`.
    - **`automated_annotation`** *(object)*:
      - **`algorithm_name`** *(string, required)*: The name of the algorithm used. It MUST be a string of the algorithm's name.
      - **`algorithm_version`** *(string, required)*: The version of the algorithm used (if applicable). It MUST be a string of the algorithm's version, which is typically in the format '[MAJOR].[MINOR]', but other versioning systems are permitted (based on the algorithm's versioning).
      - **`algorithm_repo_url`** *(string, required)*: This field denotes the URL of the version control repository associated with the algorithm used (if applicable). It MUST be a string of a valid URL.
      - **`reference_location`** *(string)*: This field denotes a valid URL of the annotated dataset that was the source of annotated reference data. This MUST be a string of a valid URL. The concept of a 'reference' specifically refers to 'annotation transfer' algorithms, whereby a 'reference' dataset is used to transfer cell annotations to the 'query' dataset.
    - **`rank`** *(integer)*: A number indicating relative granularity with 0 being the most specific.  Use this where a single dataset has multiple keys that are used consistently to record annotations and different levels of granularity.


- **`annotations`** *(array, required)*
    - **`labelset`** *(string, required)*: The unique name of the set of cell annotations. Each cell within the AnnData/Seurat file MUST be associated with a 'cell_label' value in order for this to be a valid 'cellannotation_setname'.
    - **`cell_label`** *(string, required)*: This denotes any free-text term which the author uses to annotate cells, i.e. the preferred cell label name used by the author. Abbreviations are exceptable in this field; refer to 'cell_fullname' for related details. Certain key words have been reserved:- `'doublets'` is reserved for encoding cells defined as doublets based on some computational analysis- `'junk'` is reserved for encoding cells that failed sequencing for some reason, e.g. few genes detected, high fraction of mitochondrial reads- `'unknown'` is explicitly reserved for unknown or 'author does not know'- `'NA'` is incomplete, i.e. no cell annotation was provided.
    - **`cell_fullname`** *(string)*: This MUST be the full-length name for the biological entity listed in `cell_label` by the author. (If the value in `cell_label` is the full-length term, this field will contain the same value.) NOTE: any reserved word used in the field 'cell_label' MUST match the value of this field. <br>    EXAMPLE 1: Given the matching terms 'LC' and 'luminal cell' used to annotate the same cell(s), then users could use either terms as values in the field 'cell_label'. However, the abbreviation 'LC' CANNOT be provided in the field 'cell_fullname'. <br>    EXAMPLE 2: Either the abbreviation 'AC' or the full-length term intended by the author 'GABAergic amacrine cell' MAY be placed in the field 'cell_label', but as full-length term naming this biological entity, 'GABAergic amacrine cell' MUST be placed in the field 'cell_fullname'.
    - **`cell_ontology_term_id`** *(string)*: This MUST be a term from either the Cell Ontology (https://www.ebi.ac.uk/ols/ontologies/cl) or from some ontology that extends it by classifying cell types under terms from the Cell Ontologye.g. the Provisional Cell Ontology (https://www.ebi.ac.uk/ols/ontologies/pcl) or the Drosophila Anatomy Ontology (DAO) (https://www.ebi.ac.uk/ols4/ontologies/fbbt).<br>    NOTE: The closest available ontology term matching the value within the field 'cell_label' (at the time of publication) MUST be used.For example, if the value of 'cell_label' is 'relay interneuron', but this entity does not yet exist in the ontology, users must choose the closest available term in the CL ontology. In this case, it's the broader term 'interneuron' i.e.  https://www.ebi.ac.uk/ols/ontologies/cl/terms?obo_id=CL:0000099.
    - **`cell_ontology_term`** *(string)*: This MUST be the human-readable name assigned to the value of 'cell_ontology_term_id'.
    - **`cell_ids`** *(list)*: List of cell barcode sequences/UUIDs used to uniquely identify the cells within the AnnData/Seurat matrix. Any and all cell barcode sequences/UUIDs MUST be included in the AnnData/Seurat matrix.
    - **`rationale`** *(string)*: The free-text rationale which users provide as justification/evidence for their cell annotations. Researchers are encouraged to use this field to cite relevant publications in-line using standard academic citations of the form `(Zheng et al., 2020)` This human-readable free-text MUST be encoded as a single string.All references cited SHOULD be listed using DOIs under rationale_dois. There MUST be a 2000-character limit.
    - **`rationale_dois`** *(list)*: A list of valid publication DOIs cited by the author to support or provide justification/evidence/context for 'cell_label'.
    - **`marker_gene_evidence`** *(list)*: List of names of genes whose expression in the cells being annotated is explicitly used as evidence for this cell annotation. Each gene MUST be included in the matrix of the AnnData/Seurat file.
    - **`synonyms`** *(list)*: This field denotes any free-text term of a biological entity which the author associates as synonymous with the biological entity listed in the field 'cell_label'.In the case whereby no synonyms exist, the authors MAY leave this as blank, which is encoded as 'NA'. However, this field is NOT OPTIONAL.
    - **`reviews`** *(list)*
      - **`datestamp`** *(string, format: date-time, required)*: Time and date review was last edited.
      - **`reviewer`** *(string)*: Review Author.
      - **`review`**: Reviewer's verdict on the annotation.  Must be 'Agree' or 'Disagree'. Must be one of: `["Agree", "Disagree"]`.
      - **`explanation`**: Free-text review of annotation. This is required if the verdict is disagree and should include reasons for disagreement.
    - **`author_annotation_fields`** *(object)*: A dictionary of author defined key value pairs annotating the cell set. The names and aims of these fields MUST not clash with official annotation fields.
    - **`cell_set_accession`** *(string)*: An identifier that can be used to consistently refer to the set of cells being annotated, even if the cell_label changes.
    - **`parent_cell_set_accession`** *(string)*: A list of accessions of cell sets that subsume this cell set. This can be used to compose hierarchies of annotated cell sets, built from a fixed set of clusters.
    - **`transferred_annotations`** *(list)*
        - **`transferred_cell_label`** *(string)*: Transferred cell label.
        - **`source_taxonomy`** *(string)*: PURL of source taxonomy.
        - **`source_node_accession`** *(string)*: accession of node that label was transferred from.
        - **`algorithm_name`** *(string)*: .
        - **`comment`** *(string)*: Free text comment on annotation transfer.
    - **`cells`** *(list)*: By convention this is only used for annotation transfer labelsets.  It MUST not be combined with the 'cell_ids' field.
      - **`cell_id`** *(string, required)*: Identifier for a single cell.
      - **`confidence`** *(number)*: Normalised confidence score.
      - **`author_categories`** *(list)*
    - **`negative_marker_gene_evidence`** *(list)*: List of names of genes, the absence of expression of which is explicitly used as evidence for this cell annotation. Each gene MUST be included in the matrix of the AnnData/Seurat file.
    - **`neurotransmitter_accession`** *(string)*: Accessions of cell neurotransmitter associated with this cell set.
    - **`neurotransmitter_rationale`** *(string)*: The free-text rationale which users provide as justification/evidence for supporting the neurotransmitter association.
    - **`neurotransmitter_marker_gene_evidence`** *(list)*: List of gene names used as evidence for neurotransmitter association. Each gene MUST be included in the matrix of the AnnData/Seurat file.


