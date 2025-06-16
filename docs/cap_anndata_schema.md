# CAP Encoding for AnnData file

Contact: [...]

Version: 1.0.2  

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


### organism_ontology_term_id


<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>organism_ontology_term_id</code></td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This MUST be a child of <a href="https://www.ebi.ac.uk/ols4/ontologies/ncbitaxon/classes?obo_id=NCBITaxon%3A33208"><code>NCBITaxon:33208</code></a> for <i>Metazoa</i>.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'NCBITaxon:9606'</code> or <code>'NCBITaxon:10090'</code></td>
	</tr>
</tbody></table>


### organism

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>organism</code></td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This MUST be the human-readable term assigned to the value of <code>organism_ontology_term_id</code>. The ontology term and ontology term ID MUST match.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'Homo sapiens'</code> or <code>'Mus musculus'</code></td>
	</tr>
</tbody></table>


### disease_ontology_term_id

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>disease_ontology_term_id</code></td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This MUST be a MONDO term or <a href="https://www.ebi.ac.uk/ols4/ontologies/pato/classes?obo_id=PATO%3A
0000461"><code>'PATO:0000461'</code></a> for <i>normal</i> or <i>healthy</i>.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'MONDO:0004975'</code> or <code>'MONDO:0018177'</code> or <code>'PATO:0000461'</code></td>
	</tr>
</tbody></table>


### disease

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>disease</code></td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This MUST be the human-readable term which corresponds to the value of <code>disease_ontology_term_id</code>. The ontology term and ontology term ID MUST match.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'Alzheimer's Disease'</code> or <code>'Adult Brain Glioblastoma'</code> or <code>'normal'</code></td>
	</tr>
</tbody></table>

### assay_ontology_term_id

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>assay_ontology_term_id</code></td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This MUST be an EFO term and SHOULD be the most accurate EFO term for this assay. The two options are more specific terms under <code>"assay by molecule"</code> i.e. <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0002772"><code>'EFO:0002772'</code></a> or <code>"single cell library construction"</code> i.e. <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0010183"><code>'EFO:0010183'</code></a>. <br><br> Recommended values for commonly-used assays: 		<ul>
			<li><code>'10x 3' v2'</code>corresponds to <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0009899"><code>'EFO:0009899'</code></a></li>
  			<li><code>'10x 3' v3'</code>corresponds to <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0009922"><code>'EFO:0009922'</code></a></li>
			<li><code>'10x 5' v1'</code>corresponds to <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0011025"><code>'EFO:0011025'</code></a></li>
  			<li><code>'10x 5' v2'</code>corresponds to <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0009900"><code>'EFO:0009900'</code></a></li>
  			<li><code>'Smart-seq2'</code>corresponds to <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0008931"><code>'EFO:0008931'</code></a></li>
  			<li><code>'Visium Spatial Gene Expression'</code>corresponds to <a href="https://www.ebi.ac.uk/ols4/ontologies/efo/classes?obo_id=EFO%3A0010961"><code>'EFO:0010961'</code></a></li>
		 </ul>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'EFO:0009922'</code> or <code>'EFO:0008931'</code></td>
	</tr>
</tbody></table>


### assay

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>assay</code></td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This MUST be the human-readable term which corresponds to the value of <code>assay_ontology_term_id</code>. The ontology term and ontology term ID MUST match.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'10x 3' v3'</code> or <code>'Smart-seq2'</code></td>
	</tr>
</tbody></table>


### tissue_ontology_term_id

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>tissue_ontology_term_id</code></td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This MUST be the most accurate child of <a href="https://www.ebi.ac.uk/ols4/ontologies/uberon/classes?obo_id=UBERON%3A0001062"><code>UBERON:0001062</code></a> for <i>anatomical entity</i>.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'UBERON:0000451'</code> or <code>'UBERON:0000966'</code></td>
	</tr>
</tbody></table>

### tissue

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>tissue</code></td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This MUST be the human-readable term assigned to the value of <code>tissue_ontology_term_id</code>. The ontology term and ontology term ID MUST match.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'prefrontal cortex'</code> or <code>'retina'</code></td>
	</tr>
</tbody></table>


### Clustering

