# QA
A Chinese Question and Answer System

## Stages

- Question Processing
    - Word segmentation
    - Output:
        1. **Query formulation**
            - Keywords: 中心词，名词，其他词
			- 命名实体
			- 主谓宾
        2. Question **Classification**
            - Rules / Template matching
			- Parser -> wh-words is ATT to which word => question type
            - Learning

- Passage Retrieval
    - 篇章分词
    - 建立倒排索引
    - Input: Keywords
    - Output: Related Passages
        - 计算篇章的权重
        - 排序，输出前面的篇章

- Answer Extraction
    - Algorithm
        - N-gram?
        - Template matching? **Template learning** using Search Engines?
    - Output: set of pairs {(answer, passage), ...}

- Answer Ranking
    - Rank (answer, passage) pairs
    - Produce final answer(s)
