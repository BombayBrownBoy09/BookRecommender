# Book-reccomender

**Project by Abhilash Sarnad, Christine Park and Bhargav Shetgaonkar for Duke AIPI 540 Module 3**
<p align="center"><img align="center" width="800px" src="https://github.com/SarnadAbhilash/RecIt.git/blob/Images/method.png"></p>

<a name="proj-stat"></a>
## 1. Problem statement
The objective of this project is to train a deep learning model to recommend books to users using User-User based collaborative filtering

## 2. Project Structure
The project data and codes are arranged in the following manner:

```
├── README.md               <- description of the project and how to set up and run it
├── requirements.txt        <- requirements file to document dependencies
├── Notebooks               <- contains the two colab notebooks used to build the recommendations
    ├── BooksRec.ipynb      <- notbook for generating recommendation by finding similar users
    ├── Collaborative_filtering.ipynb   <- contains the code for generating recommendation using collaborative filtering
├── scripts
    ├── search.py           <- contains the code for searching book titles
    ├── liked_books.py      <- contains the code for compiling books a user likes
    ├── recommender.py      <- contains the code for recommending books that the user might like 
├── main.py                 <- contains the main script modeled using User-User collaborative filtering based approach
├── .gitignore              <- git ignore file
```

_Data_: <br>
the `data` folder is not a part of this git project as it was heavy. The same can be downloaded from below link:
1) Download data [here](https://drive.google.com/uc?id=1LXpK1UfqtP89H1tYy0pBGHjYk8IhigUK) 

```sh
https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home
```

<a name="exp"></a>

2) _Code & Results_: <br>
View code and sample results [here](/Users/abhilashsarnad/myWork/Portfolio/Recit/RecIt/Notebooks/BooksRec.ipynb) 


## 3. Search & Recommend Functionality 
- Search Books related to sherlock holmes:
<p align="center"><img align="center" width="800px" src="https://github.com/SarnadAbhilash/RecIt.git/blob/Images/search.png"></p>

- Recommend 10 books based on liked books:

**INPUT - Steve jobs, Atomic habits, elon musk, Harry potter, AI and future**

<p align="center"><img align="center" width="800px" src="https://github.com/SarnadAbhilash/RecIt.git/blob/Images/Recs.png"></p>

## 4. How to Run the Code
Use the command line to run the main.py file in the scripts folder to train the model with specified parameters.

```
python main.py

```
