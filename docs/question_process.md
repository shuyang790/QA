# Question Processing
## Query formulation

挑选passage的时候可以选取其中前2-4个作为关键词。

- 中心词
- 其它名词
- 非停用动词
- 其它（序数词，状语等）

## Question Classification

### 步骤与流程

- 规则 Rules
    - 疑问词判断 e.g. “谁”，“哪里”
    - 中心词判断 e.g. “国家”，“城市”
    - 中心词POS判断 e.g. "nr", "ns"
- 学习 Learning
    - Training use 'rules result'
    - Use word2vec vectors of `中心词`,`疑问词` as features
    - Use classifiers to decide categories

### 相关具体

- 学习－工具: `Scikit-learn`

- 学习－分类
    - **类别**
        - Q_person-人名，
        - Q_time-时间（含年份），
        - Q_place-地点（含国家、省份）
        - Q_number-数字（含序数），
        - Q_organization-机构名，
        - Q_other-其它名词
- 学习－特征
    - 疑问词
    - 中心词
        - “是”出现，则为之前的名词（中心词），否则，为疑问词后的名词
