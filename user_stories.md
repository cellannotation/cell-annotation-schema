## User Stories

### General

1. As a user/editor of data annotated using the cell annotation standard, I want to be able to view annotations
 of of cell sets in tabular form, either as a single table, or as a set of linked tables.
Links between tables should be easy to understand (e.g. relying on obvious common keys)
   * Solutions: If robust representation of annotations requires nested data structures, we need SOPs and tooling
  for flattening & some UX testing of the resulting tables


### CxG portal user (could be made more general)

1. As a CxG portal user, I want to be able to view embeddings (UMAP, tSNE) and select terms using 
the abbreviations in the accompanying paper so that I can easily cross-reference
the paper content with the data/visualizations/analysis I see in the browser.

2. As a CxG portal user, I want to render/select by any cell (type) label or synonym

### Integration efforts

1. As a participant in integration efforts, I want the full names of cell types to be used
for clarity and to enable building consensus on cell type names.
   * Possible solutions: Mandate full names. But see CXG1; Include field for specifying full names,
specifying that this must be filled in if an abbrevation is used for the primary annotation label.

2. As a participant in integration efforts producing reference standards for cell type defintions,
I want to link official names and synonyms to reference data (cell sets) and/or reference marker lists.

4.  As a participant in integration efforts I want mechanisms to standardise names and what they refer to
 reference data, defining markers), external descriptions.
    * Solution: Ontology annotation + abiltiy to refine ontologies to take into account the results of integration efforts.


### Resource/portal builder

1. As a builder of resources including many sources of data (data portals, knowledge bases, knowledge graphs )
I want accurate annoations with standardised cell ontology terms linked to widely used symbols/synonyms in order
to drive search, query and browsing on my resource.

### Annotation transfer 

1. As a consumer of transferred annotations I want a record of what algo was used, what 
and what reference data (or reference cluster) was used (where that makes sense).

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

4. As a Brain Iniatitive taxonomy developer, I want to be able to record soma location mappings
for cell types, using Allan Brain Atlas terms (from standard structuregraphs/parcellations)
along with evidence for these mappings.

6.  As a Brain Initiative taxonomy developer I want to share clearly defined versions of 
my taxonomy with other members of the consortium, prior to publication.

7. As a consumer of brain initiative taxonomies, I want to see the (marker) evidence for
mappings to generally known cell types.
