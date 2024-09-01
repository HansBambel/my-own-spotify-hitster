import streamlit as st

for k, v in st.session_state.items():
    st.session_state[k] = v

create_page = st.Page("pages/config_page.py", title="Config")
play_page = st.Page("pages/play_page.py", title="Play")

pg = st.navigation([create_page, play_page])

st.title("My Own Spotify Hitster")


pg.run()


# if __name__ == '__main__':
# taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'
# sp = get_spotify_read_auth()
# results = sp.artist_albums(taylor_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = sp.next(results)
#     albums.extend(results['items'])
#
# for album in albums:
#     print(album['name'])
