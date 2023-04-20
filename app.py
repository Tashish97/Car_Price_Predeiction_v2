import streamlit as st
import pickle

# loadng models
##########################################################################################################################
file = open("model.pkl","rb")
model = pickle.load(file)
file.close()


file = open("le.pkl","rb")
le = pickle.load(file)
file.close()

##########################################################################################################################

st.title("CAR SELLING PRICE PREDICTION")

brand_list = ["Ambassador", "Audi", "BMW", "Chevrolet", "Daewoo", "Datsun", "Fiat", "Force", "Ford", "Honda", "Hyundai",
              "Isuzu", "Jaguar", "Jeep", "Kia", "Land Rover", "MG", "Mahindra", "Maruti Suzuki", "Mercedes Benz", 
              "Mitsubishi", "Nissan", "OpelCorsa", "Renault", "Skoda", "Tata", "Toyota", "Volkswagen", "Volvo"]

brand = st.selectbox("Select Brand", brand_list)

year = st.number_input("Build Year", value=2020, min_value=1950, max_value=2022)

driven = st.number_input("Driven Distance (in km)", min_value=0)

fuel_type = st.selectbox("Fuel Type", ("Diesel", "Petrol", "CNG"))

seller_type = st.selectbox("Seller Type", ("Individual", "Dealer"))

transmission_type = st.selectbox("Transmission Type", ("Manual", "Automatic"))

owner = st.number_input("Number of Owners", value=1, min_value=1, max_value=4)

if st.button("Predict Selling Price"):
    
    le_brand = le.transform([brand])[0]

    if fuel_type == "Petrol":
        fuel_Diesel=0
        fuel_Petrol=1
    elif fuel_type == "Diesel":
        fuel_Diesel=1
        fuel_Petrol=0
    else:
        fuel_Diesel=0
        fuel_Petrol=0


    if seller_type == "Dealer":
        seller_type_Individual=0
    else:
        seller_type_Individual=1


    if transmission_type == "Manual":
        transmission_Manual = 1
    else:
        transmission_Manual = 0


    if owner == 1:
        o2 = 0
        o3 = 0 
        o4 = 0
    elif owner == 2:
        o2 = 1
        o3 = 0 
        o4 = 0
    elif owner == 3:
        o2 = 0
        o3 = 1
        o4 = 0
    else:
        o2 = 0
        o3 = 0
        o4 = 1
        
    old = 2020 - year
    text = model.predict([[le_brand, year, driven, fuel_Diesel, fuel_Petrol, seller_type_Individual,transmission_Manual, o2, o3, o4, old]])
    text = round(text[0], 2)
    
    st.success(f"Predicted Selling Price is Rs. {text}/-")

