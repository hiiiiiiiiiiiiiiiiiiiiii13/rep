# Edges of the resource allocation graph. 1.deadlock present   2.deadlock not present
#edges = [['0', 'r1'], ['1', 'r5'], ['1', 'r4'],['1','r3'], ['2', 'r5'],['3','r2'],['r1','1'],['r2','0'],['r3','4'],['r4','2'],['r5','3']]
#edges = [['0', 'r1'],['0', 'r2'], ['1', 'r3'],['3','r3'],['r1','1'],['r2','3'],['r3','2']]



#getting the graph input as nested list----------------------------------------
x=int(input ("enter the number of connections:"))
print('enter the pair of related devices: ')
u_vertex=[]
edges=[]
for i in range(0,x):

    
    u_vertex.append(input())
    u_vertex.append(input())
    edges.append(u_vertex)
    u_vertex = []

print(edges)
#-----------------------------------------------------------------------------







# Creating adjacency list inorder to get edges for graph.--------------------------------
adj_list = {} # adjacency list.
vertex_list = []   # list of vertices (original recognised devices)
def add_node(node):
    if node not in vertex_list:     # If node not present in vertex_list, then  we should append it.
        vertex_list.append(node)
    else:
        print("Device ",node," already exists!") #not adding duplicate vertices
        
        
def add_edge(node1, node2):
    temp = []
    if node1 in vertex_list and node2 in vertex_list:
        if node1 not in adj_list:
            temp.append(node2)
            adj_list[node1] = temp             # this will Create an adjacency list.
                                                # like {'0':['r1'],...}
        elif node1 in adj_list:
            temp.extend(adj_list[node1])
            temp.append(node2)
            adj_list[node1] = temp
       
    else:
        print("Device don't exist!")
#displays the vertex connection 
def graph():
    for node in sorted(adj_list.keys()):
        print(node, " ---> ", [i for i in adj_list[node]])

#adding the vertices ie) the process(u) and devices(v) needed )        
add_node('0')
add_node('1')
add_node('2')
add_node('3')
add_node('4')
add_node('r2')
add_node('r1')
add_node('r3')
add_node('r4')
add_node('r5')        

#print the adjacency_list        
for j in edges: #adding edges to the adjacency_list.
    add_edge(j[0], j[1])
    
 
#Printing the adjacency list
print()
print(f"Adjacency List: {adj_list}")
print()
graph()
#---------------------------------------------------------------------------------



# to store edges(process involved) for graph------------------------------------------
Edges=[]    
for i in adj_list:
    if(len(i)==1):    # process had length 1.
        list_of_devices = adj_list[i]
        for k in list_of_devices:
            j=adj_list[k][0]
            Edges.append((int(i),int(j)))     # ex1: 0 -> r1 and r1-> 1 so 0 -> 1
            
'''
    ex1: adj_list
    {'0': ['r1'],
     '1': ['r3', 'r4', 'r5'],
     '2': ['r5'], 
     '3': ['r2'], 
     'r1': ['1'],
     'r2': ['0'],
     'r3': ['4'],
     'r4': ['2'],
     'r5': ['3']}

ex2: adj_list5
 {'0': ['r1', 'r2'],
 '1': ['r3'],
 '3': ['r3'],
 'r1': ['1'],
 'r2': ['3'],
 'r3': ['2']} 
 '''           
#Edges
#ex1: [(0, 1), (1, 4), (1, 2), (1, 3), (2, 3), (3, 0)]
#ex2: [(0, 1), (0, 3), (1, 2), (3, 2)]
#-------------------------------------------------



#displaying graph of processes required for a function-------------------------
import networkx as nx
import matplotlib.pyplot as plt
G1 = nx.DiGraph()
G1.add_edges_from(Edges)
nx.draw_networkx(G1,node_size=500)
#---------------------------------------------------------------




#checking deadlock present or not-----------------------------------------------
#  this is a Stack to store the visited vertices in the Topological Sort algorithm.
s = []

# to store the vertices in Topological Order
tsort = []

# Adjacency list to store edges here max devices(5) (nested list)
adj = [[] for i in range(5)]                  #  ex1: [[1], [3, 2, 4], [3], [0],[]] = adj

# To ensure visited vertex
visited = [False for i in range(5)]         #initial state no vertices are visited so false-0

# Function to perform DFS (this is a recursive function)
def dfs(u):

    # Set the vertex as visited 1-true
    visited[u] = 1                            #ex1: Visisted=[1,1,1,1,1]                                 
    
    for j in adj[u]:                              #ex1:  [[1], [3, 2, 4], [3], [0],[]] = adj           

        # Visit connected vertices
        if (visited[j] == 0):       #if node is not visited move to next vertex             
            dfs(j)                              

    # Push into the stack(the vertices here are processes)

    s.append(u)                                #ex1:  s=[3,2,4,1,0]
  
#----------------------------------------------------



# Function to check and return ,if a cycle exists or not--------------------------------------------

def check_cycle():

    # Stores the positionition of vertex in topological order.
    position= dict()
    ind = 0
    
    # Pop all elements from stack
    while (len(s) != 0):           
        position[s[-1]] = ind           #ex1: position ={0:0,1:1,4:2,2:3,3:4}
                                                                            # s=[3,2,4,1,0]
        # Push element to get Topological Order.
        tsort.append(s[-1])          #ex1: tsort=[0,1,4,2,3]

        ind += 1

        # Pop from the stack
        s.pop()
    print(tsort)
    for i in range(n):        # Deadlock detection.
        for j in adj[i]:       # [[1], [3, 2, 4], [3], [0],[]] = adj
            first = 0 if i not in position else position[i]          # first  = 0,1,1,1,3,4
            second = 0 if j not in position else position[j]       # Second = 1,4,3,2,4,0

            # If parent vertex does not appear first (basic property to be topological).
            #topological sort only for DAG acyclic graph
            if (first > second):
                # Cycle does not exists
                return True

    # Return true if cycle exist
    return False

# Function to add edges
# from u to v
def addEdge(u, v):
    adj[u].append(v)    
#------------------------------------------------------------------
 


   
#main with output deadlock present or not --------------------------------------------------
if __name__ == "__main__":

    n = 5 #number of processes
    # Insert edges
    for edge in Edges:        # Edges = [(1, 3), (1, 2), (1, 4), (2, 3), (3, 0)]
        addEdge(edge[0],edge[1])
    for i in range(n):
        if (visited[i] == False):
            dfs(i)

# If cycle exist
    if (check_cycle()):
        print('OOPS INCORRECT CONNECTION!! Deadlock Present')
    else:
        print('GREAT CORRECT CONNECTION!! No Deadlock')
#------------------------------------------------------------------------
#Topological sort of directed graph is a linear ordering of its vertices such that, 
#for every directed edge U -> V from vertex U to vertex V, U comes before V in the ordering. 
