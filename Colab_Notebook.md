<a href="https://colab.research.google.com/github/akbargherbal/JS_CODE_PATTERN_ANALYSIS/blob/main/Colab_Notebook.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


```python
#
```


```python
import pandas as pd
import regex as re
import os
```


```python
df = pd.read_pickle('./DF_REPO_LINKS.pkl')
```


```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 170 entries, 0 to 169
    Data columns (total 1 columns):
     #   Column  Non-Null Count  Dtype 
    ---  ------  --------------  ----- 
     0   REPO    170 non-null    object
    dtypes: object(1)
    memory usage: 1.5+ KB
    


```python
df.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>REPO</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>170</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>170</td>
    </tr>
    <tr>
      <th>top</th>
      <td>https://github.com/fullcalendar/fullcalendar.git</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
!jupyter nbconvert --to markdown "./Colab_Notebook.ipynb"
```

    [NbConvertApp] Converting notebook ./Colab_Notebook.ipynb to markdown
    [NbConvertApp] Writing 1431 bytes to Colab_Notebook.md
    


```python

```
