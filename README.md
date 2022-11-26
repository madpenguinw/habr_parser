# Habr parser
- Terminal app for parsing habr.com
- Saving information about artcles and their authors
- Saving article text
- Cleaning that text and creating a "tag cloud" from it
---
### Installation
Fistly run in terminal:
```
git clone https://github.com/madpenguinw/habr_parser.git
```
Secondly download <a href=https://www.anaconda.com/products/distribution>Anaconda</a> and run in its prompt:
```
conda create --name venv --file .\requirements.txt
conda install --name venv -c https://conda.anaconda.org/conda-forge wordcloud
conda install --name venv -c conda-forge pymorphy2
conda install --name venv -c conda-forge natasha
```
When your venv is activated:
```
pip install natasha
```
Finally run main.py file:
```
python 'your_path_to_main.py'
```
---
### Using
- choose the task you would like to do (1-5)
#### First task
- input keywords that you are interested to look up in habr.com
- you should choose a page that will be parsed (from 1 to 50) or input 0 if you want to parse all pages
- check the results in *data.json* that will appear in your directory 
#### Second task
- input link to arcticle on Habr.com or its id
- this article will be downloaded to text.txt file in root directory
#### Third task
- there will be created a "tag cloud" as a tag_cloud.png from text in text.txt
#### Fourth task
- generates a list of people mentioned in the text
#### Fifth task
- closes the program
---
### About
```
developed_by = {'author': 'Mikhail Sokolov',
                'university': 'ITMO',
                'telegram': 't.me/lmikhailsokolovl',
                'is_it_funny': True}
```