Users may OPTIONALLY include a single field for clustering within AnnData files, or multiple fields denoting clustering, e.g. different clustering algorithms, multiple resolutions of clustering, etc.

We therefore REQUIRE that clustering is clearly denoted within the AnnData file if it contains clustering fields.

ScanPy has set an AnnData community standard of defining the `*.obs` value by the type of algorithm. e.g. the function `scanpy.tl.louvain` (documented [here](https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.louvain.html)) by default saves the clustering as `anndata.obs['louvain']`. Similarly, `leiden` (documented [here](https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.leiden.html)) is often encoded as `anndata.obs['leiden']`.

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>'cluster'</code>, <code>'leiden'</code>, <code>'louvain'</code> or <code>'cluster + _ + [ALGORITHM_TYPE] + _ + [SUFFIX]'</code> whereby <code>[ALGORITHM_TYPE]</code> and <code>[SUFFIX]</code> are OPTIONAL.</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td><ul><li><code>'cluster'</code>, <code>'leiden'</code> or <code>'louvain'</code>: MUST be used to denote clustering in <code>AnnData.obs</code> 
        </li>
        <li><code>[ALGORITHM]</code>: Denotes the algorithm used, e.g. be either 'leiden' or 'louvain'. OPTIONAL.
        </li>
        <li><code>[SUFFIX]</code>: Denotes a descriptive tag informative enough for third-party users; used to distinguish between multiple clusterings. OPTIONAL.
        </li></ul>
        </td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>no</td>
	</tr>
	<tr>
  		<td><b>example column name</b></td>
  		<td><code>'cluster_leiden'</code> or <code>'cluster_leiden_broad'</code> or <code>'louvain'</code> or <code>'leiden'</code></td>
	</tr>
	<tr>
  		<td><b>example value</b></td>
  		<td><code>'0'</code> or <code>'1'</code> or <code>'2'</code></td>
	</tr>
</tbody></table>



## Cell Annotation Metadata


### [cellannotation_setname]

The string specified by the user for `[cellannotation_setname]` will be used as the pandas DataFrame column name (key) to encode the following cell annotation metadata columns in `*.obs`.

NOTE: A dataset may have multiple sets of cell annotations each with a  cooresponding set of cell annotation metadata, e.g. <code>'cell_type'</code> and <code>'broadclustering_celltype'</code>. 

NOTE: Certain keywords have been reserved for annotating cells:

- The term `'doublets'` is reserved for encoding cells defined as doublets based on some computational analysis. By “doublets”, we refer to the sequencing artifact within droplet-based protocols whereby two or more cells are tagged with the same barcode.
- The term `'junk'` is reserved for encoding cells that failed sequencing for some reason, e.g. few genes detected, high fraction of mitochondrial read. Researchers have found such a generic term useful. 
- The term `'unknown'` is specifically reserved for cells which the author did not know how to annotate with a biological entity. It is a generic term meaning “I do not know”. 

**Format:** The column name is the string `[cellannotation_setname]` and the values are the strings of `cell_label`. Refer to the fields `cellannotation_setname` and `cell_label` in the JSON Schema.

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>Any free-text term which the author uses to annotate cells, the preferred cell label name used by the author.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'HBC2'</code> or <code>'rod bipolar'</code> or <code>'doublets'</code> or <code>'junk'</code></td>
	</tr>
</tbody></table>


### [cellannotation_setname]--cell_fullname

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'cell_fullname'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'cell_fullname'`

For example, if the user specified the cell annotation as `broad_cells1`, then the name of the column in the pandas DataFrame will be `broad_cells1--cell_fullname`. 

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--cell_fullname</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The full-length name for the biological entity listed in <code>[cellannotation_setname]</code> by the author. </td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'rod bipolar'</code></td>
	</tr>
</tbody></table>


### [cellannotation_setname]--cell_ontology_exists

**format:** The column name is the string prefix `[cellannotation_setname]--` concatenated with the string value `cell_ontology_exists`, i.e. `[cellannotation_setname] + '--' + 'cell_ontology_exists'`

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--cell_ontology_exists</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>boolean</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>Boolean value in Python (either True or False).</td>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr> 
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'True'</code></code></td>
	</tr>
</tbody></table>


### [cellannotation_setname]--cell_ontology_term_id

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'cell_ontology_term_id'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'cell_ontology_term_id'`

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--cell_ontology_term_id</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This MUST be a term from either the <a href="https://www.ebi.ac.uk/ols/ontologies/cl"> Cell Ontology</a> or from some ontology that extends it by classifying cell types under terms from the Cell Ontology e.g. the <a href="https://www.ebi.ac.uk/ols/ontologies/pcl"> Provisional Cell Ontology</a> or the <a href="https://www.ebi.ac.uk/ols4/ontologies/fbbt"> Drosophila Anatomy Ontology (DAO).</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'CL:0000751'</code></td>
	</tr>
