import pandas as pd
import streamlit as st
from PIL import Image
import pickle as pk
from sklearn.preprocessing import LabelEncoder
import os

def Prediction(inputData):
    model = pk.load(open("HeartModel.pkl", "rb"))
    prediction = model.predict(inputData)
    return prediction

# Set page configuration
st.set_page_config(page_title="Heart Disease Prediction", page_icon="❤️", layout="wide")

# Function to reset session state
def reset_session_state():
    for key in st.session_state.keys():
        del st.session_state[key]

# Apply custom CSS
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #e63946;
        color: white;
        font-size: 16px;
        padding: 10px;
        border-radius: 5px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #d62828;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Home page logic
if "role" not in st.session_state:
    # Display the front page
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 3em;
            color: #e63946;
            text-align: center;
            font-weight: bold;
            margin-top: 20px;
        }
        .description {
            text-align: center;
            font-size: 1.2em;
            color: #1d3557;
            margin-bottom: 20px;
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 50px;
            margin-top: 30px;
        }
        .button-container > div {
            text-align: center;
        }
        .icon {
            font-size: 50px;
            color: #457b9d;
            margin-bottom: 10px;
        }
        .button-label {
            font-size: 1.2em;
            font-weight: bold;
            color: #1d3557;
            margin-bottom: 15px;
        }
        .stButton > button {
            width: 80%;
            margin: 10px auto;
            display: block;
            padding: 10px;
            font-size: 1em;
            background-color: #e63946;
            color: white;
            border: none;
            border-radius: 5px;
        }
        </style>
        <h1 class="main-title">Heart Disease Prediction Application</h1>
        <p class="description">Welcome to a user-friendly platform that uses Machine Learning to help predict heart disease risk. Choose your role below to proceed.</p>
        """,
        unsafe_allow_html=True
    )

    # Add an image (optional)
    try:
        image = Image.open("h2.png")  # Replace with your image file path
        st.image(image, caption="Stay Heart Healthy!", use_container_width=True)
    except:
        st.write("")
    
    # Role selection buttons with icons and buttons
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style="text-align: center;">
                <div class="icon">🔐</div>
                <p class="button-label">Admin Login</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Login as Admin"):
            st.session_state["role"] = "admin"    

    with col2:
        st.markdown(
            """
            <div style="text-align: center;">
                <div class="icon">👥</div>
                <p class="button-label">Patient Access</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Enter as Patient"):
            st.session_state["role"] = "patient"


