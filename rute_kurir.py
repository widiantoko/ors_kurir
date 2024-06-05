import folium.plugins
from folium.plugins import AntPath
import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import polyline
import pandas as pd





st.subheader("Simulasi Rute Delivery Kurir")

data_kurir=pd.read_excel('data/test.xlsx')

cito_lat='106.812288,-6.210011;'
cito_loc=(-6.210011, 106.812288)

data_kurir['jam']=data_kurir['Waktu Listing'].str[11:]


rute_kiriman= data_kurir.apply(lambda row: f"{row['Long_dest']},{row['Lat_dest']}", axis=1).tolist()
rute_kurir = ';'.join(rute_kiriman)

pin_kiriman=data_kurir.apply(lambda row: f"({row['Lat_dest']},{row['Long_dest']})", axis=1).tolist()
coords_tuples = [eval(coord) for coord in pin_kiriman]

konid=data_kurir.apply(lambda row: f"{row['No. Connote']}; {row['jam']}", axis=1).tolist()
st.text(konid)

konid_1=data_kurir['No. Connote'].tolist()
st.text(konid_1)



result = ''.join([cito_lat, rute_kurir])


url_A=f"""http://router.project-osrm.org/route/v1/motorcycle/{result}?overview=full"""

response_A = requests.get(url_A)
data_A = response_A.json()

lokasi_A=data_A['routes'][0]['geometry']

jarak_A=round(data_A['routes'][0]['distance']/1000,2)



koordinat_trip_A = polyline.decode(lokasi_A)


st.text(f"Estimasi Jarak Tempuh Kurir {jarak_A} Km")


mx = folium.Map(location=cito_loc, zoom_start=12)


text_Cito=f"""<p style='color:#3288bd; text-align:center; border-radius:3px; 
        font-size:12px; line-height:1px; padding-top:8px'>CitoXpress"""



text2=f"""<p style='color:#3288bd; text-align:center; border-radius:3px; 
        font-size:12px; line-height:3px; padding-top:8px'>{konid} km"""


#text3=f"""<p style='color:#3288bd; text-align:center; border-radius:3px;  
#        font-size:12px; line-height:3px; padding-top:8px'>{jarak2} km"""


folium.plugins.Fullscreen().add_to(mx)


AntPath(koordinat_trip_A, delay=600, weight=4, color='black', pulse_color='white', dash_array=[30,30]).add_to(mx)

#folium.PolyLine(
#locations=koordinat_trip_A,
#color='green',
#weight=3,
#opacity=0.9).add_to(mx)green

folium.Marker(location=cito_loc, tooltip= text_Cito, 
              icon = folium.Icon(color='red', icon_color='white',prefix='fa', icon='warehouse')).add_to(mx)



kiriman=data_kurir['No.Connote', 'Lat_dest', 'Long_dest','jam'].to_dict()
st.text(kiriman)

for loc in coords_tuples:
       folium.Marker(location=loc, icon = folium.Icon(color='green', icon_color='white', prefix='fa', icon='envelope', shadow_size=(0,0))).add_to(mx)

       
                


st_data=st_folium(mx, width=900)



