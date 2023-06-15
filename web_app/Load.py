import streamlit as st

from ask_youtube_playlists.data_processing import (download_playlist,
                                                   is_youtube_playlist,
                                                   get_available_directories
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

if "loaded_playlist_names" not in st.session_state:
    st.session_state["loaded_playlist_names"] = []


def main():
    loaded_playlist_names = st.session_state.get("loaded_playlist_names", [])
    available_playlists = get_available_directories(get_data_directory())
    available_playlists = [playlist for playlist in available_playlists
                           if playlist not in loaded_playlist_names]
    # ---------------------------------------------------------------------
    with st.sidebar:
        st.markdown("""
                <style>
                .sidebar .sidebar-content {
                    min-width: 180px;
                }
                </style>
            """, unsafe_allow_html=True)
        st.header("Set parameters")

        # Update the sidebar with the new playlist name
        st.subheader("Loaded Playlists")
        for name in loaded_playlist_names:
            st.write(name)
    # -------------------------------------------------------------------------

    playlist_name = st.text_input("Enter your playlist's folder name",
                                  available_playlists)
    data_directory = get_data_directory()
    playlist_path = data_directory / playlist_name

    if playlist_name is None:
        pass
    elif playlist_name not in loaded_playlist_names:
        if playlist_path.exists():
            st.success("Playlist cached from previous session!")
            st.session_state["loaded_playlist_names"].append(playlist_name)
            st.experimental_rerun()
        else:
            youtube_link = st.text_input("Enter YouTube playlist link")
            if is_youtube_playlist(youtube_link):
                st.success("Valid YouTube playlist link!")
                playlist_path.mkdir()
                download_playlist(youtube_link,
                                  playlist_path,
                                  use_st_progress_bar=True,
                                  )
                st.session_state["loaded_playlist_names"].append(playlist_name)
                st.experimental_rerun()
            else:
                st.error("Invalid YouTube playlist link!")
    else:
        st.caption("The playlist has been already loaded! "
                   "Please choose another name.")


if __name__ == "__main__":
    main()