</tbody></table>


### [cellannotation_setname]--cell_ontology_term

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'cell_ontology_term'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'cell_ontology_term'`

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--cell_ontology_term</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The human-readable name assigned to the value of <code>'cell_ontology_term_id'</code>.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'rod bipolar cell'</code></td>
	</tr>
</tbody></table>

### [cellannotation_setname]--rationale

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'rationale'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'rationale'`

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--rationale</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The free-text rationale which users provide as justification/evidence for their cell annotations.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'This cell was annotated with [blank] given the canonical markers in the field [X], [Y], [Z]. We noticed [X] and [Y] running differential expression.'</code></td>
	</tr>
</tbody></table>

### [cellannotation_setname]--rationale_dois

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'rationale_dois'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'rationale_dois'`

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--rationale_dois</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>Comma-separated string of valid publication DOIs cited by the author to support or provide justification/evidence/context for <code>cell_label</code>.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>no</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'10.1038/s41587-022-01468-y, 10.1038/s41556-021-00787-7, 10.1038/s41586-021-03465-8'</code></td>
	</tr>
</tbody></table>

### [cellannotation_setname]--marker_gene_evidence

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'marker_gene_evidence'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'marker_gene_evidence'`

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--marker_gene_evidence</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>Comma-separated string of gene names explicitly used as evidence for this cell annotation. Each gene MUST be included in the matrix of the AnnData/Seurat file.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'TP53, KRAS, BRCA1'</code></td>
	</tr>
</tbody></table>


### [cellannotation_setname]--canonical_marker_genes

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'canonical_marker_genes'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'canonical_marker_genes'`

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_setname]--canonical_marker_genes</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>Comma-separated string of gene names considered to be canonical markers for the biological entity used in the cell annotation.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'GATA3, CD3D, CD3E'</code></td>
	</tr>
</tbody></table>


### [cellannotation_setname]--synonyms

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'synonyms'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'synonyms'`

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--synonyms</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>Comma-separated string of synonyms for values in <code>[cellannotation_setname]</code>. Abbreviations are acceptable.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'neuroglial cell, glial cell, neuroglia'</code> or <code>'amacrine cell'</code> or <code>'FMB cell'</code></td>
	</tr>
</tbody></table>


### [cellannotation_setname]--category_fullname

**Format:** The column name is the string prefix `[cellannotation_setname]--` concatenated with the string value `category_fullname`, i.e. `[cellannotation_setname] + '--' + 'category_fullname'`. This MUST be the full-length name for the biological entity, not an abbreviation.

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--category_fullname</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>A single value of the category/parent term for the cell label value in  <code>[cellannotation_setname]</code>.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'ON-bipolar cell'</code></td>
	</tr>
</tbody></table>

### [cellannotation_setname]--category_cell_ontology_exists

**Format:** The column name is the string prefix `[cellannotation_setname]--` concatenated with the string value `category_cell_ontology_exists`, i.e. `[cellannotation_setname] + '--' + 'category_cell_ontology_exists'`

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--category_cell_ontology_exists</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>boolean</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>Boolean value in Python (either True or False).</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'True'</code></td>
	</tr>
</tbody></table>

### [cellannotation_setname]--category_cell_ontology_term_id

**Format:** The column name is the value `[cellannotation_setname]` concatenated with the string `'synonyms'` and two hyphens, i.e. `[cellannotation_setname] + '--' + 'category_cell_ontology_term_id'`

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--category_cell_ontology_term_id</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The ID from either the <a href="https://www.ebi.ac.uk/ols/ontologies/cl"> Cell Ontology </a> or from some ontology that extends it by classifying cell types under terms from the Cell Ontology.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'CL:0000749'</code></td>
	</tr>
