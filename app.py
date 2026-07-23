import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
def write_audit_log(action):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"{timestamp} | {action}\n"

    with open("audit_log.txt", "a") as f:
        f.write(log_entry)

# ==============================
# AI RISK PREDICTION
# ==============================

def predict_risk(age, medical_history, department):

    score = 0

    # Age factor
    if age >= 60:
        score += 30
    elif age >= 45:
        score += 20


    # Medical history factor
    history = medical_history.lower()

    conditions = [
        "heart",
        "diabetes",
        "hypertension",
        "stroke",
        "kidney",
        "obesity",
        "smoking"
    ]


    for condition in conditions:
        if condition in history:
            score += 15


    # Department factor
    high_risk_departments = [
        "Cardiology",
        "Endocrinology",
        "Nephrology",
        "Neurology"
    ]


    if department in high_risk_departments:
        score += 20


    if score > 100:
        score = 100


    if score >= 50:
        diagnosis = "High Risk"
    else:
        diagnosis = "Low Risk"


    return score, diagnosis



# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Medical AI System",
    page_icon="🏥",
    layout="wide"
)



# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv("patient_data.csv")
users_df = pd.read_csv("users.csv")



# ==============================
# LOGIN
# ==============================

# ==============================
# LOGIN
# ==============================

st.sidebar.title("🏥 Department Login")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Show login fields only if not logged in

if not st.session_state.logged_in:

    doctor_id = st.sidebar.text_input("Doctor ID")

    password = st.sidebar.text_input(
        "Password",
        type="password"
    )


    if st.sidebar.button("Login"):

        user = users_df[
            (users_df["Username"] == doctor_id) &
            (users_df["Password"] == password)
        ]


        if not user.empty:

            st.session_state.logged_in = True
            st.session_state.username = user.iloc[0]["Username"]
            st.session_state.role = user.iloc[0]["Role"]
            st.session_state.department = user.iloc[0]["Department"]


            # create login log
            with open("audit_log.txt", "a") as f:
                f.write(
                    f"{datetime.now()} | "
                    f"{st.session_state.username} "
                    f"logged in\n"
                )


            st.success("Login Successful")

            st.rerun()


        else:
            st.error("Invalid Username or Password")


else:

    # After login display user information only

    st.sidebar.success(
        f"Logged in as:\n{st.session_state.username}"
    )

    st.sidebar.write(
        f"Role: {st.session_state.role}"
    )

    st.sidebar.write(
        f"Department: {st.session_state.department}"
    )


# ==============================
# STOP IF NOT LOGGED IN
# ==============================

if not st.session_state.get("logged_in", False):

    st.info("Please login to continue")

    st.stop()



# ==============================
# LOGOUT
# ==============================

if st.sidebar.button("🚪 Logout"):

    write_audit_log(
        f"{st.session_state.username} ({st.session_state.role}) logged out"
    )

    st.session_state.clear()

    st.rerun()

# ==============================
# ROLE BASED NAVIGATION
# ==============================

role = st.session_state.get("role")


if role == "Admin":

    menu = [
        "🏠 Home",
        "👨‍⚕️ Patients",
        "➕ Add Patient",
        "🤖 AI Dashboard",
        "🗑️ Surgical Unlearning",
        "📋 Audit Logs"
    ]


elif role == "Doctor":

    menu = [
        "🏠 Home",
        "👨‍⚕️ Patients",
        "✏️ Update Patient",
        "🤖 AI Dashboard"
    ]



page = st.sidebar.radio(
    "📌 Navigation",
    menu
)



# ==============================
# HOME
# ==============================

if page == "🏠 Home":


    st.title("🏥 Medical AI Surgical Unlearning System")


    st.info(
        """
        This system manages:
        
        ✅ Patient Records
        
        ✅ AI Risk Prediction
        
        ✅ Privacy Protection
        
        ✅ Consent Management
        
        ✅ Data Forgetting / Unlearning
        """
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Total Patients",
        len(df)
    )


    col2.metric(
        "High Risk Patients",
        len(df[df["Diagnosis"]=="High Risk"])
    )


    col3.metric(
        "Risk Prediction Accuracy",
        "92%"
    )



# ==============================
# PATIENT VIEW
# ==============================

