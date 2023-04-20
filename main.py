import pickle
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import uvicorn

# loadng models
##########################################################################################################################
file = open("model.pkl","rb")
model = pickle.load(file)
file.close()


file = open("le.pkl","rb")
le = pickle.load(file)
file.close()

##########################################################################################################################
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_form(request: Request):
    return templates.TemplateResponse("tb.html", {"request": request})

@app.post("/")
def predict(request: Request, Year: int = Form(...), Driven: float = Form(...), 
            brand: str = Form(...), Fuel_Type: str = Form(...), Seller_Type_Individual: str = Form(...),
            Transmission_Mannual: str = Form(...), Owner: int = Form(...)):
    
    le_brand = le.transform([brand])[0]
    
    if Fuel_Type == "Petrol":
        fuel_Diesel=0
        fuel_Petrol=1
    elif Fuel_Type == "Diesel":
        fuel_Diesel=1
        fuel_Petrol=0
    else:
        fuel_Diesel=0
        fuel_Petrol=0
        
    if Seller_Type_Individual == "Dealer":
        seller_type_Individual=0
    else:
        seller_type_Individual=1
        
    
    if Transmission_Mannual == "Mannual":
        transmission_Manual = 1
    else:
        transmission_Manual = 0
        
    
    if Owner == 1:
        o2 = 0
        o3 = 0 
        o4 = 0
    elif Owner == 2:
        o2 = 1
        o3 = 0 
        o4 = 0
    elif Owner == 3:
        o2 = 0
        o3 = 1
        o4 = 0
    else:
        o2 = 0
        o3 = 0
        o4 = 1
    old = 2020-Year
    text = model.predict([[le_brand,Year,Driven,fuel_Diesel,fuel_Petrol,seller_type_Individual,transmission_Manual,o2,o3,o4,old]])
    text = round(text[0],2)
    return templates.TemplateResponse("tb.html", {"request": request, "result": text})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
