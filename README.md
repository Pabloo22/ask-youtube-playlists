# Ask Your Favorite YouTube Playlist
This web application allows users to ask questions about any YouTube playlist.
## Overview
![Project Overview](https://docs.google.com/drawings/d/e/2PACX-1vSC9uKSU6Ue7YpMr7d5qTMMZO0tFSyvy3kZeB9UVMSulpAOMkglTHZnSZXoUvgywaksNtZ_-AFx87bm/pub?w=960&h=720)



After following the steps described in the [Installation](#rocket-installation) section, we can run the web
application by executing the following command:
```shell
make run_app
```

### Download the YouTube playlist
Before asking any question, we need to download the transcripts and timestamps from the YouTube playlist.

To complete this task, we use the YouTube API to download the transcripts and timestamps from the episodes of the
playlist introduced by the user. The transcripts and timestamps will be stored inside the `$DATA_PATH/playlist_name/raw` 
folder.

The `$DATA_PATH` is defined in the `.env` file. The playlist name is the name of the playlist introduced by the user.

Inside this file, you will find files `Video_i.json` that follow the structure:

```python
{   
    "title": "Title of the video",
    "video_id": "ID of the video",
    "transcript": [
    {
        "text": "Hey there",
        "start": 7.58,
        "duration": 6.13,
    },
    {
        "text": "how are you",
        "start": 14.08,
        "duration": 7.58
    },
    # ...
}
```
Then, we will create chunks from that data, since the raw data is quite separated, so we merge some chunks. We can define the maximum length of each chunk and the overlap between chunks depending on our needs. We also add the thumbnail and the link with the timestamp

```python
[
    {
        "text": "Hey there how are you...",
        "start": 7.58,
        "duration": 34.08,
        "url": "https://www.youtube.com/watch?v=...",
        "title": "Title of the video",
        "thumbnail": "https://i.ytimg.com/vi/..."
    },
    # ...
]
```

First, 
The idea consists of creating an application that answers questions about any YouTube playlist.

The task will be divided in two steps:

1. **Information Retrieval**:
This step involves identifying relevant episodes, sections, or segments from the playlist or playlists that might contain the 
answer to the user's question. Techniques we plan to use include:

- **Pre-trained sentence transformers**: Models like DistilBERT, MiniLM or Ada can be used to create sentence
embeddings and measure the semantic similarity between the user's question and the podcast data.

Here we have a table summarizing the available sentence transformers:

| Model Name                           | Model Type            | Max Sequence Length |
|--------------------------------------|-----------------------|---------------------|
| msmarco-MiniLM-L-6-v3                 | sentence-transformers | 512                 |
| msmarco-distilbert-base-v4            | sentence-transformers | 512                 |
| msmarco-distilbert-base-tas-b         | sentence-transformers | 512                 |
| text-embedding-ada-002                | openai                | 8191                |

2. **Natural Language Understanding**:
Once relevant portions of the dataset have been identified, a fine-tuned NLP model processes the user's question and 
the relevant information to generate an appropriate answer. We will explore two approaches:

- **Extractive question-answering**: In this approach, the model is trained to identify and extract the exact answer 
from the relevant text. Models like BERT or RoBERTa can be fine-tuned on a question-answering dataset for this 
purpose.

- **Generative question-answering**: This technique involves generating a human-like answer by paraphrasing or 
summarizing the relevant information. Models like GPT can be employed for this task. We use the Open AI API to use
powerful models such as GPT-3.5 OR GPT-4, although other locally hosted models such as GPT-2 or LLaMa could be used

Our application will offer users the option to choose between the two question-answering modes, so we will implement 
both approaches. The web application will prompt users to input their questions and display results within the 
interface.

## :rocket: Installation 
1. Clone the repository.
2. Duplicate the `.env.template` file and rename it to `.env`.
3. Fill in the environment variables in the `.env` file.
4. Install [Poetry](https://python-poetry.org/) and Python if you don't have them already.
5. Run `poetry install` to install the dependencies in a virtual environment.
6. Run `poetry shell` to activate the virtual environment.

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
