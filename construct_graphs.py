import networkx as nx
import haversine as hs
import json

def isolated(G, i):
  for j in G[i]:
    if j != i:
      return False
  return True

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
      G.add_node(from_id)

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


def temporal_graph():
    """
    Function construts a temporal graph where
    each node represents a part of the city
    and each weighted edge represents the average time of travel from part a to b.
    We will denote graph as Gs = (Ns, Es, ws)
    """
    G = nx.DiGraph(name = "Temporal graph") # Directed graph
    for number in range(6):
        print("Reading: edges_data_" + str(number) + ".json")
        # Opening JSON file
        f = open("./edges_data_" + str(number) + ".json")
            
        # returns JSON object as
        # a dictionary
        data = json.load(f)
        #print(type(data))

        G.add_weighted_edges_from(data)
            
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
    
