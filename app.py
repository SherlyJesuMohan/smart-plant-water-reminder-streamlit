
import streamlit as st
from datetime import datetime, date, time

st.set_page_config(
    page_title="Smart Plant Water Reminder",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Smart Plant Water Reminder")
st.caption("Keep your plants healthy, one watering at a time!")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    ["Home", "My Plants", "Add Plant", "Watering Schedule"]
)

if "plants" not in st.session_state:
    st.session_state.plants = []

if page == "Home":
    st.subheader("Welcome to your Plant Care Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Plants", len(st.session_state.plants))
    col2.metric(
        "Watered Today",
        sum(
            1 for p in st.session_state.plants
            if p["last_watered"] == date.today()
        )
    )
    col3.metric(
        "Need Watering",
        sum(
            1 for p in st.session_state.plants
            if (date.today() - p["last_watered"]).days
            >= p["interval"]
        )
    )

    st.info("Add your plants and their watering schedules to get started.")

elif page == "Add Plant":
    st.subheader("Add a New Plant")

    with st.form("plant_form"):
        name = st.text_input("Plant name")
        plant_type = st.selectbox(
            "Plant type",
            ["Indoor", "Outdoor", "Flowering", "Succulent", "Herb", "Other"]
        )
        interval = st.number_input(
            "Water every (days)",
            min_value=1,
            max_value=60,
            value=3
        )
        last_watered = st.date_input(
            "Last watered",
            value=date.today()
        )

        submitted = st.form_submit_button("Add Plant")

        if submitted:
            if not name.strip():
                st.warning("Please enter a plant name.")
            elif any(
                p["name"].lower() == name.strip().lower()
                for p in st.session_state.plants
            ):
                st.warning("A plant with this name already exists.")
            else:
                st.session_state.plants.append({
                    "name": name.strip(),
                    "type": plant_type,
                    "interval": int(interval),
                    "last_watered": last_watered
                })
                st.success(f"{name.strip()} added successfully!")

elif page == "My Plants":
    st.subheader("My Plants")

    if not st.session_state.plants:
        st.info("No plants added yet. Open Add Plant to get started.")
    else:
        for i, plant in enumerate(st.session_state.plants):
            due = (
                date.today() - plant["last_watered"]
            ).days >= plant["interval"]

            with st.container(border=True):
                st.write(f"### 🪴 {plant['name']}")
                st.write(f"Type: {plant['type']}")
                st.write(f"Watering interval: Every {plant['interval']} days")
                st.write(f"Last watered: {plant['last_watered']}")

                if due:
                    st.warning("💧 Watering may be due today!")
                else:
                    st.success("Plant is not yet due for watering.")

                col1, col2 = st.columns(2)

                if col1.button("Mark Watered", key=f"water_{i}"):
                    plant["last_watered"] = date.today()
                    st.rerun()

                if col2.button("Delete Plant", key=f"delete_{i}"):
                    st.session_state.plants.pop(i)
                    st.rerun()

elif page == "Watering Schedule":
    st.subheader("Watering Schedule")

    if not st.session_state.plants:
        st.info("Add plants to view their watering schedule.")
    else:
        for plant in st.session_state.plants:
            days = (date.today() - plant["last_watered"]).days
            remaining = plant["interval"] - days

            if remaining <= 0:
                st.write(f"💧 **{plant['name']}** — Watering may be due now.")
            else:
                st.write(
                    f"🌿 **{plant['name']}** — Water in {remaining} day(s)."
                )

st.divider()
st.caption("Smart Plant Water Reminder | Streamlit Edition")
