import numpy as np
import matplotlib.pyplot as dsvis
import joblib
import os
import sys
from flask import Flask, render_template, request, url_for
import webbrowser
from threading import Timer
from time import time
class Graph:
    
    def __init__(self, title="Graph"):
        self.graph=dict()
        self.name=title
        
    def addEdge(self,u,v,w):
        if u not in self.graph:
            self.graph[u]=[{v:w}]
        else:
            self.graph[u].append({v:w})
        
        

            
    def graphViz(self, seed=0, scale=(1,10), size=5,d=0.1,arr_size=0.01, direc=0, alpha=0.6):
        graph=self.graph
        dsvis.figure(figsize=(size,size))
        dsvis.box(on=None)
        dsvis.title("DSvis Plot\n\n"+self.name)
        np.random.seed(seed)
        drawn=dict() 
        for key in graph.keys():
            x=np.random.randint(scale[0],scale[1])
            y=np.random.randint(scale[0],scale[1])
            dsvis.plot(x,y,'o')
            dsvis.text(x+d,y+d,  key)
            if key not in drawn.keys():
                drawn[key]=[x,y]
            else:
                pass

        for key in graph.keys():
            for j in graph[key]:
                val=sorted(j.keys())[0]
                if val not in drawn.keys():
                    x=np.random.randint(scale[0],scale[1])
                    y=np.random.randint(scale[0],scale[1])
                    dsvis.plot(x,y,'o')
                    dsvis.text(x+d,y+d,  val)
                    drawn[val]=[x,y]
                else:
                    pass
                
        for key in graph.keys():
            v1=key
            x1=drawn[v1][0]
            y1=drawn[v1][1]
            for j in graph[v1]:
                v2=sorted(j.keys())[0]
                x2=drawn[v2][0]
                y2=drawn[v2][1]
                
                
                if direc==0:
                    dsvis.plot([x1,x2],[y1,y2], alpha=alpha)
                else:
                    dsvis.arrow(x1,y1,-x1+x2,-y1+y2,length_includes_head=True, head_width=arr_size, alpha=alpha)
                    
                ## plotting weights
                wt=sorted(j.values())[0]
                mx=(x1+x2)/2
                my=(y1+y2)/2
                
                dsvis.plot(mx,my)
                dsvis.text(mx+d,my+d,wt)
                
                
        dsvis.xticks(())
        dsvis.yticks(())
        dsvis.xlabel("ORIENTATION= "+str(seed)+"  | "+
                   " SPACE: "+str(scale[1])+ 
                   "  |  SIZE: "+str(size)+
                   "  |  d= "+str(d)+
                   "  |  ALPHA="+str(alpha))



        fname=str(time())+".png"
        imgpath=os.path.join("static",fname)

        try:
            os.remove(os.path.join("static","*.png"))
        except:
            pass
        dsvis.savefig(imgpath, transparent=True, dpi=300)
        dsvis.close()

        return fname






app = Flask(__name__)

@app.route('/')
@app.route('/home')

def home():
    graphs=os.listdir("saved_graphs")
    return render_template('home.html',files=graphs)
def open_browser():
  webbrowser.open_new('http://127.0.0.1:5000/')


@app.route('/generate', methods=['POST'])
def gen():
    gn=request.form.get('title')

    direc=int(request.form.get('type'))

    structure=request.form.get('structure')
    
    file_name=request.form.get('fileselect')

    to_save=request.form.get('to_save')



    if structure!="":
        g=Graph(gn)
        print("Created empty graph",g.name)
        edge=[]
        for ch in structure:
            if ch=="(":
                edge=[]
                v=str()
            elif ch==',':
                if v!="":
                    edge.append(v)
                v=str()
                
            elif ch==')':
                edge.append(v)
                print("Added Edge: ",edge)
                g.addEdge(edge[0],edge[1],edge[2])
                v=str()
            else:
                v=v+ch




        if to_save=="1":
            joblib.dump(g,os.path.join("saved_graphs",gn+".dsvisGraph"))








    else:
        path=os.path.join("saved_graphs",file_name) 
        print(path)
        g=joblib.load(path)

    
    try:
        seed=int(request.form.get('seed'))
    except:
        seed=0
    try:
        space=int(request.form.get('space'))
    except:
        space=10

    try:
        size=int(request.form.get('size'))
    except:
        size=5

    try:
        d=float(request.form.get('d'))
    except:
        d=0.1

    try:
        arr_size=float(request.form.get('arrowhead'))
    except:
        arr_size=0.01

    try:
        alpha=float(request.form.get('alpha'))
    except:
        alpha=0.6

    try:
        fname=g.graphViz(seed=seed,
         scale=(1,space), size=size,d=d,
            arr_size=arr_size, direc=direc, alpha=alpha)
        shout=str(time())+" |Shout: No errors!"
    except:
        shout=str(time())+" |Shout Check your values!"
    

    memory=sys.getsizeof(g)
    _id=id(g)
    graphs=os.listdir("saved_graphs")

    return render_template('home.html',files=graphs,
     img=url_for('static',filename=fname),g=g.graph,
     shout=shout,memory=memory,id=hex(_id))





if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run(debug=True)