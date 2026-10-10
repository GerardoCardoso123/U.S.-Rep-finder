import requests
import streamlit as st

st.set_page_config(page_title="U.S. Representative Finder")
API_URL = "https://api.5calls.org/v1/representatives"

st.title("U.S. Representative Finder")
st.write("Find your U.S. House Representative and Senators.")

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
try:
    reps = data.get("representatives", [])
except Exception as e:
    st.error(f"An error occured: {e}")
    reps = []

if reps:
    for rep in reps:
        with st.container(border=True):
            photo = (
                rep.get("photoURL")
                or rep.get("photo_url")
                or rep.get("image")
            )

            col1, col2 = st.columns([1, 3])

            with col1:
                if photo:
                    st.image(photo, width=130)
                else:
                    st.caption("Photo unavailable")

            with col2:
                name = rep.get("name", "Unknown")
                party = rep.get("party", "Unknown")
                office = rep.get("area", "Unknown")

                st.subheader(name)
                st.write(f"**Party:** {party}")
                st.write(f"**Office:** {office}")

                if "house" in office.lower():
                    district = rep.get("district")

                    if district is None:
                        district = data.get("district")

                    if district is not None:
                        st.write(f"**Congressional District:** {district}")
                    else:
                        st.write("**Congressional District:** Not provided")

                elif "senate" in office.lower():
                    st.write("**District:** Statewide")

                if rep.get("url"):
                    st.link_button(
                        "Official Website",
                        rep["url"]
                    )
else:
    st.info("No representatives found.")

                        else:
                            st.info("No representatives found.")

            except requests.exceptions.RequestException:
                st.error("Could not connect to the lookup service.")