# Logic for the Patient and Admin sections
if "role" in st.session_state:
    if st.session_state["role"] == "patient":
        # Patient page
        st.title("Heart Disease Prediction: Patient Section")
     
        st.markdown("<h3 style='text-align: center;'>Patient Login</h3>", unsafe_allow_html=True)
        patient_username = st.text_input("Patient ID")
        patient_password = st.text_input("Patient Password", type="password")
        if st.button("Enter as Patient", key="patient_btn"):
            if patient_username and patient_password:  # Replace with actual authentication logic
                st.session_state["role"] = "patient"
                st.success("Patient Login Successful!")
            else:
                st.error("Invalid Patient Credentials")
        
       


        # Add a back button
        if st.button("Back to Main Page"):
            reset_session_state()

        # Create sections
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Enter Parameters", "View Results", "Suggested Doctor", "Give Feedback"])

        if page == "Enter Parameters":
            st.header("Enter Parameter Values")
            st.markdown("### Provide your health details below:")

            # Collect user inputs
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=1, max_value=120, step=1)
            sex_label = st.selectbox("Sex", ["Male", "Female"])
            sex_map = {"Male": 1, "Female": 0}
            sex = sex_map[sex_label]
            chest_pain = st.selectbox("Chest Pain Type", [
                "Typical Angina",
                "Atypical Angina",
                "Non-anginal Pain",
                "Asymptomatic"
            ])
            rest_bp = st.number_input("Resting Blood Pressure (mmHg)", min_value=50, max_value=250, step=1)
            chol = st.number_input("Cholesterol Level (mg/dL)", min_value=0, max_value=600, step=1)
            fbs_label = st.selectbox("Fasting Blood Sugar > 120 mg/dL", ["True", "False"])
            fbs_map = {"True": 1, "False": 0}
            fbs = fbs_map[fbs_label]

            rest_ecg_label = st.selectbox("Resting Electrocardiographic Results", [
                "Normal",
                "ST-T Wave Abnormality",
                "Probable or Definite Left Ventricular Hypertrophy"
            ])
            rest_ecg_map = {
                "Normal": 0,
                "ST-T Wave Abnormality": 1,
                "Probable or Definite Left Ventricular Hypertrophy": 2
            }
            rest_ecg = rest_ecg_map[rest_ecg_label]
            max_hr = st.number_input("Maximum Heart Rate Achieved", min_value=0, max_value=300, step=1)
            ex_ang_label = st.selectbox("Exercise-Induced Angina", ["Yes", "No"])
            ex_ang_map = {"Yes": 1, "No": 0}
            ex_ang = ex_ang_map[ex_ang_label]
            oldpeak = st.number_input("Oldpeak (ST Depression Induced by Exercise Relative to Rest)", min_value=0.0, max_value=10.0, step=0.1)
            slope_label = st.selectbox("Slope of the Peak Exercise ST Segment", [
                "Upsloping",
                "Flat",
                "Downsloping"
            ])
            slope_map = {
                "Upsloping": 1,
                "Flat": 2,
                "Downsloping": 3
            }
            slope = slope_map[slope_label]
            ca = st.number_input("Number of Major Vessels (0-3) Colored by Flourosopy", min_value=0, max_value=3, step=1)
            thal = st.selectbox("Thalassemia", [
                "normal",
                "fixed",
                "reversible"
            ])
            data = {'Name': name,
                    'Age': age,
                    'Sex': sex,
                    'ChestPain': chest_pain,
                    'RestBP': rest_bp,
                    'Chol': chol,
                    'Fbs': fbs,
                    'RestECG': rest_ecg,
                    'MaxHR': max_hr,
                    'ExAng': ex_ang,
                    'Oldpeak': oldpeak,
                    'Slope': slope,
                    'Ca': ca,
                    'Thal': thal}
            features = pd.DataFrame(data, index=[0])

            label_encoders = {}
            for column in ['ChestPain', 'Thal']:
                le = LabelEncoder()
                features[column] = le.fit_transform(features[column])
                label_encoders[column] = le
            X = features

            if st.button("Submit"):
                prediction = Prediction(X.drop(columns=['Name']))  # Drop 'Name' for prediction
                st.session_state['prediction'] = prediction
                st.session_state['patient_name'] = name
                st.success("Parameters submitted successfully!")
                if prediction == 1:
                    st.write("Positive.... You must consult a doctor")
                elif prediction == 0:
                    st.write("Negative.... ")

                # Save data to CSV
                file_path = "patient_data.csv"

                # Include the prediction result in the data
                features['Prediction'] = prediction

                if os.path.exists(file_path):
                    # Append to existing file
                    existing_data = pd.read_csv(file_path)
                    updated_data = pd.concat([existing_data, features], ignore_index=True)
                    updated_data.to_csv(file_path, index=False)
                else:
                    # Create a new file
                    features.to_csv(file_path, index=False)

        elif page == "View Results":
            st.header("View Results")
            if 'prediction' in st.session_state:
                name = st.session_state.get('patient_name', 'Patient')
                st.markdown(f"### Prediction Result for {name}: {st.session_state['prediction']}")
            else:
                st.warning("No prediction results available. Please submit your parameters first.")

        elif page == "Suggested Doctor":
            file_path = "dummy_doctor_data.csv"  # Ensure the correct path to your CSV file
            try:
                doctors_df = pd.read_csv(file_path)
                st.header("View Suggested Doctor")
                st.markdown("### All Available Doctors")
                st.dataframe(doctors_df)
            except FileNotFoundError:
                st.error("Doctor data not found. Please upload the data.")

        elif page == "Give Feedback":
            st.header("Give Feedback")
            name = st.text_input("Name")
            feedback = st.text_area("Please provide your feedback about the application:")
            feedback_file_path = "feedback_data.csv"
            if st.button("Submit Feedback"):
                if feedback:  # Check if feedback is not empty
                    # Create a new entry as a DataFrame
                    new_entry = pd.DataFrame({'Name': [name], 'Feedback': [feedback]})

                    try:
                        # Try to load the existing feedback data
                        existing_feedback = pd.read_csv(feedback_file_path)

                        # Append the new entry to the existing feedback
                        updated_feedback = pd.concat([existing_feedback, new_entry], ignore_index=True)
                    except FileNotFoundError:
                        # If the file does not exist, use the new entry as the initial DataFrame
                        updated_feedback = new_entry

                    # Save the updated feedback back to the CSV file, preserving previous data
                    updated_feedback.to_csv(feedback_file_path, index=False)

                    st.success("Thank you for your feedback!")
                else:
                    st.error("Feedback cannot be empty.")

    elif st.session_state["role"] == "admin":
        # Admin page
        st.title("Admin Login")
        admin_username = st.text_input("Username", key="admin_username")
        admin_password = st.text_input("Password", type="password", key="admin_password")

        if st.button("Login"):
            # Authentication
            if admin_username == "admin" and admin_password == "admin123":
                st.session_state["role"] = "admin_authenticated"
                st.success("Welcome, Admin!")
            else:
                st.error("Invalid credentials. Please try again.")

    elif st.session_state["role"] == "admin_authenticated":
        st.title("Admin Dashboard")
        st.sidebar.title("Admin Navigation")
        page = st.sidebar.radio(
            "Go to",
            ["Manage Patients", "Manage Doctors", "Manage Feedback"]
        )

        # Back button to return to the main page
        if st.button("Back to Main Page"):
            reset_session_state()



        if page == "Manage Patients":
            st.header("Manage Patients")

            patient_file_path = "patient_data.csv"  # Ensure this path is correct

            # Load patient data
            try:
                patient_df = pd.read_csv(patient_file_path)
            except FileNotFoundError:
                # Create an empty DataFrame with the required columns if file does not exist
                patient_df = pd.DataFrame(columns=["Name", "Age", "Sex", "ChestPain", "RestBP", "Chol", "Fbs", "RestECG", "MaxHR", "ExAng", "Oldpeak", "Slope", "Ca", "Thal", "Prediction"])
                patient_df.to_csv(patient_file_path, index=False)

            # Display patient data
            st.markdown("### Patient Records")
            if not patient_df.empty:
                st.dataframe(patient_df)

                # Delete patient details
                st.markdown("### Delete Patient")
                delete_patient_index = st.selectbox(
                    "Select Patient to Delete",
                    patient_df.index,
                    format_func=lambda x: f"{patient_df.at[x, 'Name']} - Age: {patient_df.at[x, 'Age']}"
                )

                if st.button("Delete Selected Patient"):
                    patient_df = patient_df.drop(index=delete_patient_index).reset_index(drop=True)
                    patient_df.to_csv(patient_file_path, index=False)
                    st.success("Patient deleted successfully!")

            else:
                st.warning("No patient records found.")

            # Add new patient
            st.markdown("### Add New Patient")
            with st.form("add_patient"):
                name = st.text_input("Name")
                age = st.number_input("Age", min_value=1, max_value=120, step=1)
                sex_label = st.selectbox("Sex", ["Male", "Female"])
                sex_map = {"Male": 1, "Female": 0}
                sex = sex_map[sex_label]
                chest_pain = st.selectbox("Chest Pain Type", [
                    "Typical Angina",
                    "Atypical Angina",
                    "Non-anginal Pain",
                    "Asymptomatic"
                ])
                rest_bp = st.number_input("Resting Blood Pressure (mmHg)", min_value=50, max_value=250, step=1)
                chol = st.number_input("Cholesterol Level (mg/dL)", min_value=0, max_value=600, step=1)
                fbs_label = st.selectbox("Fasting Blood Sugar > 120 mg/dL", ["True", "False"])
                fbs_map = {"True": 1, "False": 0}
                fbs = fbs_map[fbs_label]

                rest_ecg_label = st.selectbox("Resting Electrocardiographic Results", [
                    "Normal",
                    "ST-T Wave Abnormality",
                    "Probable or Definite Left Ventricular Hypertrophy"
                ])
                rest_ecg_map = {
                    "Normal": 0,
                    "ST-T Wave Abnormality": 1,
                    "Probable or Definite Left Ventricular Hypertrophy": 2
                }
                rest_ecg = rest_ecg_map[rest_ecg_label]
                max_hr = st.number_input("Maximum Heart Rate Achieved", min_value=0, max_value=300, step=1)
                ex_ang_label = st.selectbox("Exercise-Induced Angina", ["Yes", "No"])
                ex_ang_map = {"Yes": 1, "No": 0}
                ex_ang = ex_ang_map[ex_ang_label]
                oldpeak = st.number_input("Oldpeak (ST Depression Induced by Exercise Relative to Rest)", min_value=0.0, max_value=10.0, step=0.1)
                slope_label = st.selectbox("Slope of the Peak Exercise ST Segment", [
                    "Upsloping",
                    "Flat",
                    "Downsloping"
                ])
                slope_map = {
                    "Upsloping": 1,
                    "Flat": 2,
                    "Downsloping": 3
                }
                slope = slope_map[slope_label]
                ca = st.number_input("Number of Major Vessels (0-3) Colored by Flourosopy", min_value=0, max_value=3, step=1)
                thal = st.selectbox("Thalassemia", [
                    "normal",
                    "fixed",
                    "reversible"
                ])

                if st.form_submit_button("Add Patient"):
                    new_patient = pd.DataFrame({
                        "Name": [name],
                        "Age": [age],
                        "Sex": [sex],
                        "ChestPain": [chest_pain], 
                        "RestBP": [rest_bp], 
                        "Chol": [chol],
                        "Fbs": [fbs],
                        "RestECG": [rest_ecg], 
                        "MaxHR": [max_hr], 
                        "ExAng": [ex_ang], 
                        "Oldpeak": [oldpeak],
                        "Slope": [slope],
                        "Ca": [ca],
                        "Thal": [thal],
                        "Prediction": ["Not Available"]
                    })
                    patient_df = pd.concat([patient_df, new_patient], ignore_index=True)
                    patient_df.to_csv(patient_file_path, index=False)
                    st.success("Patient added successfully!")

            # Update Patient
            st.markdown("### Update Patient")
            if patient_df.empty:
                st.warning("No patient data available for update.")
            else:
                # Ensure a default selection for patient index
                if "update_patient_index" not in st.session_state or st.session_state.update_patient_index not in patient_df.index:
                    st.session_state.update_patient_index = patient_df.index[0]  # Default to the first row

                # Select the patient to update
                patient_index = st.selectbox(
                    "Select Patient to Update",
                        patient_df.index,
                        format_func=lambda x: f"{patient_df.at[x, 'Name']} - Age: {patient_df.at[x, 'Age']}",
                        key="update_patient_index"
                )

                # Form to update patient details
                with st.form("update_patient"):
                    updated_name = st.text_input("Name", value=patient_df.at[patient_index, 'Name'])
                    updated_age = st.number_input("Age", min_value=0, max_value=120, value=int(patient_df.at[patient_index, 'Age']))
                    updated_sex = st.selectbox("Sex", ["Male", "Female"], index=0 if patient_df.at[patient_index, 'Sex'] == "Male" else 1)
                    updated_chest_pain = st.text_input("Chest Pain", value=patient_df.at[patient_index, 'ChestPain'])
                    updated_rest_bp = st.number_input("Resting Blood Pressure (mmHg)", min_value=50, max_value=250, value=int(patient_df.at[patient_index, 'RestBP']))
                    updated_chol = st.number_input("Cholesterol Level (mg/dL)", min_value=0, max_value=600, value=int(patient_df.at[patient_index, 'Chol']))
                    updated_fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", ["True", "False"], index=0 if patient_df.at[patient_index, 'Fbs'] == "True" else 1)
                    updated_rest_ecg = st.text_input("Resting ECG Results", value=patient_df.at[patient_index, 'RestECG'])
                    updated_max_hr = st.number_input("Maximum Heart Rate Achieved", min_value=0, max_value=300, value=int(patient_df.at[patient_index, 'MaxHR']))
                    updated_ex_ang = st.selectbox("Exercise-Induced Angina", ["Yes", "No"], index=0 if patient_df.at[patient_index, 'ExAng'] == "Yes" else 1)
                    updated_oldpeak = st.number_input("Oldpeak", min_value=0.0, max_value=10.0, step=0.1, value=float(patient_df.at[patient_index, 'Oldpeak']))
                    updated_slope = st.number_input("Slope", min_value=1, max_value=3, step=1, value=int(patient_df.at[patient_index, 'Slope']))
                    updated_ca = st.number_input("Number of Major Vessels", min_value=0, max_value=3, step=1, value=int(patient_df.at[patient_index, 'Ca']))
                    updated_thal = st.text_input("Thalassemia", value=patient_df.at[patient_index, 'Thal'])

                    # Update the patient's details
                    if st.form_submit_button("Update Patient"):
                        patient_df.at[patient_index, 'Name'] = updated_name
                        patient_df.at[patient_index, 'Age'] = updated_age
                        patient_df.at[patient_index, 'Sex'] = updated_sex
                        patient_df.at[patient_index, 'ChestPain'] = updated_chest_pain
                        patient_df.at[patient_index, 'RestBP'] = updated_rest_bp
                        patient_df.at[patient_index, 'Chol'] = updated_chol
                        patient_df.at[patient_index, 'Fbs'] = updated_fbs
                        patient_df.at[patient_index, 'RestECG'] = updated_rest_ecg
                        patient_df.at[patient_index, 'MaxHR'] = updated_max_hr
                        patient_df.at[patient_index, 'ExAng'] = updated_ex_ang
                        patient_df.at[patient_index, 'Oldpeak'] = updated_oldpeak
                        patient_df.at[patient_index, 'Slope'] = updated_slope
                        patient_df.at[patient_index, 'Ca'] = updated_ca
                        patient_df.at[patient_index, 'Thal'] = updated_thal

                        # Save the updated data back to the file
                        patient_df.to_csv(patient_file_path, index=False)
                        st.success("Patient details updated successfully!")


        elif page == "Manage Doctors":
            st.header("Manage Doctors")
            st.write("Here you can manage doctor details.")

            # Add a button to view doctor data
            if st.button("View Doctor Data"):
                # Load the doctor data CSV
                try:
                    doctor_file_path = "dummy_doctor_data.csv"  # Ensure this path is correct
                    doctor_df = pd.read_csv(doctor_file_path)

                    # Display the doctor data in a table
                    st.markdown("### Doctors Records")
                    st.dataframe(doctor_df)
                except FileNotFoundError:
                    st.error("The file was not found. Please ensure it exists in the correct location.")

        # Manage Feedback Section
        elif page == "Manage Feedback":
            st.header("Manage Feedback")
            st.write("Here you can review feedback submitted by patients.")
            feedback_file_path = 'feedback_data.csv'

            try:
                feedback_df = pd.read_csv(feedback_file_path)

                # Display the feedback data
                st.markdown("### User Feedback")
                st.dataframe(feedback_df)

                # Add feedback manually
                st.markdown("### Add Feedback")
                with st.form("add_feedback"):
                    name = st.text_input("Name")
                    feedback = st.text_area("Feedback")
                    if st.form_submit_button("Add Feedback"):
                        new_feedback = pd.DataFrame({'Name': [name], 'Feedback': [feedback]})
                        feedback_df = pd.concat([feedback_df, new_feedback], ignore_index=True)
                        feedback_df.to_csv(feedback_file_path, index=False)
                        st.success("Feedback added successfully!")

                # Update feedback
                st.markdown("### Update Feedback")
                if feedback_df.empty:
                    st.warning("No feedback data available for update.")
                else:
                    if "update_feedback_index" not in st.session_state or st.session_state.update_feedback_index not in feedback_df.index:
                        st.session_state.update_feedback_index = feedback_df.index[0]  # Default to the first row

                    feedback_index = st.selectbox(
                        "Select Feedback to Update",
                        feedback_df.index,
                        format_func=lambda x: f"{feedback_df.at[x, 'Name']} - {feedback_df.at[x, 'Feedback']}",
                        key="update_feedback_index"
                    )

                    with st.form("update_feedback"):
                        updated_name = st.text_input("Name", value=feedback_df.at[feedback_index, 'Name'])
                        updated_feedback = st.text_area("Feedback", value=feedback_df.at[feedback_index, 'Feedback'])
                        if st.form_submit_button("Update Feedback"):
                            feedback_df.at[feedback_index, 'Name'] = updated_name
                            feedback_df.at[feedback_index, 'Feedback'] = updated_feedback
                            feedback_df.to_csv(feedback_file_path, index=False)
                            st.success("Feedback updated successfully!")

                # Delete feedback
                st.markdown("### Delete Feedback")

                if feedback_df.empty:
                    st.warning("No feedback data available for deletion.")
                else:
                    if "delete_feedback_index" not in st.session_state or st.session_state.delete_feedback_index not in feedback_df.index:
                        st.session_state.delete_feedback_index = feedback_df.index[0]  # Default to the first row

                    delete_feedback_index = st.selectbox(
                        "Select Feedback to Delete",
                        feedback_df.index,
                        format_func=lambda x: f"{feedback_df.at[x, 'Name']} - {feedback_df.at[x, 'Feedback']}",
                        key="delete_feedback_index"
                    )

                    if st.button("Delete Selected Feedback"):
                        feedback_df = feedback_df.drop(index=delete_feedback_index).reset_index(drop=True)
                        feedback_df.to_csv(feedback_file_path, index=False)
                        st.success("Feedback deleted successfully!")

            except FileNotFoundError:
                st.warning("No feedback data available.")