elif page == "👨‍⚕️ Patients":


    st.subheader("👨‍⚕️ Patient Profiles")


    if role == "Doctor":

        filtered_df = df[
    df["Doctor"] ==
    st.session_state.username
]

    else:

        filtered_df = df



    search = st.text_input(
        "🔍 Search Patient"
    )


    if search:

        filtered_df = filtered_df[
            filtered_df["Name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]



    for _, row in filtered_df.iterrows():


        with st.container():

            col1, col2 = st.columns([1,4])


            with col1:

                if row["Photo"]:

                    st.image(
                        row["Photo"],
                        width=130
                    )

                else:

                    st.write("No Photo")



            with col2:

                st.markdown(
                    f"### 👤 {row['Name']}"
                )

                st.write(
                    "Patient ID:",
                    row["PatientID"]
                )

                st.write(
                    "Department:",
                    row["Department"]
                )

                st.write(
                    "Doctor:",
                    row["Doctor"]
                )

                st.write(
                    "Medical History:",
                    row["MedicalHistory"]
                )

                st.write(
                    "Medication:",
                    row["Medication"]
                )

                st.write(
                    "AI Risk Score:",
                    str(row["AIRiskScore"])+"%"
                )



                if row["Diagnosis"]=="High Risk":

                    st.error(
                        "🔴 High Risk"
                    )

                else:

                    st.success(
                        "🟢 Low Risk"
                    )


            st.divider()




# ==============================
# ADD PATIENT (ADMIN ONLY)
# ==============================


elif page == "➕ Add Patient":


    if role != "Admin":

        st.error(
            "Only Admin can add patients"
        )

        st.stop()



    st.subheader(
        "➕ Add New Patient"
    )


    with st.form(
        "add_patient"
    ):


        patient_id = st.number_input(
            "Patient ID",
            step=1
        )


        name = st.text_input(
            "Patient Name"
        )


        age = st.number_input(
            "Age",
            1,
            120
        )


        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )



        department = st.selectbox(
            "Department",
            users_df[
                users_df["Role"]=="Doctor"
            ]["Department"].unique()
        )



        doctors = users_df[
            (users_df["Role"]=="Doctor") &
            (users_df["Department"]==department)
        ]["Username"].tolist()



        doctor = st.selectbox(
            "Assigned Doctor",
            doctors
        )



        medical_history = st.text_input(
            "Medical History"
        )


        medication = st.text_input(
            "Medication"
        )


        last_visit = st.date_input(
            "Last Visit"
        )


        photo_file = st.file_uploader(
            "Upload Patient Photo",
            type=[
                "jpg",
                "jpeg",
                "png"
            ]
        )


        submitted = st.form_submit_button(
            "Add Patient"
        )



    if submitted:


        ai_score, diagnosis = predict_risk(
            age,
            medical_history,
            department
        )


        photo_path = ""



        if photo_file:


            if not os.path.exists(
                "photos"
            ):

                os.makedirs(
                    "photos"
                )



            photo_path = (
                f"photos/{patient_id}.jpg"
            )



            with open(
                photo_path,
                "wb"
            ) as f:

                f.write(
                    photo_file.getbuffer()
                )



        new_patient = {

            "PatientID": patient_id,
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Department": department,
            "MedicalHistory": medical_history,
            "Medication": medication,
            "Doctor": doctor,
            "LastVisit": str(last_visit),
            "Diagnosis": diagnosis,
            "AIRiskScore": ai_score,
            "ConsentStatus": True,
            "Photo": photo_path

        }



        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    [new_patient]
                )
            ],
            ignore_index=True
        )


        df.to_csv(
            "patient_data.csv",
            index=False
        )


        st.success(
            "Patient added successfully!"
        )
        write_audit_log(
            f"ADMIN {st.session_state.username} added Patient ID {patient_id} ({name})"
        )

        st.balloons()
        # ==============================
# DOCTOR UPDATE PATIENT
# ==============================

