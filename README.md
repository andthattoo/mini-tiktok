# Mini TikTok
## A fully personalized TikTok feed with Streamlit, Pinecone, and FirstBatch

This repository showcases an application that provides a no-login, personalized TikTok feed using [Streamlit](https://streamlit.io/) for the front end, [Pinecone](https://www.pinecone.io/) for vector search, and [FirstBatch](https://www.firstbatch.xyz/) for content recommendation.
Personalized feed is shaped by how much a viewer spent time on a video.

Main idea is here to demonstrate how AI based navigation can be used instead of search based navigation. 

![App](https://cdn.firstbatch.xyz/tiktok_mini.png)

## Dataset
The dataset used for this project is [TikTok Trending Video Dataset](https://www.kaggle.com/datasets/erikvdven/tiktok-trending-december-2020) from Kaggle.
Dataset consists of 1000 videos. 

## Tutorial
You can find a detailed tutorial on how to build this app [here](https://andthattoo.substack.com/p/personalized-mini-tiktok).

## Features

- **Personalized Recommendations**: Integrating FirstBatch with Pinecone, the app provides unique, tailored content recommendations for each user.
- **Custom Algorithms**: App uses a custom algorithm developed with [user embeddings dashboard](https://userembeddings.firstbatch.xyz), which can be easily swapped out for other custom algorithms.
- **Scalability**: With Pinecone's powerful vector search, the application can easily scale to handle large datasets.
- **Easy Development**: Streamlit provides a simple, intuitive interface for developing the front end.
## Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:andthattoo/mini-tiktok.git
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API keys in the `st.secrets` configuration. Ensure you have API keys for both FirstBatch and Pinecone. A secrets.toml example:
    ```toml
   
    "custom_algo_id" = "[algo_id]"
   
    [api]
    "pinecone_api_key"="[pinecone_key]"
    "pinecone_env"="[pinecone_env]"
    "firstbatch_api_key"="[firstbatch_key]"
    ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Build Your Personalization Algorithm
FirstBatch allows you to create your own personalization algorithms.
You can go through [How to Build an Algorithm?](https://firstbatch.gitbook.io/user-embeddings/user-embeddings-personal-navigation-for-llms/how-to-build-an-algorithm) and this [walkthrough](https://app.storylane.io/share/ui1h5umftbaz) to build your own algorithm.

Once you've created your algorithm, user embeddings dashboard will provide you with an `algo_id` that you can use in the `st.secrets` configuration.

## Contribution

Feel free to fork this repository and make enhancements. Pull requests are warmly welcomed!