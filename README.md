
# Unsupervised-Thai-Document-Clustering-with-Sanook-news
TL;DR: This work creates an unsupervised model to clustering Thai news into 10 categories. Using TD-IDF, SimCSE-WangchanBERTa with weighted by number of named entities as a vector representation, and using k-means as an clustering model.

## Problem statement
Create unsupervised model to clustering sanook news 10 categories. 

## Dataset
* The data was scraped from [sanook.com](https://www.sanook.com/) is ordered by most popular views for each category. 
* there are 10 categories: [crime](https://www.sanook.com/news/tag/อาชญากรรม/),  [politics](https://www.sanook.com/news/tag/การเมือง/), [money](https://www.sanook.com/money/archive/), [technology](https://www.sanook.com/hitech/archive/), [sport](https://www.sanook.com/sport/archive/), [health](https://www.sanook.com/health/archive/), [horoscope](https://www.sanook.com/horoscope/archive/), [car](https://www.sanook.com/auto/archive/), [game](https://www.sanook.com/game/archive/), [entertain](https://www.sanook.com/news/archive/entertain/') 
* I scraped using Selenium and BeautifulSoup.
* he source code can be found in [sanook_web_scraping.ipynb](https://github.com/sorayutmild/Unsupervised-Thai-Document-Clustering-with-Sanook-news/blob/main/sanook_web_scraping.ipynb "sanook_web_scraping.ipynb") or you can download it from [Google drive](https://drive.google.com/drive/folders/14iCuSBW-Ia31dhJgOVGdd4XSSdqntmbh?usp=sharing)


## Method
### 1. Vector representation
#### 1.1 Vector representation using Bag-of-Words (TF-IDF) 
I create vector representation using Bag-of-Words (TF-IDF) and use it as a baseline.

<p align="center">
  <img src="https://github.com/sorayutmild/Unsupervised-Thai-Document-Clustering-with-Sanook-news/blob/main/img/tf_idf.jpg?raw=true" alt="Bag-of-Words"/>
</p>

* Text cleaning: remove link, symbols, numbers, special characters
* Word tokenization: newmm (dictionary-based, Maximum Matching + Thai Character Cluster)
* TF-IDF vectorization

#### 1.2 Vector representation using Transformer model
<p align="center">
  <img src="https://github.com/sorayutmild/Unsupervised-Thai-Document-Clustering-with-Sanook-news/blob/main/img/transformer.jpg?raw=true" alt="Transformer model"/>
</p>

* Text cleaning: remove link, symbols, numbers, special characters
* Sentence tokenization: CRF
* Sentence embedding: The best model is [WangchanBERTa with SimCSE](https://huggingface.co/mrp/simcse-model-wangchanberta).
* Weighted with number of Named-Entities
After, Sentences are embedded to vector by Transformer model. The embedded vectors are weighted by number of named entities of particular types in sentence. then make Document vector representation using these formulas.

$$
  v_{d} = \frac {\sum_{s \in d}w_{s} \times v_{s}} {\sum w_{s}}
$$ 

$$ w_{s} = n_{s} + 1$$

where  n<sub>s</sub> denotes the number of named entities of particular types in sentence.
This weighting scheme is adopted from https://ieeexplore.ieee.org/document/9085059

### 2. Clustering model
After, we get vector representation. we use the vector as a cluster features. 
I used simple k-mean clustering following the code below.
```python
from sklearn.cluster import KMeans
k = 10
km = KMeans(n_clusters=k, max_iter=100, n_init=55,)
```

## How to run code
* **For web scraping** (you can skip this. we download it for you)
	* Install the library by running this command ```pip install -r requirements.txt```
    * Download chromedriver.exe and put in directory.
	* then run this notebook [sanook_web_scraping.ipynb](https://github.com/sorayutmild/Unsupervised-Thai-Document-Clustering-with-Sanook-news/blob/main/sanook_web_scraping.ipynb "sanook_web_scraping.ipynb") with that environment.

* **Document clustering**
	*  Run this [Document_clustering.ipynb](https://github.com/sorayutmild/Unsupervised-Thai-Document-Clustering-with-Sanook-news/blob/main/Document_clustering.ipynb "Document_clustering.ipynb") notebook on Google Colab. 
it contains 
		* Text preprocessing
		* Text representation
			* Bag-of-Words
			* Transformer Embedding
		* Clustering model
		* Evaluation
		* Error analysis

## Results
Chosen the class of cluster by select the most frequency in each cluster. \
compare the predictions with Labels by accuracy score as a evaluation metric. 

| **Vector representation techniques** | Acc |
|------------------------|-------|
| TF-IDF | 0.8216 |
| SimCSE WangchanBERTa | 0.8330 |
| SimCSE WangchanBERTa Weighted with number of Named-Entities | **0.8445** |
| SimCSE WangchanBERTa finetuned Weighted with number of Named-Entities | 0.7368 |

## Discussion
* I have tried a lot of Transformer model (BERT, RoBERTa, and WangchanBERTa) by adding pooling layer to get embedding vector shape (number_of_samples, 768). But they are not perform well in this task.
* SimCSE improves the model's performance.
* SimCSE model with Weighted with number of Named-Entities is the best in my experiments.

## Future work
* Try other Clustering models (e.g., Hierarchical clustering, DBSCAN)
* Try Dimension reduction methods (e.g., PCA)
* Try other weighted schemes
* Try Vector representation with Doc2vec method
* Try soft clustering (topic modeling) (e.g., LDA)

## Acknowledgements
* pre-trained model from [huggingface](https://huggingface.co/mrp/simcse-model-wangchanberta)
*  weighting scheme is adopted from  [https://ieeexplore.ieee.org/document/9085059](https://ieeexplore.ieee.org/document/9085059)
* [WangchanBERTa: Pretraining transformer-based Thai Language Models](https://arxiv.org/abs/2101.09635)
* [SimCSE: Simple Contrastive Learning of Sentence Embeddings](https://arxiv.org/abs/2104.08821)