</tbody></table>


### [cellannotation_setname]--category_cell_ontology_term

**format:** The column name is the string prefix `[cellannotation_setname]--` concatenated with the string value `category_cell_ontology_term`, i.e. `[cellannotation_setname] + '--' + 'category_cell_ontology_term'`

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--category_cell_ontology_term</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The human-readable name assigned to the value of <code>'category_cell_ontology_term_id'</code>.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'ON-bipolar cell'</code></td>
	</tr>
</tbody></table>


### [cellannotation_setname]--cell_ontology_assessment

**Format:** The column name is the string prefix `[cellannotation_setname]--` concatenated with the string value `cell_ontology_assessment`, i.e. `[cellannotation_setname] + '--' + 'cell_ontology_assessment'`

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--cell_ontology_assessment</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>Free-text field for researchers to express disagreements with any aspect of the Cell Ontology for this cell annotation.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>no</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'Amacrine cell should have four child terms: glycinergic, GABAergic, GABAergic Glycinergic amacrine cells and non-GABAergic non-glycinergic amacrine cells; which then contain their cooresponding child terms'</code></td>
	</tr>
</tbody></table>

### [cellannotation_setname]--confidence_score

**Format:** The column name is the string prefix `[cellannotation_setname]--` concatenated with the string value `confidence_score`, i.e. `[cellannotation_setname] + '--' + 'confidence_score'`

<table><tbody>
	<tr>
  		<td><b>column</b></td>
  		<td><code>[cellannotation_set]--confidence_score</code></td>
	</tr>
	<tr>
  		<td><b>index</b></td>
  		<td>Cell barcode names</td>
	</tr>
	<tr>
  		<td><b>dtype</b></td>
  		<td>float</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>A float number in [0,1] range corresponding to the model's internal probability that the predicted label is correct.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>no</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>0.45</code></td>
	</tr>
</tbody></table>

# `var` and `raw.var` (Gene Metadata)