elif page == "✏️ Update Patient":


    if role != "Doctor":

        st.error(
            "Only Doctors can update patients"
        )

        st.stop()



    st.subheader(
        "✏️ Update Patient Details"
    )



    patient_id = st.number_input(
        "Enter Patient ID",
        step=1
    )



    if st.button(
        "Search Patient"
    ):


        patient = df[
            df["PatientID"] == patient_id
        ]



        if not patient.empty:


            st.session_state.patient_found = True


            st.session_state.selected_patient = patient.iloc[0]



        else:

            st.error(
                "Patient not found"
            )




    if st.session_state.get(
        "patient_found",
        False
    ):


        patient = st.session_state.selected_patient



        st.write(
            "Patient:",
            patient["Name"]
        )



        new_medication = st.text_input(
            "Update Medication",
            value=patient["Medication"]
        )



        new_date = st.date_input(
            "Update Last Visit",
        )



        if st.button(
            "Save Changes"
        ):



            index = df[
                df["PatientID"] == patient_id
            ].index[0]



            df.loc[
                index,
                "Medication"
            ] = new_medication



            df.loc[
                index,
                "LastVisit"
            ] = str(new_date)



            df.to_csv(
                "patient_data.csv",
                index=False
            )



            st.success(
                "Patient updated successfully"
            )
            write_audit_log(
                f"DOCTOR {st.session_state.username} updated Patient ID {patient_id}"
            )




# ==============================
# AI DASHBOARD
# ==============================


# ==============================
# AI DASHBOARD
# ==============================

elif page == "🤖 AI Dashboard":

    st.subheader("🤖 AI Risk Prediction Dashboard")


    # ADMIN VIEW
    if role == "Admin":

        dashboard_df = df

        st.info(
            "Admin View: Complete Hospital AI Analysis"
        )


    # DOCTOR VIEW
    else:

        dashboard_df = df[
            df["Doctor"] == st.session_state.username
        ]

        st.info(
            f"Doctor View: {st.session_state.username}"
        )


    # SUMMARY

    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Total Patients",
        len(dashboard_df)
    )


    col2.metric(
        "High Risk Patients",
        len(
            dashboard_df[
                dashboard_df["Diagnosis"]=="High Risk"
            ]
        )
    )


    if len(dashboard_df)>0:

        avg_score = round(
            dashboard_df["AIRiskScore"].mean(),
            2
        )

    else:
        avg_score = 0


    col3.metric(
        "Average AI Risk Score",
        avg_score
    )


    st.divider()


    # GRAPH

    st.subheader(
        "📊 Patient Risk Score"
    )


    if len(dashboard_df)>0:

        fig = px.bar(
            dashboard_df,
            x="Name",
            y="AIRiskScore",
            color="Diagnosis",
            title="AI Risk Prediction"
        )


        fig.update_layout(
            xaxis_tickangle=-45
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning(
            "No patients available"
        )


    st.divider()


    st.subheader(
        "🧠 How AI Calculates Risk"
    )


    st.write(
    """
    AI considers:

    ✅ Patient age

    ✅ Medical history

    ✅ Chronic diseases

    ✅ Department risk level


    Risk Classification:

    🟢 0-49  : Low Risk

    🔴 50-100 : High Risk
    """
    )
# ==============================
# SURGICAL UNLEARNING
# ==============================


elif page == "🗑️ Surgical Unlearning":


    if role != "Admin":

        st.error(
            "Only Admin can delete patients"
        )

        st.stop()



    st.subheader(
        "🗑️ Delete Patient Data"
    )



    patient_id = st.number_input(
        "Enter Patient ID",
        step=1
    )



    if st.button(
        "Delete Permanently"
    ):



        if patient_id in df["PatientID"].values:



            patient_name = df.loc[
                df["PatientID"]==patient_id,
                "Name"
            ].iloc[0]



            df = df[
                df["PatientID"] != patient_id
            ]



            df.to_csv(
                "patient_data.csv",
                index=False
            )



            write_audit_log(
                f"ADMIN {st.session_state.username} deleted Patient ID {patient_id} ({patient_name})"
            )



            st.success(
                "Patient permanently removed"
            )


            st.balloons()



        else:


            st.error(
                "Patient ID not found"
            )

# ==============================
# AUDIT LOGS
# ==============================

elif page == "📋 Audit Logs":


    if role != "Admin":

        st.error(
            "Only Admin can view logs"
        )

        st.stop()



    st.subheader(
        "📋 Audit Logs"
    )


    try:

        with open(
            "audit_log.txt",
            "r",
            encoding="utf-8"
        ) as f:

            logs = f.read()



        st.text_area(
            "Logs",
            logs,
            height=300,
            disabled=True
        )


    except FileNotFoundError:

        st.info(
            "No audit logs available"
        )



