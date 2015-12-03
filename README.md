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
    - Passage index (perhpas not necessary)
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

## Specific

### Question Processing
#### Query formulation

- 中心词
- 其它名词
- 非停用动词
- 其它（序数词，状语等）

#### Question Classification

Classification Process: Rules + Learning
- 规则 Rules
    - Prejudge and construct training set
- 学习 Learning
    - Training use 'rules result'
    - Use word2vec vectors of `中心词`,`疑问词` as features
    - Use classifiers to decide categories

LDA?

规则
2. 疑问词“谁”－0
4. 疑问词“哪一年”－1
9. 疑问词“哪里”－2
3. 疑问词“多少”－3
1. 疑问词“第几”－3
3. 疑问词“多少倍”－3
4. 中心词“作者”－0
5. 中心词“校长”－0
5. 中心词“国家”－2
6. 中心词“城市”－2
6. 中心词“地点”－2
7. 中心词“海拔”－3
7. 中心词“大学”－4
8. 中心词“少数民族”－5
8. 中心词“语言”－5

Use `Scikit-learn`

- 学习－分类
    - **类别**
        - 0-名字，
        - 1-时间（含年份），
        - 2-地点（含国家、省份）
        - 3-数字（含序数），
        - 4-学校及其它机构，
        - 5-其它名词
- 学习－特征
    - ![](img/Q_classification_L.png)
    - 中文情况考虑因素
        - "是"前的词（中心词）
        - 命名实体
        - （非停用词的？）动词
        - 词，词性
    - **构造**
        - 疑问词
        - 中心词
            - “是”出现，则为之前的名词（中心词），否则，为疑问词后的名词