CAP requires that gene names be provided by ENSEMBL terms. These MUST be encoded in the [index](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.index.html) of the `var` fields following the [AnnData standard](https://anndata.readthedocs.io/en/latest/generated/anndata.AnnData.html). 

NOTE: `var` is a `pandas.DataFrame` object. ENSEMBL terms MUST be used to index these rows, i.e. `pandas.DataFrame.index`.

NOTE: the UI will convert the ENSEMBL terms to common gene names based on the organism specified. We currently support `Homo sapiens` and `Mus musculus`. 

If there are other species you wish to upload to CAP, please contact `support@celltpye.info` and we will work to accommodate your request.


# `obsm` (Embeddings)

Users MUST include at least one two-dimensional embedding, which must be encoded by `X_`. 

That is, given a data matrix `X` of the dimension `(#observations, #variables)` data matrix, the dimensions of all embeddings MUST be `(#observations, 2)`. 

NOTE: Embeddings of higher dimensions >=2 may be encoded in the AnnData file, but these embeddings will not be accessible via the CAP UI.

The format for the name of embeddings in `obsm` is RECOMMENDED to be the following format: 

<code>'X + _ + [EMBEDDING_TYPE] + _ + [SUFFIX]'</code>

whereby:
* <code>'X_'</code>: MUST be used to denote embeddings in <code>AnnData.obsm</code>. REQUIRED.
* <code>[EMBEDDING TYPE]</code>: MUST denote the algorithm used to generate the embedding (e.g. `UMAP`, `tSNE`, `pca`, etc.). REQUIRED.
* <code>[SUFFIX]</code>: Denotes a descriptive tag informative enough for third-party users; used to distinguish between multiple embeddings of the same type. OPTIONAL.

**examples:** <td><code>'X_pca'</code>, <code>'X_tsne'</code>, <code>'X_tSNE'</code>, <code>'X_umap'</code>, <code>'X_UMAP_nneigbors15'</code>, <code>'X_umap_2'</code>


# uns (Dataset metadata)

**NOTE:** Each time a cell annotation `cellannotation_setname` is modified, these values potentially change. 

## cellannotation_schema_version

Key-value pair in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>cellannotation_schema_version</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The schema version, the cell annotation open standard. 
This versioning MUST follow the format <code>'[MAJOR].[MINOR].[PATCH]'</code> as defined by <a href="https://semver.org">Semantic Versioning 2.0.0.</a> Current version MUST follow 0.1.0</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>software</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'0.1.0'</code></td>
	</tr>
</tbody></table>


## publication_timestamp

Key-value pair in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>publication_timestamp</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The timestamp of the dataset published on CAP. This MUST be a string in the format <code>%yyyy-%MM-%dd'T'%hh:%mm:%ss</code>.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>software</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'2023-11-21T04:12:36'</code></td>
	</tr>
</tbody></table>

## publication_version

Key-value pair in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>publication_version</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string of <code>'v' + '[integer]'</code></td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This versioning MUST follow the format <code>'v' + '[integer]'</code>, whereby newer versions must be naturally incremented.</td>
	</tr>
  		<td><b>source</b></td>
  		<td>software</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'v1'</code> or <code>'v3'</code></td>
	</tr>
</tbody></table>

## title

Key-value pair in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>title</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The title of the dataset on CAP. This MUST be less than or equal to 200 characters.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'Human retina cell atlas - retinal ganglion cells'</code></td>
	</tr>
</tbody></table>


## description

Key-value pair in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>description</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The description of the dataset on CAP.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'A total of 15 retinal ganglion cell clusters were identified from over 99K retinal ganglion cell nulcei in the current atlas. Utilizing previoulsy characterized markers from macaque, 5 clusters can be annotated.'</code></td>
	</tr>
</tbody></table>

## cap_dataset_url

Key-value pair in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>cap_dataset_url</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>A persistent URL of the dataset on CAP.</td>
	</tr>
  		<td><b>source</b></td>
  		<td>software</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'https://celltype.info/CAP_DataCuration/A-Single-Cell-Transcriptome-Atlas-of-the-Human-Pancreas/1/dataset/20'</code></td>
	</tr>
</tbody></table>


## cap_publication_title

Key-value pair in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>cap_publication_title</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The title of the publication on CAP. This MUST be less than or equal to 200 characters.<br><br>NOTE: the term "publication" refers to the workspace published on CAP with a version and timestamp.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'Integrated multi-omics single cell atlas of the human retina'</code></td>
	</tr>
</tbody></table>


## cap_publication_description

Key-value pair in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>cap_publication_description</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The description of the publication on CAP.<br><br>NOTE: the term "publication" refers to the workspace published on CAP with a version and timestamp.</td>
	</tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td>Similar to an abstract in a scientific publication, the <code>cap_publication_description</code> should provide enough information for other scientists unfamilar with the work.</td>
	</tr>
</tbody></table>

## cap_publication_url

Key-value pair in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>cap_publication_url</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>A persistent URL of the publication on CAP.<br><br>NOTE: the term "publication" refers to the workspace published on CAP with a version and timestamp.</td></td>
	</tr>
  		<td><b>source</b></td>
  		<td>software</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'https://celltype.info/CAP_DataCuration/A-Single-Cell-Transcriptome-Atlas-of-the-Human-Pancreas/1'</code></td>
	</tr>
</tbody></table>

## authors_list

Key-value pair in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>authors_list</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This field stores a list of CAP users who are included in the CAP project as collaborators, regardless of their specific role (Viewer, Editor, or Owner).</td>
	</tr>
  		<td><b>source</b></td>
  		<td>software</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'['John Smith', 'Cody Miller', 'Sarah Jones']'</code></td>
	</tr>
</tbody></table>

## author_name

Key-value pair in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>author_name</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This MUST be a string in the format <code>[FIRST NAME] [LAST NAME]</code>.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'John Smith'</code></td>
	</tr>
</tbody></table>


## author_contact

Key-value pair in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>author_contact</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This MUST be a valid email address of the author.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'jsmith@university.edu'</code></td>
	</tr>
</tbody></table>

## author_orcid

Key-value pair in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>author_orcid</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>This MUST be a valid ORCID for the author.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'0000-0002-3843-3472'</code></td>
	</tr>
</tbody></table>

## hierarchy

A dictionary in the `uns` dictionary

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>hierarchy</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>python dictionary</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
		<td>An ordering of cell level groupings from <code>[cellannotation_setname]</code> where smaller numbers are broader types. E.g. {"Class":0, "Subclass": 1, "cell_type": 2}</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>no</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'hierarchy': {'Class':0, 'Subclass':1, 'Group':2, 'cluster_id':3}</code></td>
	</tr>
</tbody></table>

## cellannotation_metadata

Python dictionary within the `uns` dictionary, with the key the string `[cellannotation_setname]`


#### cellannotation_metadata

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>[cellannotation_setname]</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>python dictionary</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The rest of the dictionary as defined below.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'{'cell_type': {'annotation_method':'algorithmic', ...}}'</code></td>
	</tr>
</tbody></table>

#### description

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>'description'</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>Description of the <code>cellannotation_set</code> created. This is free-text for collaborators and third-parties to understand the context/background for the creation of this cell annotation set.<br><br> We STRONGLY recommend this field be descriptive for other scientists unfamiliar with this project to understand why this set of cell annotations exist.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'Cell annotations based on resolution broad clustering using the Leiden algorithm.'</code></td>
	</tr>
</tbody></table>

#### annotation_method

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>'annotation_method'</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td><code>'algorithmic'</code>, <code>'manual'</code>, or <code>'both'</code><br><br>NOTE: If <code>'algorithmic'</code> or <code>'both'</code>, more details are required. If <code>'manual'</code>, the values in the following 'algorithm_' and 'reference_' fields will be <code>'NA'</code>.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'algorithmic'</code> or <code>'manual'</code> or <code>'both'</code></td>
	</tr>
</tbody></table>

#### algorithm_name

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>'algorithm_name'</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The name of the algorithm used.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'scArches'</code> or if <code>'manual'</code> then <code>'NA'</code></td>
	</tr>
</tbody></table>

#### algorithm_version

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>'algorithm_version'</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The string of the algorithm's version, which is typically in the format <code>'[MAJOR].[MINOR]'</code>, but other versioning systems are permitted based on the algorithm's versioning.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'0.5.9'</code>or if <code>'manual'</code> then <code>'NA'</code></td>
	</tr>
</tbody></table>

#### algorithm_repo_url

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>'algorithm_repo_url'</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The string of the URL of the version control repository associated with the algorithm used (if applicable). It MUST be a string of a valid URL.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>yes</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'https://github.com/theislab/scarches'</code>or if <code>'manual'</code> then <code>'NA'</code></td>
	</tr>
</tbody></table>


#### reference_location

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>'reference_location'</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>The string of the URL pointing to the reference dataset.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>no</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'https://figshare.com/projects/Tabula_Muris_Senis/64982'</code>or if <code>'manual'</code> then <code>'NA'</code></td>
	</tr>
</tbody></table>

#### reference_description

<table><tbody>
	<tr>
  		<td><b>key</b></td>
  		<td><code>'reference_description'</code></td>
	</tr>
	<tr>
  		<td><b>type</b></td>
  		<td>string</td>
	</tr>
	<tr>
  		<td><b>value</b></td>
  		<td>Free-text description of the reference used for automated annotation for this cell annotation set. Users are welcome to write out context which may be useful for other researchers.</td>
	</tr>
	<tr>
  		<td><b>source</b></td>
  		<td>file or UI</td>
	</tr>
	<tr>
  		<td><b>required for publication on CAP</b></td>
  		<td>no</td>
	</tr>
	<tr>
  		<td><b>example</b></td>
  		<td><code>'Tabula Muris Senis: a single cell transcriptomic atlas across the life span of Mus musculus which includes data from 18 tissues and organs.'</code>or if <code>'manual'</code> then <code>'NA'</code></td>
	</tr>
</tbody></table>

# Appendix: Changelog

schema version 1.0.0 
 <ul>
  <li>Renamed <code>dataset_title</code> to <code>title</code></li>
  <li>Renamed <code>dataset_description</code> to <code>description</code></li>
  <li>Renamed <code>cellannotation_setdescription</code> to <code>description </code></li>
</ul> 

schema version 1.0.1 
 <ul>
  <li>Added <code>hierarchy</code> to <code>uns</code> section</li>
</ul> 

schema version 1.0.2 
 <ul>
  <li>Added <code>[cellannotation_setname]--confidence_score</code> to <code>obs</code> section</li>
</ul> 
