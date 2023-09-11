# CAP Encoding for AnnData file

Contact: [...]

Document Status: In Review

Version: unpublished 

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED" "MAY", and "OPTIONAL" in this document are to be interpreted as described in [BCP 14](https://tools.ietf.org/html/bcp14), [RFC2119](https://www.rfc-editor.org/rfc/rfc2119.txt), and [RFC8174](https://www.rfc-editor.org/rfc/rfc8174.txt) when, and only when, they appear in all capitals, as shown here.

## Background

Much of this schema has been based on the v4.0.0 CELLxGENE schema, documented at this GitHub commit [here](https://github.com/chanzuckerberg/single-cell-curation/blob/2c53d2b77a9b76c14955484ae5f378515fe5e72f/schema/4.0.0/schema.md). 

### Required Ontologies

The following ontologies are utilized within this schema:

| Ontology | OBO Prefix | Download |
|:--|:--|:--|
| [Cell Ontology] | CL | [cl.owl]|
| [Experimental Factor Ontology] | EFO | [efo.owl]
| [Mondo Disease Ontology] | MONDO | [mondo.owl] |
| [NCBI organismal classification] |  NCBITaxon | [ncbitaxon.owl] |
| [Uberon multi-species anatomy ontology] |  UBERON | [uberon.owl] |
| | | |

[Cell Ontology]: http://obofoundry.org/ontology/cl.html
[2023-07-20]: https://github.com/obophenotype/cell-ontology/releases/tag/v2023-07-20
[cl.owl]: https://github.com/obophenotype/cell-ontology/releases/download/v2023-07-20/cl.owl

[Experimental Factor Ontology]: http://www.ebi.ac.uk/efo
[2023-07-17 EFO 3.56.0]: https://github.com/EBISPOT/efo/releases/tag/v3.56.0
[efo.owl]: https://github.com/EBISPOT/efo/releases/download/v3.56.0/efo.owl

[Mondo Disease Ontology]: http://obofoundry.org/ontology/mondo.html
[2023-07-03]: https://github.com/monarch-initiative/mondo/releases/tag/v2023-07-03
[mondo.owl]: https://github.com/monarch-initiative/mondo/releases/download/v2023-07-03/mondo.owl

[NCBI organismal classification]: http://obofoundry.org/ontology/ncbitaxon.html
[2023-06-20]: https://github.com/obophenotype/ncbitaxon/releases/tag/v2023-06-20
[ncbitaxon.owl]: https://github.com/obophenotype/ncbitaxon/releases/download/v2023-06-20/ncbitaxon.owl.gz

[Uberon multi-species anatomy ontology]: http://www.obofoundry.org/ontology/uberon.html
[2023-06-28]: https://github.com/obophenotype/uberon/releases/tag/v2023-06-28
[uberon.owl]: https://github.com/obophenotype/uberon/releases/download/v2023-06-28/uberon.owl


# Sections

Sections are as follows, based on the [AnnData file format](https://anndata.readthedocs.io/en/latest/generated/anndata.AnnData.html#anndata.AnnData): 

* [`X` (Matrix layers)](#x-matrix-layers)
* [`obs` (Cell metadata)](#obs-cell-metadata), metadata on each cell
    * [Dataset-specific metadata](#dataset-specific-metadata)
    * [Cell annotation metadata](#cell-annotation-metadata)
* [`var` and `raw.var` (Gene metadata)](#var-and-rawvar-gene-metadata), metadata on each gene
* [`obsm` (Embeddings)](#obsm-embeddings)
* [`uns` (Dataset metadata)](#uns-dataset-metadata), metadata related to the dataset itself



# `X` (Matrix Layers)

This is the standard X layer within the AnnData file, see [here](https://anndata.readthedocs.io/en/latest/generated/anndata.AnnData.html#anndata.AnnData). 

This is the data matrix of the dimension `(#observations, #variables)` data matrix.

Users MUST provide the raw count matrix either in `.X` or `.raw.X` fields. If the user provides the raw count matrix in `.X` the `.raw` layer MUST be empty.  

Users MAY provide the normalized matrix in the `.X` field. We STRONGLY RECOMMEND users to provide both a raw count matrix and a normalized one. We STRONGLY RECOMMEND users to normalize the matrix with the following algorithm:

1. Normalize counts per cell up to 10 000 reads per cell (NOTE: this is done simply so that counts become comparable among cells. See the default values used in the ScanPy tutorial [here](https://scanpy-tutorials.readthedocs.io/en/latest/pbmc3k.html) or the Seurat function `NormalizeData()` [here](https://satijalab.org/seurat/reference/normalizedata))
2. Use `log(1+x)` transformation

If the normalized matrix provided by the user differs from the expected one based on the algorithm above, then the user provided matrix will be moved to the additional AnnData layer named `AnnData.layers['user-provided']`. In this case, the `.X` field will be filled by a re-normalized raw count matrix using the algorithm above. NOTE: The re-normalization is needed for reliable work of the CAP calculations.

After the CAP preprocessing, any AnnData file downloadable via CAP:
- MUST have the raw count matrix in `.raw.X`, 
- MUST have a normalized (by the algorithms above) matrix  in `.X`
- MAY have a normalized (by another algorithm) matrix  in the `.layers['user-provided']`

In any layer, if a matrix has 50% or more values that are zeros, it is STRONGLY RECOMMENDED that the matrix be encoded as a [`scipy.sparse.csr_matrix`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html).



# `obs` (Cell Metadata)

`obs` is a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html).


## Dataset-specific Metadata


### donor_id

* **column** `donor_id`
* **dtype:** string
* **value:** A UUID for the donor/sample within this dataset



### organism_ontology_term_id


* **column** `organism_ontology_term_id`
* **dtype:** string
* **value:** This MUST be a child of <a href="https://www.ebi.ac.uk/ols4/ontologies/ncbitaxon/classes?obo_id=NCBITaxon%3A33208"><code>NCBITaxon:33208</code></a> for <i>Metazoa</i>.


### organism

* **column** `organism`
* **dtype:** string
* **value:** This MUST be the human-readable term assigned to the value of <code>organism_ontology_term_id</code>. The ontology term and ontology term ID MUST match.


### disease_ontology_term_id

* **column** `disease_ontology_term_id`
* **dtype:** string
* **value:** This MUST be a MONDO term or <a href="https://www.ebi.ac.uk/ols4/ontologies/pato/classes?obo_id=PATO%3A
0000461"><code>"PATO:0000461"</code></a> for <i>normal</i> or <i>healthy</i>.


### disease

* **column** `disease`
* **dtype:** string
* **value:** This MUST be the human-readable term which corresponds to the value of <code>disease_ontology_term_id</code>. The ontology term and ontology term ID MUST match.

### assay_ontology_term_id

* **column** `assay_ontology_term_id`
* **dtype:** string
* **value:** This MUST be an EFO term and SHOULD be the most accurate EFO term for this assay. The two options are more specific terms under `"assay by molecule"` i.e. <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0002772"><code>"EFO:0002772"</code></a> or `"single cell library construction"` i.e. <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0010183"><code>"EFO:0010183"</code></a>. Recommended values for commonly-used assays:
    * `10x 3' v2` corresponds to <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0009899"><code>"EFO:0009899"</code></a> 
    * `10x 3' v3` corresponds to <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0009922"><code>"EFO:0009922"</code></a> 
    * `10x 5' v1` corresponds to <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0011025"><code>"EFO:0011025"</code></a> 
    * `10x 5' v2` corresponds to <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0009900"><code>"EFO:0009900"</code></a> 
    * `Smart-seq2` corresponds to <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0008931"><code>"EFO:0008931"</code></a> 
    * `Visium Spatial Gene Expression` corresponds to <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0010961"><code>"EFO:0010961"</code></a> 


### assay

* **column** `assay`
* **dtype:** string
* **value:** This MUST be the human-readable term which corresponds to the value of <code>disease_ontology_term_id</code>. The ontology term and ontology term ID MUST match.



### tissue_type

* **column** `tissue_type`
* **dtype:** string
* **value:** This MUST be one of the following strings: <code>"tissue"</code>, <code>"organoid"</code>, or <code>"cell culture"</code>.



### tissue_ontology_term_id

* **column** `tissue_ontology_term_id`
* **dtype:** string
* **value:** This MUST be the most accurate child of <a href="https://www.ebi.ac.uk/ols4/ontologies/uberon/classes?obo_id=UBERON%3A0001062"><code>UBERON:0001062</code></a> for <i>anatomical entity</i>.<br><br>

### tissue

* **column** `tissue`
* **dtype:** string
* **value:** This MUST be the human-readable term assigned to the value of <code>tissue_ontology_term_id</code>. The ontology term and ontology term ID MUST match.


### Clustering

Users may OPTIONALLY include a single field for clustering within AnnData files, or multiple fields denoting clustering (e.g. different clustering algorithms, multiple resolutions of clustering, etc.)

We therefore REQUIRE that clustering is clearly denoted within the AnnData file if it contains clustering fields.

ScanPy has set an AnnData community standard of defining the `*.obs` value by the type of algorithm. e.g. the function `scanpy.tl.louvain` (documented [here](https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.louvain.html)) by default saves the clustering as `anndata.obs['louvain']`. Similarly, `leiden` (documented [here](https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.leiden.html)) is often encoded as `anndata.obs['leiden']`.

* **column** <code>"cluster"</code> or <code>"cluster + _ + [ALGORITHM_TYPE] + _ + [SUFFIX]"</code> whereby <code>[ALGORITHM_TYPE]</code> and <code>[SUFFIX]</code> are OPTIONAL.
* **dtype:** string
* **value:** 
    * <code>"cluster"</code>: MUST be used to denote clustering in <code>AnnData.obs</code> 
    * <code>[ALGORITHM]</code>: Denotes the algorithm used, e.g. be either "leiden" or "louvain". OPTIONAL.
    * <code>[SUFFIX]</code>: Denotes a descriptive tag informative enough for third-party users; used to distinguish between multiple clusterings. OPTIONAL.
* **example:** <td><code>"cluster_leiden"</code> or <code>"cluster_leiden_broad"</code> or <code>"cluster_louvain_precise3"</code> <code>"cluster_fine"</code>



## Cell Annotation Metadata


### [cellannotation_setname]

The string specified by the user for `[cellannotation_setname]` will be used as the pandas DataFrame column name (key) to encode all columns in `*.obs`.

**Format:** The column name is the string `[cellannotation_setname]` and the values are the strings of `cell_label`. Refer to the fields `cellannotation_setname` and `cell_label` in the JSON Schema.

* **column** `[cellannotation_setname]`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of `cell_label` strings, i.e. any free-text term which the author uses to annotate cells, i.e. the preferred cell label name used by the author.


### [cellannotation_setname]--cell_fullname

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'cell_fullname'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'cell_fullname'`

For example, if the user specified the cell annotation as `broad_cells1`, then the name of the column in the pandas DataFrame will be `broad_cells1--cell_fullname`. 

* **column** `[cellannotation_setname]--cell_fullname`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of `cell_fullname` strings, i.e. the full-length name for the biological entity listed in `cell_label` by the author. 


### [cellannotation_setname]--cell_ontology_term_id

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'cell_ontology_term_id'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'cell_ontology_term_id'`

* **column** `[cellannotation_setname]--cell_ontology_term_id`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of `cell_ontology_term_id` strings, i.e. the ID from either the Cell Ontology (https://www.ebi.ac.uk/ols/ontologies/cl) or from some ontology that extends it by classifying cell types under terms from the Cell Ontology 



### [cellannotation_setname]--cell_ontology_term

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'cell_ontology_term'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'cell_ontology_term'`

* **column** `[cellannotation_setname]--cell_ontology_term`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of `cell_ontology_term` strings, i.e. the human-readable name assigned to the value of `'cell_ontology_term_id'`

### [cellannotation_setname]--rationale

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'rationale'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'rationale'`

* **column** `[cellannotation_setname]--rationale`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of strings maximum length 2000, i.e. each ndarray value must be a single encoding the free-text rationale which users provide as justification/evidence for their cell annotations. 

### [cellannotation_setname]--rationale_dois

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'rationale_dois'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'rationale_dois'`

* **column** `[cellannotation_setname]--rationale_dois`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of strings, i.e. each ndarray value must be a single comma-separated string of valid publication DOIs cited by the author to support or provide justification/evidence/context for 'cell_label'.

* **example:** `'10.1038/s41587-022-01468-y, 10.1038/s41556-021-00787-7, 10.1038/s41586-021-03465-8'`

### [cellannotation_setname]--marker_gene_evidence

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'marker_gene_evidence'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'marker_gene_evidence'`

* **column** `[cellannotation_setname]--marker_gene_evidence`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of strings, i.e. each ndarray value must be a single comma-separated string of gene names explicitly used as evidence for this cell annotation. Each gene MUST be included in the matrix of the AnnData/Seurat file.

* **example:** `'TP53, KRAS, BRCA1'`

### [cellannotation_setname]--synonyms

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'synonyms'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'synonyms'`

* **column** `[cellannotation_setname]--synonyms`
* **index** Cell barcode names
* **dtype:** string
* **value:** ndarray of strings, i.e. each ndarray value must be a single comma-separated string of synonyms for `cell_label`

* **example:** `'neuroglial cell, glial cell, neuroglia'`


# `var` and `raw.var` (Gene Metadata)

CAP requires that gene names by ENSEMBL terms. These MUST be encoded in the [index](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.index.html) of the `var` fields following the [AnnData standard](https://anndata.readthedocs.io/en/latest/generated/anndata.AnnData.html). 

(Note that `var` is a `pandas.DataFrame` object. The gene names MUST be used to index these rows, i.e. `pandas.DataFrame.index`.)

Note that the UI will convert the ENSEMBL terms to common gene names based on the organism specified. We currently support `Homo sapiens` and `Mus musculus`. 

If there are other species you wish to upload to CAP, please contact `support@celltpye.info` and we will work to accommodate your request.


# `obsm` (Embeddings)

Users MUST include at least one two-dimensional embedding, which must be encoded by `X_`. 

That is, given a data matrix `X` of the dimension `(#observations, #variables)` data matrix, the dimensions of all embeddings MUST be `(#observations, 2)`. 

(Embeddings of higher dimensions >=2 may be encoded in the AnnData file, but these embeddings will not be accessible via the CAP UI.)

The format for the name of embeddings in `obsm` is RECOMMENDED to be the following format: 

<code>"X + _ + [EMBEDDING_TYPE] + _ + [SUFFIX]"</code>

whereby
* <code>"X_"</code>: MUST be used to denote embeddings in <code>AnnData.obsm</code>. REQUIRED.
* <code>[EMBEDDING TYPE]</code>: MUST denote the algorithm used to generate the embedding (e.g. `UMAP`, `tSNE`, `pca`, etc.). REQUIRED.
* <code>[SUFFIX]</code>: Denotes a descriptive tag informative enough for third-party users; used to distinguish between multiple embeddings of the same type. OPTIONAL.

**examples:** <td><code>"X_pca"</code>, <code>"X_tsne"</code>, <code>"X_tSNE"</code>, <code>"X_umap"</code>, <code>"X_UMAP_nneigbors15"</code>, <code>"X_umap_2"</code>




# uns (Dataset metadata)

**NOTE:** Each time a cell annotation `cellannotation_setname` is modified, these values potentially change. 

## cellannotation_schema_version

Key-value pair in the `uns` dictionary

* **key:** `cellannotation_schema_version`
* **type:** string
* **value:** The schema version, the cell annotation open standard. 
This versioning MUST follow the format `'[MAJOR].[MINOR].[PATCH]'` as defined by Semantic Versioning 2.0.0, https://semver.org/. Current version MUST follow 0.1.0

## cap_dataset_timestamp

Key-value pair in the `uns` dictionary

* **key:** `cap_dataset_timestamp`
* **type:** string
* **value:** The timestamp of the dataset published on CAP. This MUST be a string in the format `%yyyy-%MM-%dd'T'%hh:%mm:%ss`.

## cap_dataset_version

Key-value pair in the `uns` dictionary

* **key:** `## cap_dataset_version`
* **type:** string
* **value:** The version for all cell annotations published (per dataset) on CAP. This MUST be a string. The recommended versioning format is `'[MAJOR].[MINOR].[PATCH]'` as defined by Semantic Versioning 2.0.0, https://semver.org/

## cap_dataset_title

Key-value pair in the `uns` dictionary

* **key:** `cap_dataset_title`
* **type:** string
* **value:** The title of the dataset on CAP. This MUST be less than or equal to 200 characters.


## cap_dataset_description

Key-value pair in the `uns` dictionary

* **key:** `cap_dataset_description`
* **type:** string
* **value:** The description of the dataset on CAP. This MUST be less than or equal to N characters.


## cap_publication_title

Key-value pair in the `uns` dictionary

* **key:** `cap_publication_title`
* **type:** string
* **value:** The title of the publication on CAP. (NOTE: the term "publication" refers to the workspace published on CAP with a version and timestamp.) This MUST be less than or equal to N characters.


## cap_publication_description

Key-value pair in the `uns` dictionary

* **key:** `cap_publication_description`
* **type:** string
* **value:** The description of the publication on CAP. (NOTE: the term "publication" refers to the workspace published on CAP with a version and timestamp.) This MUST be less than or equal to N characters.


## cap_publication_url

Key-value pair in the `uns` dictionary

* **key:** `cap_workspace_url`
* **type:** string
* **value:** A persistent URL of the publication on CAP. (NOTE: the term "publication" refers to the workspace published on CAP with a version and timestamp.) This MUST be less than or equal to N characters.


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


## cellannotation_metadata

Python dictionary within the `uns` dictionary


#### [cellannotation_setname]--metadata

* **key:** `[cellannotation_setname]--metadata`
* **type:** python dictionary
* **value:** the rest of the dictionary as defined below

#### description

* **key:** `'description'`
* **type:** string
* **value:** Description of the `cellannotation_setname` created. This is free-text for collaborators and third-parties to understand the context/background for the creation of this cell annotation set. We STRONGLY recommend this field be descriptive for other scientists unfamiliar with this project to understand why this set of cell annotations exist. This MUST be less than or equal to N characters.


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

