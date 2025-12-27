import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime


# paths
BASE_DIR = os.getcwd()
USERS_FILE = os.path.join(BASE_DIR, "users.csv")
FILES_FILE = os.path.join(BASE_DIR, "userfiles.csv")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


# setup folders + csv files
def setup_storage():
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    if not os.path.exists(USERS_FILE):
        pd.DataFrame(
            columns=["userid", "username", "password_hash", "created_at"]
        ).to_csv(USERS_FILE, index=False)

    if not os.path.exists(FILES_FILE):
        pd.DataFrame(
            columns=["userid", "original_name", "saved_path", "uploaded_at"]
        ).to_csv(FILES_FILE, index=False)


# password hashing
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def get_users():
    return pd.read_csv(USERS_FILE)


def register_user(username, password):
    users = get_users()

    if username in users["username"].values:
        return False, "Username already exists"

    new_id = int(users["userid"].max()) + 1 if not users.empty else 1

    users.loc[len(users)] = {
        "userid": new_id,
        "username": username,
        "password_hash": hash_pw(password),
        "created_at": datetime.now().isoformat()
    }

    users.to_csv(USERS_FILE, index=False)
    return True, new_id


def login_user(username, password):
    users = get_users()

    if username not in users["username"].values:
        return False, "User not found"

    row = users[users["username"] == username].iloc[0]
    if row["password_hash"] == hash_pw(password):
        return True, int(row["userid"])

    return False, "Invalid password"


def save_file_info(userid, original, path):
    df = pd.read_csv(FILES_FILE)

    df.loc[len(df)] = {
        "userid": userid,
        "original_name": original,
        "saved_path": path,
        "uploaded_at": datetime.now().isoformat()
    }

    df.to_csv(FILES_FILE, index=False)


def fetch_user_files(userid):
    df = pd.read_csv(FILES_FILE)
    return df[df["userid"] == userid]


def main():
    setup_storage()

    if "user" not in st.session_state:
        st.session_state.user = None

    st.sidebar.title("Menu")

    if st.session_state.user is None:
        choice = st.sidebar.selectbox("Choose", ["Home", "Login", "Register"])
    else:
        choice = st.sidebar.selectbox(
            "Choose", ["Explore CSV", "See history", "Logout"]
        )

    st.title("CSV Explorer App")

    if choice == "Home":
        st.write("Welcome! Please login or register to use the app.")

    elif choice == "Register":
        st.subheader("Register")

        uname = st.text_input("Username")
        pw = st.text_input("Password", type="password")

        if st.button("Register"):
            ok, result = register_user(uname, pw)

            if ok:
                st.session_state.user = {
                    "userid": result,
                    "username": uname
                }
                st.success("Registered and logged in successfully")
                st.rerun()
            else:
                st.error(result)

    elif choice == "Login":
        st.subheader("Login")

        uname = st.text_input("Username", key="login_name")
        pw = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            ok, result = login_user(uname, pw)

            if ok:
                st.session_state.user = {
                    "userid": result,
                    "username": uname
                }
                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error(result)

    elif choice == "Logout":
        st.session_state.user = None
        st.success("Logged out")
        st.rerun()

    elif choice == "Explore CSV":
        st.subheader("Explore CSV")
        st.write(f"Logged in as **{st.session_state.user['username']}**")

        uploaded = st.file_uploader("Upload CSV file", type=["csv"])

        if uploaded:
            fname = (
                f"user{st.session_state.user['userid']}_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_"
                f"{uploaded.name}"
            )

            full_path = os.path.join(UPLOAD_DIR, fname)

            with open(full_path, "wb") as f:
                f.write(uploaded.getbuffer())

            save_file_info(
                st.session_state.user["userid"],
                uploaded.name,
                full_path
            )

            st.success("File uploaded")
            st.dataframe(pd.read_csv(full_path))

        history = fetch_user_files(st.session_state.user["userid"])
        if not history.empty:
            selected = st.selectbox(
                "Load previous file",
                history["saved_path"]
            )

            if st.button("Load"):
                st.dataframe(pd.read_csv(selected))

    elif choice == "See history":
        st.subheader("Upload History")

        history = fetch_user_files(st.session_state.user["userid"])
        if history.empty:
            st.info("No files uploaded yet.")
        else:
            st.dataframe(history)


if __name__ == "__main__":
    main()
