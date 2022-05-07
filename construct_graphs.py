import networkx as nx
import haversine as hs
import operator
import json
import time

from collections import deque

def isolated(G, i):
  for j in G[i]:
    if j != i:
      return False
  return True
  
def component(G, N, i):
  C = []
  S = []
  N.remove(i)
  S.append(i)
  while S:
    i = S.pop()
    C.append(i)
    for j in G[i]:
      if j in N:
        N.remove(j)
        S.append(j)
  return C

def components(G):
  C = []
  N = set(G.nodes())
  while N:
    C.append(component(G, N, next(iter(N))))
  return C
  
def distance(G, i):
  D = [-1] * len(G)
  Q = deque()
  D[i] = 0
  Q.append(i)
  while Q:
    i = Q.popleft()
    for j in G[i]:
      if D[j] == -1:
        D[j] = D[i] + 1
        Q.append(j)
  return [d for d in D if d > 0]

def info(G):
  print("{:>12s} | '{:s}'".format('Graph', G.name))

  n = G.number_of_nodes()
  n0, n1, delta = 0, 0, 0
  for i in G.nodes():
    if isolated(G, i):
      n0 += 1
    elif G.degree(i) == 1:
      n1 += 1
    if G.degree(i) > delta:
      delta = G.degree(i)
  
  print("{:>12s} | {:,d} ({:,d}, {:,d})".format('Nodes', n, n0, n1))
  
  m = G.number_of_edges()
  m0 = nx.number_of_selfloops(G)
  
  print("{:>12s} | {:,d} ({:,d})".format('Edges', m, m0))
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, delta))
  print("{:>12s} | {:.2e}".format('Density', 2 * m / n / (n - 1)))

  C = components(G)

  print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * max(len(c) for c in C) / n, len(C)))
  print()

def tops(G, centrality, label, n = 15):
  print("{:>12s} | '{:s}'".format('Centrality', label))
  
  tic = time.time()
  C = centrality(G)
  
  for p, (i, c) in enumerate(sorted(C.items(), key = operator.itemgetter(1), reverse = True)):
    if p < n:
      print("{:>12.6f} | '{:d}' ({:,d})".format(c, G.nodes[i]['label'], G.degree[i]))
      
  print("{:>12s} | {:.1f} s".format('Time', time.time() - tic))
  print()

def spatial_graph():
    """
    Function construts a spatial graph where
    each node represents a part of the city
    and each weighted edge represents the distance from part a to b.
    We will denote graph as Gs = (Ns, Es, ws)
    """
    G = nx.Graph(name = "Spatial graph")
    f = open("./nodes_data.json")
    data = json.load(f)

    # Let's walk through all parts of the city and use them as nodes in the graph
    # Then we calculate distances to all other parts of the city and add them
    # as weghts to edges: edge represents a distance between two parts of the city.
    # As the direction doesn't matter the constructed graph is undirected.
    for node in data:
      from_id = int(node['node_id'])
      from_x = node['geo_loc'][0]
      from_y = node['geo_loc'][1]
      G.add_node(from_id, label=from_id)

      # Now let's add all the edges: distances between different
      # parts of the city 
      for edge in data:
        to_id = int(edge['node_id'])
        to_x = edge['geo_loc'][0]
        to_y = edge['geo_loc'][1]
        
        # Calculating distance between two locations
        loc1=(from_x, from_y)
        loc2=(to_x, to_y)
        haversine_distance = hs.haversine(loc1,loc2)
        #print(haversine_distance)

        G.add_edge(from_id, to_id, weight=haversine_distance) 
    
    f.close()

    return G


def temporal_graph(time_interval):
    """
    Function construts a temporal graph where
    each node represents a part of the city
    and each weighted edge represents the average time of travel from part a to b.
    time_interval is a variable representing the slot in the day
    0 - morning rush
    1 - mid-day
    2 - afternoon-rush
    3 to 5 - night time
    We will denote graph as Gs = (Ns, Es, ws)
    """
    G = nx.DiGraph(name = "Temporal graph") # Directed graph
    print("Reading: edges_data_" + str(time_interval) + ".json")
    # Opening JSON file
    f = open("./edges_data_" + str(time_interval) + ".json")
            
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    print(type(data))

    #G.add_weighted_edges_from(data)
            
    # Closing file
    f.close()
    return G


if __name__ == "__main__":
    # Construct temporal graph
    G_temp = temporal_graph()
    info(G_temp)

    print("\n")

    #Construct spatial graph
    G_spat = spatial_graph()
    info(G_spat)
    
    tops(G_spat, nx.closeness_centrality, 'closeness')
    #tops(G, closeness_centrality, 'closeness')
    tops(G_spat, nx.betweenness_centrality, 'betweenness')
    

    tops(G_temp, nx.closeness_centrality, 'closeness')
    #tops(G, closeness_centrality, 'closeness')
    tops(G_temp, nx.betweenness_centrality, 'betweenness')
