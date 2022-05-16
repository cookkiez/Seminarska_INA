import networkx as nx
import construct_graphs

if __name__ == "__main__":

    # Construct spatial graph
    G_spat = construct_graphs.spatial_graph()
    construct_graphs.info(G_spat)

    print("\n")

    # Construct temporal graph for each time slot in the day
    # This means 4 different temporal directed graphs
    G_temp_morning = construct_graphs.temporal_graph(0)
    construct_graphs.info(G_temp_morning)

    print("\n")

    G_temp_mid = construct_graphs.temporal_graph(1)
    construct_graphs.info(G_temp_mid)

    print("\n")

    G_temp_afternoon = construct_graphs.temporal_graph(2)
    construct_graphs.info(G_temp_afternoon)

    print("\n")

    G_temp_night = construct_graphs.temporal_graph(3)
    construct_graphs.info(G_temp_night)

    print("\n")

    # Closeness centrality    
    print("Closeness centrality for spatial graph")
    construct_graphs.tops(G_spat, nx.closeness_centrality, 'closeness')

    print("Closeness centrality for temporal graph - morning")
    construct_graphs.tops(G_temp_morning, nx.closeness_centrality, 'closeness')

    print("Closeness centrality for temporal graph - mid")
    construct_graphs.tops(G_temp_mid, nx.closeness_centrality, 'closeness')

    print("Closeness centrality for temporal graph - afternoon")
    construct_graphs.tops(G_temp_afternoon, nx.closeness_centrality, 'closeness')

    print("Closeness centrality for temporal graph - night")
    construct_graphs.tops(G_temp_night, nx.closeness_centrality, 'closeness')


    # Betweenness centrality
    print("Betweenness centrality for spatial graph")
    construct_graphs.tops(G_spat, nx.betweenness_centrality, 'betweenness')

    print("Betweenness centrality for temporal graph - morning")
    construct_graphs.tops(G_temp_morning, nx.betweenness_centrality, 'betweenness')

    print("Betweenness centrality for temporal graph - mid")
    construct_graphs.tops(G_temp_mid, nx.betweenness_centrality, 'betweenness')

    print("Betweenness centrality for temporal graph - afternoon")
    construct_graphs.tops(G_temp_afternoon, nx.betweenness_centrality, 'betweenness')

    print("Betweenness centrality for temporal graph - night")
    construct_graphs.tops(G_temp_night, nx.betweenness_centrality, 'betweenness')

    # PageRank
    print("Pagerank for spatial graph")
    construct_graphs.tops(G_spat, nx.pagerank, 'pagerank')

    print("Pagerank for temporal graph - morning")
    construct_graphs.tops(G_temp_morning, nx.pagerank, 'pagerank')

    print("Pagerank for temporal graph - mid")
    construct_graphs.tops(G_temp_mid, nx.pagerank, 'pagerank')

    print("Pagerank for temporal graph - afternoon")
    construct_graphs.tops(G_temp_afternoon, nx.pagerank, 'pagerank')

    print("Pagerank for temporal graph - night")
    construct_graphs.tops(G_temp_night, nx.pagerank, 'pagerank')

    # HITS
    # print("Pagerank for spatial graph")
    # construct_graphs.tops(G_spat, nx.pagerank, 'pagerank')

    # print("Pagerank for temporal graph - morning")
    # construct_graphs.tops(G_temp_morning, nx.pagerank, 'pagerank')

    # print("Pagerank for temporal graph - mid")
    # construct_graphs.tops(G_temp_mid, nx.pagerank, 'pagerank')

    # print("Pagerank for temporal graph - afternoon")
    # construct_graphs.tops(G_temp_afternoon, nx.pagerank, 'pagerank')

    # print("Pagerank for temporal graph - night")
    # construct_graphs.tops(G_temp_night, nx.pagerank, 'pagerank')
