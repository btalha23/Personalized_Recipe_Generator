## Setup for Running the Application Locally

Make sure `git` is installed on your local machine. If not, then 

1. go to [Git Downloads](https://git-scm.com/downloads),
2. download the installer for your operating system, and
3. follow the instructions to complete the installation.


Since the LLM RAG is basically a text-to-SQL chain, it is required that MySQL database server is running on your local machine. For this reason,

1. got to [MySQL Community Installer](https://dev.mysql.com/downloads/installer/)
2. download the installer for your operating system, and
3. follow the instructions to complete the installation.

**NOTE: use *root* for both username and password of the database.**

Clone the repository in your local machine.

```bash
git clone https://github.com/btalha23/Personalized_Recipe_Generator.git && \
cd Personalized_Recipe_Generator
```

Install all the tools and dependencies

```bash
pip install -r requirements.txt
```
To prepare the database to be used as the knowledge base in the LLM RAG application, go to `exploratory_data_analysis` folder. If you are currently in `Personalized_Recipe_Generator` folder then executing the following command will move you to the correct directory.

```bash
cd exploratory_data_analysis
```
Then execute the Jupyter notebook entitled `prg_prepare_database.ipynb` to load the dataset CSV file into the database.



To run the Personalized Recipe Generator application to have to come out of `exploratory_data_analysis` folder and go to `llm_rag_application` folder

```bash
cd .. && \
cd llm_rag_application && \
streamlit run personalized_recipe_generator.py
```

**IMPORTANT: In order for the Streamlit app and LangSmith monitoring to work, you need to create a `.env` file in the root directory. Root directory is the one where you can find READMED.md and the requirements.txt files.**

There are OPENAI and LanhChain API keys in the `.env`file. It should look something like

```

OPENAI\_API\_KEY=<YOUR\_OPENAI\_API\_KEY>

LANGCHAIN\_API\_KEY=<YOUR\_LANGCHAIN\_API\_KEY>

```

*NOTE: Please refer to [Setup](setup/monitoring.md) for pointers about how to get the required API key for LangChain.*