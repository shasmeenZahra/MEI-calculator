import streamlit as st  # Streamlit for web app GUI
import matplotlib.pyplot as plt  # For generating BMI category chart
from fpdf import FPDF  # For generating PDF reports

def calculate_bmi(weight, height):
    """Calculates BMI using weight (kg) and height (m)."""
    bmi = weight / (height ** 2)
    return round(bmi, 2)

def bmi_category(bmi):
    """Determines BMI category based on BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def generate_bmi_chart():
    """Generates and displays a bar chart representing BMI categories."""
    categories = ["Underweight", "Normal", "Overweight", "Obese"]
    bmi_values = [18.5, 24.9, 29.9, 35]
    plt.figure(figsize=(6,3))
    plt.bar(categories, bmi_values, color=["blue", "green", "orange", "red"])
    plt.xlabel("BMI Category")
    plt.ylabel("BMI Value")
    plt.title("BMI Categories")
    st.pyplot(plt)

def generate_pdf_report(weight, height, bmi, category):
    """Generates a downloadable PDF report containing BMI details."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "BMI Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, f"Weight: {weight} kg", ln=True)
    pdf.cell(200, 10, f"Height: {height} m", ln=True)
    pdf.cell(200, 10, f"BMI: {bmi}", ln=True)
    pdf.cell(200, 10, f"Category: {category}", ln=True)
    pdf.output("bmi_report.pdf")
    with open("bmi_report.pdf", "rb") as file:
        st.download_button(label="Download Report", data=file, file_name="BMI_Report.pdf", mime="application/pdf")

def main():
    """Main function to run the BMI Calculator web app."""
    st.title("BMI Calculator Web App")
    
    # Sidebar settings
    st.sidebar.title("Settings")
    dark_mode = st.sidebar.checkbox("Enable Dark Mode")  # Dark mode toggle
    st.sidebar.subheader("Unit Selection")
    unit = st.sidebar.radio("Select Unit", ["Metric (kg, m)", "Imperial (lbs, in)"])
    
    # User input fields for weight and height
    if unit == "Metric (kg, m)":
        weight = st.number_input("Enter your weight (kg)", min_value=1.0, step=0.1)
        height = st.number_input("Enter your height (m)", min_value=0.1, step=0.01)
    else:
        weight = st.number_input("Enter your weight (lbs)", min_value=1.0, step=0.1)
        height = st.number_input("Enter your height (in)", min_value=1.0, step=0.1)
        weight = weight * 0.453592  # Convert lbs to kg
        height = height * 0.0254  # Convert inches to meters
    
    # BMI Calculation and Result Display
    if st.button("Calculate BMI"):
        if weight > 0 and height > 0:
            bmi = calculate_bmi(weight, height)
            category = bmi_category(bmi)
            st.success(f"Your BMI is {bmi} ({category})")
            generate_bmi_chart()
            generate_pdf_report(weight, height, bmi, category)
        else:
            st.error("Please enter valid weight and height values.")
    
    # Footer section in sidebar
    st.sidebar.markdown("---")
    st.sidebar.text("Developed with ❤️ using Python & Streamlit")

if __name__ == "__main__":
    main()
