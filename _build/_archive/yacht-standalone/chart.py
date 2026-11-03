# Builds the stylised Dubai-coast chart SVG. Projection: x=(lon-55.08)*9060, y=(25.16-lat)*10000 (north up).
import math
def P(lat,lon): return ((lon-55.08)*9060,(25.16-lat)*10000)
def cr(pts, closed=False, t=0.5):
    """Catmull-Rom through points -> cubic bezier path data."""
    p=pts[:]; 
    if closed: p=[p[-1]]+p+[p[0],p[1]]
    else: p=[p[0]]+p+[p[-1]]
    d=f"M{p[1][0]:.0f},{p[1][1]:.0f}"
    for i in range(1,len(p)-2):
        p0,p1,p2,p3=p[i-1],p[i],p[i+1],p[i+2]
        c1=(p1[0]+(p2[0]-p0[0])*t/3,p1[1]+(p2[1]-p0[1])*t/3); c2=(p2[0]-(p3[0]-p1[0])*t/3,p2[1]-(p3[1]-p1[1])*t/3)
        d+=f" C{c1[0]:.0f},{c1[1]:.0f} {c2[0]:.0f},{c2[1]:.0f} {p2[0]:.0f},{p2[1]:.0f}"
    return d+(" Z" if closed else "")
coast=[(60,1080),(317,1000),(408,900),(462,840),(522,772),(580,700),(661,570),(735,495),(815,420),(900,322),(978,232),(1060,160),(1132,100),(1260,-20)]
land=cr(coast)+" L1300,-20 L1300,1100 L60,1100 Z"
def offset(pts,dist):
    out=[]
    for i,(x,y) in enumerate(pts):
        a=pts[max(i-1,0)]; b=pts[min(i+1,len(pts)-1)]
        dx,dy=b[0]-a[0],b[1]-a[1]; L=math.hypot(dx,dy); nx,ny=dy/L,-dx/L   # left normal = seaward
        out.append((x+nx*dist,y+ny*dist))
    return out
contours=[cr(offset(coast,d)) for d in (55,130,240,380)]
# Palm Jumeirah: trunk, fronds, crescent
base=(661,570); top=(497,420); C=(480,400); R=170
ux,uy=(top[0]-base[0]),(top[1]-base[1]); L=math.hypot(ux,uy); ux,uy=ux/L,uy/L; px,py=uy,-ux
fronds=[]
def ray(bx,by,dx,dy,rad):
    # distance along (dx,dy) from (bx,by) to the circle of radius rad around C
    fx,fy=bx-C[0],by-C[1]; bq=fx*dx+fy*dy; cq=fx*fx+fy*fy-rad*rad; disc=bq*bq-cq
    return -bq+math.sqrt(disc) if disc>0 else 0
for k in range(8):
    t=0.42+k*0.082; bx,by=base[0]+ux*L*t,base[1]+uy*L*t
    for s in (1,-1):
        dx,dy=px*s+ux*0.28,py*s+uy*0.28; m=math.hypot(dx,dy); dx,dy=dx/m,dy/m
        ln=max(14,min(118,ray(bx,by,dx,dy,R-34)))
        fronds.append(f"M{bx:.0f},{by:.0f} L{bx+dx*ln:.0f},{by+dy*ln:.0f}")
a1,a2=math.radians(103),math.radians(-17)
c1=(C[0]+R*math.cos(a1),C[1]+R*math.sin(a1)); c2=(C[0]+R*math.cos(a2),C[1]+R*math.sin(a2))
crescent=f"M{c1[0]:.0f},{c1[1]:.0f} A{R},{R} 0 1 1 {c2[0]:.0f},{c2[1]:.0f}"
# routes (sea only), drawn as loops so the return leg is visible
D=(522,772)
loop1=[D,(455,756),(385,744),(318,776),(338,834),(430,826),D]
out_south=[D,(476,806),(410,842),(330,832),(296,770),(272,670),(262,540),(272,410),(296,316),(318,262)]
back_west=[(318,262),(258,300),(222,430),(230,590),(300,704),(410,740),D]
north=[(318,262),(400,204),(560,186),(700,226),(820,214),(925,160),(976,146),(1004,196)]
north_back=[(1004,196),(936,236),(840,250),(700,286),(560,232),(420,226),(300,292),(232,430)]
r1=cr(loop1)
r2=cr(out_south+back_west[1:])
r3=cr(out_south+north[1:]+north_back[1:]+back_west[3:])
r4=r3
pins={'marina':D,'ain':(372,800),'atlantis':P(25.1305,55.1175),'burj':P(25.1412,55.1853),'anchor':(840,246)}
import json
json.dump(dict(land=land,contours=contours,fronds=fronds,crescent=crescent,trunk=f"M{base[0]},{base[1]} L{top[0]},{top[1]}",r1=r1,r2=r2,r3=r3,r4=r4,pins=pins),open(__file__.replace('.py','.json'),'w'),indent=1)
print(pins)
