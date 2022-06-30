



class graph:
    
    """Graph ADT"""    
    def __init__(self):
        self.graph={}
        self.visited={}
            
    def append(self,vertexid,edge,weight):        
        """add/update new vertex,edge,weight"""        
        if vertexid not in self.graph.keys():      
            self.graph[vertexid]={}
            self.visited[vertexid]=0
        if edge not in self.graph.keys():      
            self.graph[edge]={}
            self.visited[edge]=0
        self.graph[vertexid][edge]=weight
        
    def reveal(self):
        """return adjacent list"""
        return self.graph
    
    def vertex(self):
        """return all vertices in the graph"""
        return list(self.graph.keys())
    
    def edge(self,vertexid):
        """return edge of a particular vertex"""
        return list(self.graph[vertexid].keys())
    
    def edge_reverse(self,vertexid):
        """return vertices directing to a particular vertex"""                
        return [i for i in self.graph if vertexid in self.graph[i]]
    
    def weight(self,vertexid,edge):
        """return weight of a particular vertex"""
        return (self.graph[vertexid][edge])
    
    def order(self):
        """return number of vertices"""
        return len(self.graph)
    
    def visit(self,vertexid):
        """visit a particular vertex"""
        self.visited[vertexid]=1
        
    def go(self,vertexid):
        """return the status of a particular vertex"""
        return self.visited[vertexid]
    
    def route(self):
        """return which vertices have been visited"""
        return self.visited
    
    def degree(self,vertexid):
        """return degree of a particular vertex"""
        return len(self.graph[vertexid])
    
    def mat(self):
        """return adjacent matrix"""        
        self.matrix=[[0 for _ in range(max(self.graph.keys())+1)] for i in range(max(self.graph.keys())+1)]        
        for i in self.graph:    
            for j in self.graph[i].keys():    
                self.matrix[i][j]=1        
        return self.matrix
    
    def remove(self,vertexid):  
        """remove a particular vertex and its underlying edges"""
        for i in list(self.graph[vertexid].keys()):
            self.graph[i].pop(vertexid)
        self.graph.pop(vertexid)
        
    def disconnect(self,vertexid,edge):
        """remove a particular edge"""
        del self.graph[vertexid][edge]
    
    def clear(self,vertexid=None,whole=False):
        """unvisit a particular vertex"""
        if whole:
            self.visited=dict(zip(self.graph.keys(),[0 for i in range(len(self.graph))]))
        elif vertexid:
            self.visited[vertexid]=0
        else:
            assert False,"arguments must satisfy whole=True or vertexid=int number"
                    

        
def sort_by_degree(ADT):
    """sort vertices by degree"""  
    dic={}
    for i in ADT.vertex():
        dic[i]=ADT.degree(i)
    
    #the dictionary is sorted by value and exported as a list in descending order
    output=[i[0] for i in sorted(dic.items(), key=lambda x:x[1])]
    
    return output[::-1]

def prune_graph(ADT):
    """ remove all vertics that have a degree of n-1; n is the number of nodes """
    for i in ADT.vertex():
        if ADT.degree(i)== len(ADT.graph):
            ADT.remove(i)
    for i in ADT.vertex():
        if ADT.degree(i) > 1:
            ADT.disconnect(i,i)
            
    return ADT


def serialize_graph(ADT,path):
    nodes_dict=dict()
    with open(path, "w", encoding="utf-8") as output:
        for i in ADT.vertex():
            for edge in ADT.edge(i):
                if edge+i not in nodes_dict:
                    nodes_dict[i+edge]=""
                    output.write(i+"	pp	"+edge+"\r\n")
    
