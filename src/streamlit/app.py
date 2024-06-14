import requests
from matplotlib import pyplot as plt

import streamlit as st

COMPONENT_HEIGHT = 600

st.title("Predict health of tree")

st.markdown("You can get probabilities of health for tree by some features")

# @st.cache_data
# def get_model(path):
#     return load_model(path)


@st.cache_resource(max_entries=10, ttl=3600)
def predict_health(
    tree_dbh,
    curb_loc,
    steward,
    guards,
    sidewalk,
    problems,
    root_stone,
    root_grate,
    root_other,
    trunk_wire,
    trnk_light,
    trnk_other,
    brch_light,
    brch_shoe,
    brch_other,
    spc_common,
    zip_city,
    borough,
    user_type,
):
    data = {
        "tree_dbh": tree_dbh,
        "curb_loc": curb_loc,
        "steward": steward,
        "guards": guards,
        "sidewalk": sidewalk,
        "problems": problems,
        "root_stone": root_stone,
        "root_grate": root_grate,
        "root_other": root_other,
        "trunk_wire": trunk_wire,
        "trnk_light": trnk_light,
        "trnk_other": trnk_other,
        "brch_light": brch_light,
        "brch_shoe": brch_shoe,
        "brch_other": brch_other,
        "spc_common": spc_common,
        "zip_city": zip_city,
        "borough": borough,
        "user_type": user_type,
    }
    url = "http://fastapi:8000/api/predict/"
    response = requests.post(url, json=data)
    return response.json()


with st.form("form"):
    tree_dbh = st.number_input(
        "Diameter at breast height of tree", min_value=0, value=22
    )
    curb_loc = st.number_input(
        "Whether tree is along (0) or offset (1) from the curb",
        min_value=0,
        max_value=1,
        value=1,
    )
    steward = st.number_input(
        "Number of signs of stewardship observed", min_value=0, max_value=3, value=0
    )
    guards = st.number_input(
        "Presence and type of tree guard", min_value=0, max_value=3, value=0
    )
    sidewalk = st.number_input(
        "Sidewalk damage immediately adjacent to tree (damage 1, else 0)",
        min_value=0,
        max_value=1,
        value=1,
    )
    problems = st.number_input("Length of list with problems", min_value=0, value=1)
    root_stone_check = st.checkbox(
        "Root problems caused by paving stones in the tree bed", value=False
    )
    root_stone = 1 if root_stone_check else 0
    root_grate_check = st.checkbox("Root problems caused by metal grates", value=False)
    root_grate = 1 if root_grate_check else 0
    root_other_check = st.checkbox("Presence of other root problems", value=False)
    root_other = 1 if root_other_check else 0
    trunk_wire_check = st.checkbox(
        "Trunk problems caused by rope or wires", value=False
    )
    trunk_wire = 1 if trunk_wire_check else 0
    trnk_light_check = st.checkbox("Trunk problems caused by lights", value=False)
    trnk_light = 1 if trnk_light_check else 0
    trnk_other_check = st.checkbox("Presence of other trunk problems", value=False)
    trnk_other = 1 if trnk_other_check else 0
    brch_light_check = st.checkbox(
        "Branch problems caused by lights or wires", value=False
    )
    brch_light = 1 if brch_light_check else 0
    brch_shoe_check = st.checkbox("Branch problems caused by shoes", value=False)
    brch_shoe = 1 if brch_shoe_check else 0
    brch_other_check = st.checkbox("Presence of other branch problems", value=False)
    brch_other = 1 if brch_other_check else 0
    spc_common = st.text_input("Common name of tree species", value="green ash")
    zip_city = st.text_input("City, as derived from zipcode", value="Ozone Park")
    borough = st.selectbox(
        "Borough Name",
        options=["Manhattan", "Bronx", "Brooklyn", "Queens", "Staten Island"],
    )
    user_type = st.selectbox(
        "Category of user who collected this tree point",
        options=["Volunteer", "TreesCount Staff", "NYC Parks Staff"],
    )

    submit_button = st.form_submit_button("Click on me")

    if submit_button:
        # features = [tree_dbh, curb_loc, steward, guards, sidewalk, problems,
        #             root_stone, root_grate, root_other, trunk_wire, trnk_light,
        #             trnk_other, brch_light, brch_shoe, brch_other, spc_common,
        #             zip_city, borough, user_type]
        # path_to_model = os.path.join(
        #     os.path.abspath(os.getcwd()),
        #     "src/resources",
        #     "model.bin",
        # )
        # model = get_model(path_to_model)
        # prediction = model.predict_proba(features)
        # health_classes = {0: "Poor", 1: "Fair", 2: "Good"}
        # result = {
        #     name_health: round(score, 4)
        #     for name_health, score in zip(health_classes.values(), prediction)
        # }
        result = predict_health(
            tree_dbh,
            curb_loc,
            steward,
            guards,
            sidewalk,
            problems,
            root_stone,
            root_grate,
            root_other,
            trunk_wire,
            trnk_light,
            trnk_other,
            brch_light,
            brch_shoe,
            brch_other,
            spc_common,
            zip_city,
            borough,
            user_type,
        )
        st.write("Probability of stages health of tree:")
        st.text(result)

        categories = list(result.keys())
        values = list(result.values())
        fig, ax = plt.subplots()
        bars = ax.barh(categories, values, color=["red", "yellow", "green"])
        ax.set_xlim(0, 1)
        ax.set_xlabel("Probability")
        ax.set_title("Probability of health for tree")
        for bar in bars:
            width = bar.get_width()
            label_x_position = width + 0.01
            ax.text(
                label_x_position,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.3f}",
                va="center",
            )

        st.pyplot(fig)
