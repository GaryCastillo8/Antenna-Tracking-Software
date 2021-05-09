from skyfield.api import load
from skyfield.api import wgs84
from skyfield.api import EarthSatellite
import math
import numpy as np

Tscale=load.timescale()
TLE1="1 45598U 98067RL  21128.37885972  .00010203  00000-0  13794-3 0  9997"
TLE2="2 45598  51.6395 168.8093 0000238 243.3217 116.7751 15.58386339 58307"
CubeSatQ=EarthSatellite(TLE1,TLE2,"Quetzal-1",Tscale)

CScul=wgs84.latlon(+14.0872,-87.1594)
inicial_time=Tscale.utc(2021,5,8)
final_time=Tscale.utc(2021,5,9)
time, culminate=CubeSatQ.find_events(CScul,inicial_time, final_time, altitude_degrees=15)

for i , culminate2 in zip(time, culminate):
    lista=("Orto Local","Culminacion Local","Ocaso Local")[culminate2]
    print(i.utc_strftime("%Y %b %d %H:%M:%S"),lista)
print(" ")

time2=Tscale.now()
position1=CubeSatQ.at(time2)
print(position1.position.km)

X=float(position1.position.km[0])
Y=float(position1.position.km[1])
Z=float(position1.position.km[2])
print(" ")

AlturaCS=math.sqrt((X)**2+(Y)**2+(Z)**2)
print(AlturaCS, "km")

subpoint=wgs84.subpoint(position1)
print("Elevacion:",int(subpoint.elevation.km), "km")
print(" ")

GS=CubeSatQ-CScul
observador=GS.at(time2)
print(GS)
print(" ")

altitud, azimuth, elevacion= observador.altaz()
print(" ")

topocentric = GS.at(time2)
print(topocentric.position.km)
X2=float(topocentric.position.km[0])
Y2=float(topocentric.position.km[1])
Z2=float(topocentric.position.km[2])
AlturaTpc=math.sqrt((X2)**2+(Y2)**2)
print("Radio topocéntrico ", AlturaTpc)
print(" ")

def altzim(altitud, azimuth):

#print(altitud)
    #print(azimuth)
    #print(int(elevacion.km))
    a=str(altitud)
    fracc=a.split(" ")
    gfracc=fracc[0].split("deg")
    mfracc=fracc[1].split("'")
    minfracc=fracc[2].split('"')
    grados=float(gfracc[0])
    arcmin=float(mfracc[0])
    arcseg=float(minfracc[0])   
    b=str(azimuth)
    fracc2=b.split(" ")
    gfracc2=fracc2[0].split("deg")
    mfracc2=fracc2[1].split("'")
    minfracc2=fracc2[2].split('"')
    grados2=float(gfracc2[0])
    arcmin2=float(mfracc2[0])
    arcseg2=float(minfracc2[0])
    
    dfracc=grados+arcmin/60+arcseg/3600
    dfracc2=grados2+arcmin2/60+arcseg2/3600
    
    return dfracc, dfracc2
    
vec1=np.array(altzim(altitud, azimuth))
print("This is the Altitude and Azimuth with respect to Tegucigalpa: ", vec1)
