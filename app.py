import numpy as np
import matplotlib.pyplot as plt
import joblib
import os
from flask import Flask, render_template, request
import webbrowser
from threading import Timer
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
        plt.figure(figsize=(size,size))
        plt.title("DS plot by Pulkit Mehta\n\n"+self.name)
        np.random.seed(seed)
        drawn=dict() 
        for key in graph.keys():
            x=np.random.randint(scale[0],scale[1])
            y=np.random.randint(scale[0],scale[1])
            plt.plot(x,y,'o')
            plt.text(x+d,y+d,  key)
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
                    plt.plot(x,y,'o')
                    plt.text(x+d,y+d,  val)
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
                    plt.plot([x1,x2],[y1,y2], alpha=alpha)
                else:
                    plt.arrow(x1,y1,-x1+x2,-y1+y2,length_includes_head=True, head_width=arr_size, alpha=alpha)
                    
                ## plotting weights
                wt=sorted(j.values())[0]
                mx=(x1+x2)/2
                my=(y1+y2)/2
                
                plt.plot(mx,my)
                plt.text(mx+d,my+d,wt)
                
                
        plt.xticks(())
        plt.yticks(())
        plt.xlabel("ORIENTATION= "+str(seed)+"  | "+
                   " SPACE: "+str(scale[1])+ 
                   "  |  SIZE: "+str(size)+
                   "  |  d= "+str(d))
        plt.savefig("grph.png", transparent=True, dpi=300)
        plt.close()






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

    direc=request.form.get('type')

    structure=request.form.get('structure')
    
    direc=request.form.get('type')
    direc=request.form.get('type')
    direc=request.form.get('type')
    direc=request.form.get('type')
    direc=request.form.get('type')

    img_name=request.form.get('images')
    path=os.path.join("input",img_name)
    print(path)
    pred=predictit(path)
    print(pred)
    images=os.listdir("input")
    return render_template('home.html',pname=pn ,imgs=images,covid_text=str(pred[2]) ,show_img=img_name, pneumonia_text=str(pred[1]),  normal_text=str(pred[0]))





if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run(debug=True)