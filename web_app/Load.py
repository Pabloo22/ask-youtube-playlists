import streamlit as st
import re  # regex library
import time
import pathlib

from ask_youtube_playlists.data_processing import (download_playlist,
                                                   EMBEDDING_MODELS_NAMES
                                                   )

from utils import get_data_directory

# youtube playlist link to test:
# https://www.youtube.com/playlist?list=PLPNW_gerXa4Pc8S2qoUQc5e8Ir97RLuVW

st.set_page_config(
    page_title="Ask Youtube Playlist",
    page_icon="🔎",
)

st.title("Ask YouTube Playlist")
st.caption("Welcome to Ask YouTube Playlist! Get started by entering a valid "
           "YouTube playlist link below and selecting your preferred "
           "answering mode and model. Ask away and explore the content of "
           "your favorite YouTube playlists in a whole new way!")

playlist_dict = st.session_state.get("playlist_list", {})

# Sidebar ---------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
            <style>
            .sidebar .sidebar-content {
                min-width: 180px;
            }
            </style>
        """, unsafe_allow_html=True)
    st.header("Set parameters")

    # Embedding model selection
    embedding_model_name = st.selectbox("Embedding Model", EMBEDDING_MODELS_NAMES)

    # Update the sidebar with the new playlist name
    st.subheader("Available Playlists")

    # Allows to choose which playlists one wants to use
    for playlist, link in playlist_dict.items():
        checkbox_value = st.checkbox(f"[{playlist}]({link})", key=playlist)

    # -------------------------------------------------------------------------


# checks if a string is a youtube playlist link
def is_youtube_playlist(link):
    pattern = r'(https?://)?(www\.)?youtube\.com/playlist\?list=([' \
              r'a-zA-Z0-9_-]+)'
    match = re.match(pattern, link)
    return match is not None


def clear_text():
    st.session_state["text"] = ""


# Download
def main():
    # TODO check if there is already a playlist on the data folder

    # input for YouTube playlist link
    playlist_name = st.text_input("Enter your playlist's name")

    if playlist_name != "":
        youtube_link = st.text_input("Enter YouTube playlist link")

        # the user can only insert a question if the link is valid
        if is_youtube_playlist(youtube_link):
            st.success("Valid YouTube playlist link!")

            parent_path = pathlib.Path(__file__).parent
            while parent_path.name != "ask-youtube-playlists":
                parent_path = parent_path.parent

            playlist_path = parent_path / 'data' / playlist_name

            if not playlist_path.exists():
                playlist_path.mkdir()
            else:
                st.caption("The playlist already exists. "
                            "Please choose another name.")

            download_playlist(youtube_link, playlist_path,
                              use_st_progress_bar="true")

            # TODO call the function that downloads the playlist
            # TODO get the names of the playlist
            # TODO Add the playlist details to the list (change youtube_link
            #  to the name of the playlist)
            playlist_dict[playlist_name] = youtube_link
            # Update the session state with the new playlist list
            st.session_state["playlist_list"] = playlist_dict

        else:
            st.error("Invalid YouTube playlist link!")


if __name__ == "__main__":
    main()
