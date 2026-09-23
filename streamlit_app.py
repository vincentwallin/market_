import streamlit as st

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Fiskfötter",
    page_icon="🐟",
    layout="wide"
)

# =========================
# DARK DESIGN
# =========================

st.markdown("""
<style>

.stApp {
    background-color: #0d1117;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #090d12;
}

h1, h2, h3 {
    color: white;
}

.item-box {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 8px;
}

.completed {
    opacity: 0.5;
    text-decoration: line-through;
}

.list-card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION DATA
# =========================

if "lists" not in st.session_state:
    st.session_state.lists = {
        "Handlingslista": []
    }

if "selected_list" not in st.session_state:
    st.session_state.selected_list = "Handlingslista"

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("🐟 Fiskfötter")

    st.divider()

    st.subheader("Dina listor")

    # Select list
    list_names = list(st.session_state.lists.keys())

    selected = st.selectbox(
        "Välj lista",
        list_names,
        index=list_names.index(st.session_state.selected_list)
    )

    st.session_state.selected_list = selected

    st.divider()

    # Create new list
    st.subheader("Ny lista")

    new_list = st.text_input(
        "Namn",
        placeholder="T.ex. Skolan"
    )

    if st.button("➕ Skapa lista", use_container_width=True):

        if new_list.strip():

            if new_list.strip() not in st.session_state.lists:

                st.session_state.lists[new_list.strip()] = []
                st.session_state.selected_list = new_list.strip()
                st.rerun()

            else:
                st.error("Den listan finns redan.")

    st.divider()

    # Delete current list
    if len(st.session_state.lists) > 1:

        if st.button(
            "🗑️ Ta bort lista",
            use_container_width=True
        ):

            del st.session_state.lists[
                st.session_state.selected_list
            ]

            st.session_state.selected_list = list(
                st.session_state.lists.keys()
            )[0]

            st.rerun()

# =========================
# CURRENT LIST
# =========================

current_list = st.session_state.selected_list
items = st.session_state.lists[current_list]

# =========================
# HEADER
# =========================

st.title(f"📋 {current_list}")

completed = sum(
    1 for item in items
    if item["completed"]
)

total = len(items)

if total > 0:
    progress = completed / total

    st.progress(progress)

    st.caption(
        f"{completed} av {total} klara"
    )
else:
    st.caption("Listan är tom.")

# =========================
# ADD ITEM
# =========================

st.subheader("Lägg till")

col1, col2 = st.columns([4, 1])

with col1:

    new_item = st.text_input(
        "Nytt objekt",
        placeholder="T.ex. Mjölk",
        label_visibility="collapsed"
    )

with col2:

    add_button = st.button(
        "➕ Lägg till",
        use_container_width=True
    )

if add_button:

    if new_item.strip():

        items.append({
            "text": new_item.strip(),
            "completed": False
        })

        st.rerun()

# =========================
# SEARCH
# =========================

st.subheader("🔍 Sök")

search = st.text_input(
    "Sök i listan",
    placeholder="Skriv för att söka...",
    label_visibility="collapsed"
)

# =========================
# ITEMS
# =========================

st.subheader("Lista")

if not items:

    st.info("Den här listan är tom.")

else:

    for i, item in enumerate(items):

        # Search filter
        if search and search.lower() not in item["text"].lower():
            continue

        col1, col2, col3 = st.columns([1, 6, 1])

        with col1:

            checked = st.checkbox(
                "",
                value=item["completed"],
                key=f"check_{current_list}_{i}"
            )

            if checked != item["completed"]:
                item["completed"] = checked
                st.rerun()

        with col2:

            if item["completed"]:

                st.markdown(
                    f"""
                    <div class="item-box completed">
                        {item["text"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="item-box">
                        {item["text"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col3:

            if st.button(
                "🗑️",
                key=f"delete_{current_list}_{i}"
            ):

                items.pop(i)
                st.rerun()

# =========================
# CLEAR COMPLETED
# =========================

if any(item["completed"] for item in items):

    st.divider()

    if st.button(
        "🧹 Ta bort alla klara",
        use_container_width=True
    ):

        st.session_state.lists[current_list] = [
            item
            for item in items
            if not item["completed"]
        ]

        st.rerun()

# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    f"🐟 Fiskfötter • {len(st.session_state.lists)} listor"
)
