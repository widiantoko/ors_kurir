import folium.plugins
from folium.plugins import AntPath
import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import polyline
import pandas as pd




st.subheader("Simulasi Rute Delivery Kurir")

#data_kurir=pd.read_excel('data/test.xlsx')

new=pd.read_excel('data/new.xlsx')






cito_lat='106.812288,-6.210011;'
cito_loc=(-6.210011, 106.812288)

#data_kurir['jam']=data_kurir['Waktu Listing'].str[11:]


#rute_kiriman= data_kurir.apply(lambda row: f"{row['Long_dest']},{row['Lat_dest']}", axis=1).tolist()
#rute_kurir = ';'.join(rute_kiriman)
#rute_new= new.apply(lambda row: f"{row['Long']},{row['Lat']}", axis=1).tolist()

urut_nama= new['Nama Kurir'].drop_duplicates(keep='last').sort_values(ascending=True)
urut_tgl=new['Tgl'].dt.strftime("%d-%b-%Y").sort_values(ascending=True).drop_duplicates(keep='last')

new['Tgl']=new['Tgl'].dt.strftime("%d-%b-%Y")

opt_kurir = st.selectbox("Nama Kurir:",urut_nama)
opt_tgl = st.selectbox("Tanggal Delivery:", urut_tgl)

def mask(opt_kurir, opt_tgl):
        try: 
                len((new['Nama Kurir']== opt_kurir) & (new['Tgl']==opt_tgl))
                return st.text(len((new['Nama Kurir']== opt_kurir) & (new['Tgl']==opt_tgl)))
                #if len((new['Nama Kurir']== opt_kurir) & (new['Tgl']==opt_tgl))>0:
                #        return  new[(new['Nama Kurir']== opt_kurir) & (new['Tgl']==opt_tgl)]
        except:
               exit

#mask = (new['Nama Kurir']== opt_kurir) & (new['Tgl']==opt_tgl)
new_data = new[mask]
        

#def pjg(opt_kurir, opt_tgl):
#    try:
#        len((new['Nama Kurir']== opt_kurir) & (new['Tgl']==opt_tgl))
#        if len((new['Nama Kurir']== opt_kurir) & (new['Tgl']==opt_tgl))>0:
#                return new[(new['Nama Kurir']== opt_kurir) & (new['Tgl']==opt_tgl)]
#    except:
#        None



st.dataframe(new_data)

new_data_loc=new_data.apply(lambda row: f"{row['Long']},{row['Lat']}", axis=1).tolist() 


new_data_kurir = ';'.join(new_data_loc) 

#st.text(rute_kiriman)
#st.text(new_data_kiriman)
#st.text(new_data_kurir)

#result = ''.join([cito_lat, rute_kurir])
result = ''.join([cito_lat, new_data_kurir])


st.text(result)
#st.text(new_data_kurir) = tdk perlu

url_A=f"""http://router.project-osrm.org/route/v1/motorcycle/{result}?overview=full"""

response_A = requests.get(url_A)
data_A = response_A.json()

lokasi_A=data_A['routes'][0]['geometry']
jarak_A=round(data_A['routes'][0]['distance']/1000,2)


koordinat_trip_A = polyline.decode(lokasi_A)



st.text(f"Estimasi Jarak Tempuh Kurir {jarak_A} Km")


mx = folium.Map(location=cito_loc, zoom_start=12)


text_Cito=f"""<p style='color:#3288bd; text-align:center; border-radius:3px; 
        font-size:12px; line-height:1px; padding-top:3px'>CitoXpress"""


#text2=f"""<p style='color:#3288bd; text-align:center; border-radius:3px; 
#        font-size:12px; line-height:3px; padding-top:8px'>{x}"""


#text3=f"""<p style='color:#3288bd; text-align:center; border-radius:3px;  
#        font-size:12px; line-height:3px; padding-top:8px'>{jarak2} km"""


folium.plugins.Fullscreen().add_to(mx)


AntPath(koordinat_trip_A, delay=600, weight=4, color='black', pulse_color='white', dash_array=[30,30]).add_to(mx)



folium.Marker(location=cito_loc, tooltip= text_Cito, 
              icon = folium.Icon(color='red', icon_color='white',prefix='fa', icon='warehouse')).add_to(mx)


#for loc in coords_tuples:
#        folium.Marker(location=loc, icon=folium.Icon(color='green', icon_color='white', prefix='fa', icon='envelope', shadow_size=(0,0))).add_to(mx)



#for index, row in new_data.iterrows():
#    folium.Marker(
#        location=[row['Lat'], row['Long']],
#        tooltip= 
#        f"""<p style='color:#3288bd; text-align:center; border-radius:1px; 
#        font-size:12px; line-height:1px; padding-top:3px'>{row['No. Connote']}""",
#
#        icon=folium.Icon(icon_color='white', prefix='fa',icon='envelope')).add_to(mx)

       
#for loc in pin_new:
#        folium.Marker(location=loc['koord'], tooltip=loc['jam'], icon = folium.Icon(color='green', icon_color='white', prefix='fa', icon='envelope', shadow_size=(0,0))).add_to(mx)



#st_data=st_folium(mx, width=900)



