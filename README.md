# Huberman Lab Podcast Q&A System
Work in progress

## :rocket: Installation 

1. Clone the repository.
2. Duplicate the `.env.template` file and rename it to `.env`.
3. Fill in the environment variables in the `.env` file.
4. Install [Poetry](https://python-poetry.org/) if you don't have it already.
5. Run `poetry install` to install the dependencies in a virtual environment.
6. Run `poetry shell` to activate the virtual environment.
7. Download the podcast transcripts and timestamps from 
[Kaggle](https://www.kaggle.com/datasets/piyusharma/andrew-huberman-podcast-transcripts-95-episodes) and place them 
in the `data/raw` folder.

## Objective
The idea consists of creating an application that answers questions about 
the [Huberman Lab podcast](https://hubermanlab.com/) which discusses 
science and science-based tools for everyday life. We will make 
use of a dataset with the transcripts of the first 95 episodes that is available on 
[Kaggle](https://www.kaggle.com/datasets/piyusharma/andrew-huberman-podcast-transcripts-95-episodes). 
The task will be divided in two steps:

1. **Information Retrieval**:
This step involves identifying relevant episodes, sections, or segments from the podcast dataset that might contain the 
answer to the user's question. Techniques we plan to use include:

- **Keyword matching**: Extract keywords from the user's question and search for those keywords in the dataset.
- **Pre-trained sentence transformers**: Models like BERT or Universal Sentence Encoder can be used to create sentence
embeddings and measure the semantic similarity between the user's question and the podcast data.

2. **Natural Language Understanding**:
Once relevant portions of the dataset have been identified, a fine-tuned NLP model processes the user's question and 
the relevant information to generate an appropriate answer. We will explore two approaches:

- **Extractive question-answering**: In this approach, the model is trained to identify and extract the exact answer 
from the relevant text. Models like BERT or RoBERTa can be fine-tuned on a question-answering dataset for this 
purpose.

- **Abstractive question-answering**: This technique involves generating a human-like answer by paraphrasing or 
summarizing the relevant information. Models like GPT can be employed for this task.

Our application will offer users the option to choose between the two question-answering modes, so we will implement 
both approaches. The web application will prompt users to input their questions and display results within the 
interface.

## :file_folder: Project Structure 
The source code is organized in two main components. The first component is the... 

### Question-Answering System Package
The Question-Answering system package contains the code for the different components of the system. The code contained in this package is not dependent on the specific web application framework used to deploy 
the system or any specific data sources. 

The sub-package `base` contains the base classes for the question answering system. These classes are used to define the interfaces for the
different components of the system. The main classes are:

- **Embedder**: Interface for the embedding component of the system. This component is responsible for generating
embeddings for the user's question and the relevant information from the podcast dataset.
- **InformationRetriever**: Interface for the information retrieval component.
- **ExtractiveQuestionAnswerer**: Interface for the extractive question answering component.
- **AbstractiveQuestionAnswerer**: Interface for the abstractive question answering component.

This allows us to define different implementations for each component of the system and easily switch between them.
These implementations are defined in the sub-packages `information_retrieval`, and `question_answering`,
which will be used by...

### The Web Application
This package contains the code for the web application. The code inside this package requires the data sources to be
available and the .env file to be correctly configured. It also 
contains the sub-package `data` which contains the code for loading and
preprocessing the transcripts and timestamps from the podcast dataset downloaded from 
[Kaggle](https://www.kaggle.com/datasets/piyusharma/andrew-huberman-podcast-transcripts-95-episodes).

## :books: Resources
Resources and tutorials that we have found useful for this project.

### :fire: PyTorch
- **How to learn PyTorch?**: [YouTube, How to learn PyTorch? (3 easy steps) | 2021](https://www.youtube.com/watch?v=2n_uoGOPoVk)
- **Official tutorial**: https://pytorch.org/tutorials/
- **Blog**: [Understanding PyTorch with an example: a step-by-step tutorial](https://towardsdatascience.com/understanding-pytorch-with-an-example-a-step-by-step-tutorial-81fc5f8c4e8e)

### :gear: Set Up
- **Poetry**: [YouTube, How to Create and Use Virtual Environments in Python With Poetry](https://youtu.be/0f3moPe_bhk)
- **Automated testing**: [YouTube, Automated Testing in Python with pytest, tox, and GitHub Actions](https://youtu.be/DhUpxWjOhME)

### :mag: Information Retrieval
- **Semantic Search with S-BERT**: [Medium article, Semantic Search with S-BERT is all you need](https://medium.com/mlearning-ai/semantic-search-with-s-bert-is-all-you-need-951bc710e160)