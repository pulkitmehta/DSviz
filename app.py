import numpy as np
import matplotlib.pyplot as plt
import joblib

class Graph:
    
    def __init__(self):
        self.graph=dict()
        
        
    def addEdge(self,u,v):
        if u not in self.graph:
            self.graph[u]=[v]
        else:
            self.graph[u].append(v)
        
        

            
    def graphViz(self, seed, scale=(1,10), size=(5,5), title="Graph Visualisation",d=0.1):
        graph=self.graph
        plt.figure(figsize=size)
        plt.title(title)
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
            for val in graph[key]:
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
            for v2 in graph[v1]:
                x2=drawn[v2][0]
                y2=drawn[v2][1]

                plt.plot([x1,x2],[y1,y2])
        plt.xticks(())
        plt.yticks(())
        plt.xlabel("SEED= "+str(seed)+"  | "+
                   " SCALE: ("+str(scale[0])+','+str(scale[1])+")"+ 
                   "  |  SIZE: ("+str(size[0])+','+str(size[1])+")"+
                   "  |  d= "+str(d))
        plt.show()
