# QA
A Chinese Question and Answer System

## Stages

- Question Processing
    - Word segmentation
    - Output:
        1. **Query formulation**
            - Keywords
        2. Question **Classification**
            - Learning? Rules?

- Passage Retrieval
    - Passage word segmentation
    - Passage index
    - Input: Keywords
    - Output: Possible paragraphs / sentences (with order of possibilities?)
        - Filter according to entities and question classification
        - Sort using rules or learning

- Answer Extraction
    - Algorithm
        - N-gram?
        - Template matching? **Template learning** using Search Engines?

- (Optional) Answer Refinement
    - Perhaps another filtering and sorting of answer candidates
