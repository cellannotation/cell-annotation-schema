## User Stories

### General

1. As a user/editor of data annotated using the cell annotation standard, I want to be able to view annotations
 of cell sets in tabular form, either as a single table, or as a set of linked tables.
Links between tables should be easy to understand (e.g. relying on obvious common keys)
   * Solutions: 
       * If robust representation of annotations requires nested data structures, we need SOPs and tooling
  for flattening & some UX testing of the resulting tables
       * We also require these nested data structures to map to bioinformatic files, i.e. AnnData files. The standard bioinformatic tooling needs to work with these files.
     
2. As a consumer of annotated data I wish to understand the rationale for annotation in order to judge its accuracy.  Rationale might include marker genes whose expression or absence was used as evidence for annotation, gene set enrichment evidence (e.g. with GO) or the nature of automated annotation, e.g.  annotation transfer using Azimuth from some specified reference dataset.


### CxG portal user (could be made more general)

1. As a CxG portal user, I want to be able to view embeddings (UMAP, tSNE) and select terms using 
the abbreviations in the accompanying paper so that I can easily cross-reference
the paper content with the data/visualizations/analysis I see in the browser.

2. As a CxG portal user, I want to render/select by any cell (type) label or synonym

### Integration efforts ("Atlas building efforts")

1. As a participant in integration efforts, I want the full names of cell types to be used
for clarity and to enable building consensus on cell type names.
   * Possible solutions: Mandate full names. But see CXG1; Include field for specifying full names,
specifying that this must be filled in if an abbreviation is used for the primary annotation label.

2. As a participant in integration efforts producing reference standards for cell type definitions,
I want to link official names and synonyms to reference data (cell sets) and/or reference marker lists.

4.  As a participant in integration efforts I want mechanisms to standardise names and what they refer to
 reference data, defining markers), external descriptions.
    * Solution: Ontology annotation + ability to refine ontologies to take into account the results of integration efforts.

5. Integration efforts for the HCA will accumulate the annotations of disparate research labs and biologists. Given this reality, the following cases could arise:
* (A) research groups define the SAME molecular signatures with the SAME terms
* (B) research groups define the SAME molecular signatures with DIFFERENT terms
* (C) research groups define DIFFERENT molecular signatures with the SAME terms

As a participant in the integration efforts for the HCA, I need to understand how these individual labs defined the cell annotations within their datasets. 
* (i) I need to understand the biological rationale used to label these cells with this biological entity
* (ii) I need to have the ability to compare and contrast how individual researchers define this same biological entity, both based on the terms (e.g. shared terms or shared synonyms) and the rationale provided as biomarkers (e.g. the shared marker genes).

Given these N datasets composing the atlas, I can therefore derive a "consensus annotation" to be used for the integrated object (which by definition should have fairly broad cell types) which can be used for the annotation jamborees.


### Resource/portal builder

1. As a builder of resources including many sources of data (e.g. data portals, knowledge bases, knowledge graphs)
I want accurate annotations with standardised cell ontology terms linked to widely used symbols/synonyms in order
to drive search, query and browsing on my resource.

### Annotation transfer 

1. As a consumer of transferred annotations I want a record of what algorithm was used, which version
and what reference data (or reference cluster) was used (where applicable).

2. As a builder of resources including many sources of data (data portals, knowledge bases, knowledge graphs)
I want transferred annotations to include cell ontology terms that I can use to index data and drive searching/browsing on the site.


### BICAN 

1. As a Brain Initiative taxonomy developer I want an easy way to build 
and edit a simple hierarchy of cell sets, built on a fixed set of (leaf node) clusters.
In this simple hierarchy there are a fixed number of levels (ranks) and all cell 
sets have only one parent (subsuming) cell set.

2.  As a Brain Initiative taxonomy developer I want to be able to record the predicted 
neurotransmitter(s) for all clusters using a simple, agreed shorthand.

3.  As a Brain Initiative taxonomy developer, I want to be able to keep track of
annotation transfer from multiple sources onto individual nodes in my taxonomy - 
tracking the transferred label, the algorithm, and the reference taxonomy and dataset.  
I want this to be stable to changes in nomenclature in the reference taxonomy.

4. As a Brain Initiative taxonomy developer, I want to be able to record some location mappings
for cell types, using Allen Brain Atlas terms (from standard structure graphs/parcellations)
along with evidence for these mappings.

6.  As a Brain Initiative taxonomy developer I want to share clearly defined versions of 
my taxonomy with other members of the consortium, prior to publication.

7. As a consumer of brain initiative taxonomies, I want to see the (marker) evidence for
mappings to generally known cell types.






