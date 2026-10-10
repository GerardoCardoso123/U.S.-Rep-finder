import requests
import streamlit as st

st.set_page_config(
    page_title="Find My Reps",
    page_icon="🇺🇸",
    layout="centered"
)
st.markdown("""
<style>
/* Main page background */
.stApp {
    background-color: d7e3ff;
}

/* Main title and headings */
h1, h2, h3 {
    color: #102A56 !important;
}
/* Buttons */
.stButton > button {
    background-color: #bd1313;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1.2rem;
    font-weight: 600;
}
/* Button hover effect */
.stButton > button:hover {
    background-color: #102A56;
    color: white;
    border: 1px solid white;
}

/* Input fields */
.stTextInput input {
    border-radius: 8px;
}

/* Cards and content containers */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: d7e3ff;
    border-radius: 12px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #102A56;
}
</style>
""", unsafe_allow_html=True)




st.set_page_config(page_title="U.S. Representative Finder")

API_URL = "https://api.5calls.org/v1/representatives"

st.title("U.S. Representative Finder")

address = st.text_input(
    "Enter your address",
    placeholder="Street address, city, state, ZIP code"
)

if st.button("Find My Representatives"):
    if not address.strip():
        st.warning("Please enter your address.")
    else:
        api_token = "f75ea9aec2ff88f32b433843"

        if not api_token:
            st.error("The API token has not been configured.")
        else:
            try:
                response = requests.get(
                    API_URL,
                    headers={"X-5Calls-Token": api_token},
                    params={
                        "location": address.strip(),
                        "areas": "US House,US Senate"
                    },
                    timeout=15
                )

                if response.status_code != 200:
                    st.error("The representative lookup failed.")
                else:
                    data = response.json()

                    if data.get("error"):
                        st.error(str(data["error"]))
                    else:
                        st.subheader("Your Representatives")
                        st.write("**Location:**", data.get("location", "Unknown"))
                        st.write("**State:**", data.get("state", "Unknown"))
                        st.write(
                            "**Congressional District:**",
                            data.get("district", "Unknown")
                        )

                        reps = data.get("representatives", [])

                        if reps:
                            for rep in reps:
                                with st.container(border=True):
                                    st.subheader(rep.get("name", "Unknown"))
                                    st.write("**Party:**", rep.get("party", "Unknown"))
                                    st.write("**Office:**", rep.get("area", "Unknown"))

                                    if rep.get("district") is not None:
                                        st.write("**District:**", rep["district"])

                                    if rep.get("url"):
                                        st.link_button("Official Website", rep["url"])
                        else:
                            st.info("No representatives found.")

            except requests.exceptions.RequestException:
                st.error("Could not connect to the lookup service.")
