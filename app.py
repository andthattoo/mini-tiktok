import time
import streamlit as st
from firstbatch import FirstBatch, AlgorithmLabel, Pinecone, Config, UserAction, Signal
import pinecone

aurl = 'https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/default-avatar.png'
cdn_url = "https://cdn.firstbatch.xyz/source/{}.mp4"

FIRST_BATCH_API_KEY = st.secrets["api"]["firstbatch_api_key"]
PINECONE_API_KEY = st.secrets["api"]["pinecone_api_key"]
PINECONE_ENV = st.secrets["api"]["pinecone_env"]
CUSTOM_ALGO_ID = st.secrets["custom_algo_id"]


def init():
    if 'personalized' not in st.session_state:
        config = Config(batch_size=5, verbose=True, enable_history=True, embedding_size=384)
        personalized = FirstBatch(api_key=FIRST_BATCH_API_KEY, config=config)
        pinecone.init(api_key=PINECONE_API_KEY,
                      environment=PINECONE_ENV)

        index = pinecone.Index("tiktok")
        personalized.add_vdb("tiktok_db_pinecone", Pinecone(index))
        st.session_state.personalized = personalized

        st.session_state.session = st.session_state.personalized.session(AlgorithmLabel.CUSTOM,
                                                                         vdbid="tiktok_db_pinecone",
                                                                         custom_id=CUSTOM_ALGO_ID)

        st.session_state.batches = []
        st.session_state.ids = []
        st.session_state.likes = []
        st.session_state.current_idx = 0

        st.session_state.watch_time = []

        ids, batch = st.session_state.personalized.batch(st.session_state.session)
        st.session_state.batches += batch
        st.session_state.ids += ids

        st.session_state.stamp = time.time()


def display_video_with_size(width=640, height=360, avatar_url=""):
    b = st.session_state.batches[st.session_state.current_idx]
    _id = b.data["id"]
    text = b.data["text"]
    username = b.data["username"]
    play_count = b.data["play_count"]
    likes = b.data["likes"]
    url = cdn_url.format(_id)

    padding_horizontal = 20
    adjusted_width = width - 2 * padding_horizontal

    lines_of_caption = max(1, len(text) // 40)
    caption_height = lines_of_caption * 20

    video_embed_code = f"""
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
            <div style="display: flex; justify-content: center; align-items: center; flex-direction: column; font-family: 'Poppins', sans-serif; width: {width}px; margin-left: auto; margin-right: auto;">

                <!-- Avatar and Username with white background and left alignment -->
                <div style="display: flex; align-items: center; padding: 20px; background-color: white; width: {adjusted_width}px; justify-content: flex-start;">
                    <img src="{avatar_url}" alt="{username}'s avatar" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px;" />
                    <div style="font-weight: 600;">@{username}</div>
                </div>

                <!-- Video -->
                <video width="{width}" height="{height}" autoplay loop>
                    <source src="{url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>

                <!-- Video Caption -->
                <div style="text-align: center; background-color: white; padding: 10px 20px; border-top: 1px solid #e5e5e5; border-bottom: 1px solid #e5e5e5; width: {adjusted_width}px;">
                    {text}
                </div>

                <!-- Likes and Views with white background -->
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px; background-color: white; width: {adjusted_width}px;">
                    <div><span style="font-weight: bold;">{int(likes)}</span> Likes</div>
                    <div><span style="font-weight: bold;">{int(play_count)}</span> Views</div>
                </div>
            </div>
    """
    total_height = height + 150 + caption_height + 40
    st.components.v1.html(video_embed_code, height=total_height)


st.title("TikTok Mini")
st.header("", divider="rainbow")
placeholder = st.empty()


def display_video():
    with placeholder:
        display_video_with_size(width=405, height=720, avatar_url=aurl)


def main():

    with st.container():

        st.markdown("""
            <style>
                .stButton>button {
                    display: block;
                    width: 405px;
                    margin-left: auto;
                    margin-right: auto;
                    margin-top: -30px;  # Adjusts the top margin to reduce the space above the button
                }
            </style>
        """, unsafe_allow_html=True)

        if st.button("Next"):
            cid = st.session_state.ids[st.session_state.current_idx]
            t2 = time.time()
            time_passed = t2 - st.session_state.stamp

            if time_passed > 5:
                # If time spent post is more than 5 seconds, send signals
                if time_passed > 15:
                    ua = UserAction(Signal.HIGH_ATTN)
                    st.session_state.personalized.add_signal(st.session_state.session, ua, cid)
                elif time_passed > 12:
                    ua = UserAction(Signal.MID_ATTN)
                    st.session_state.personalized.add_signal(st.session_state.session, ua, cid)
                elif time_passed > 9:
                    ua = UserAction(Signal.LOW_ATTN)
                    st.session_state.personalized.add_signal(st.session_state.session, ua, cid)

            if st.session_state.current_idx >= len(st.session_state.batches) - 1:
                ids, batch = st.session_state.personalized.batch(st.session_state.session)
                st.session_state.batches += batch
                st.session_state.ids += ids

            st.session_state.current_idx += 1
            st.session_state.stamp = time.time()
            display_video()


if __name__ == '__main__':
    init()
    display_video()
    main()


