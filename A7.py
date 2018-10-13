import networkx as nx
import pandas as pd

class MyGraph(nx.DiGraph):
    print("WELCOME TO MAGIC KINGDOM")
    __graphattr = pd.read_csv('disneyattribute.csv')
    for k in range(len(__graphattr['Number'])):
        print(__graphattr['Number'][k], __graphattr['Attraction'][k])
    __graphInfo = pd.read_csv('disneyfinaldataset.csv')
    __graphRev_dir = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E', 'NW': 'SE', 'SW': 'NE'}

    def __init__(self):

        nx.DiGraph.__init__(self)       # the main graph for normal people

        for i in range(len(self.__graphInfo['from_node'])):

            if self.__graphInfo['bi_dir_indicator'][i] == 1:

                if self.__graphInfo['bi_dir_indicator'][i] == 1:
                    self.add_edge(self.__graphInfo['from_node'][i], self.__graphInfo['to_node'][i],
                                  weight=self.__graphInfo['distance'][i], path=self.__graphInfo['path'][i],
                                  direction=self.__graphInfo['direction'][i])
                    self.add_edge(self.__graphInfo['to_node'][i], self.__graphInfo['from_node'][i],
                                  weight=self.__graphInfo['distance'][i], path=self.__graphInfo['path'][i],
                                  direction=self.__graphRev_dir[self.__graphInfo['direction'][i]])

            else:

                self.add_edge(self.__graphInfo['from_node'][i], self.__graphInfo['to_node'][i],
                              weight=self.__graphInfo['distance'][i], path=self.__graphInfo['path'][i],
                              direction=self.__graphInfo['direction'][i])

    def sub_graph(self, nodes):
        '''
        A function that create a subgraph for handicap accessible paths
        :param nodes: the nodes from the main graph
        :return: return the subgraph

        '''
        sub=self.subgraph(nodes).copy()
        for j in range(len(self.__graphInfo['from_node'])):
            if self.__graphInfo['handicap_indicator'][j] == 1:   # 1 means this road has upstairs
                if self.__graphInfo['bi_dir_indicator'][j] == 1:
                    sub.remove_edge(self.__graphInfo['from_node'][j], self.__graphInfo['to_node'][j])
                    sub.remove_edge(self.__graphInfo['to_node'][j], self.__graphInfo['from_node'][j])
                else:
                    sub.remove_edge(self.__graphInfo['from_node'][j], self.__graphInfo['to_node'][j])

        return sub

    def num_to_attra(self, startnum, endnum):
        '''
        A function that transfer the number of attractions to the name of attractions
        :param startnum: the number of the start attraction
        :param endnum:  the number of the end attraction
        :return: return the name of attractions

        '''
        startnode = ''
        endnode = ''
        for j in range(len(self.__graphattr['Attraction'])):
            if self.__graphattr['Number'][j] == startnum:
                startnode = self.__graphattr['Attraction'][j]
            if self.__graphattr['Number'][j] == endnum:
                endnode = self.__graphattr['Attraction'][j]
        return startnode, endnode

    def out_attra_info(self, endnode):
        '''
        A funtion that output the minimun height and other information for the end attraction
        :param endnode: the end attraction
        :return: return the details about the end attraction
        '''
        for k in range(len(self.__graphattr['Attraction'])):
            if self.__graphattr['Attraction'][k] == endnode:
                print("\nNotice: %s facility has the following information: "
                      "min height %d cm, min weight %d pounds, handicap(%s), children(%s)"
                      % (self.__graphattr['Attraction'][k], self.__graphattr['min_height(cm)'][k],
                         self.__graphattr['min_weight(pounds)'][k], self.__graphattr['handicap_allowed'][k],
                         self.__graphattr['children_allowed'][k]))


    def output_best_route(self, start, end, user):
        '''
        A function for generating and outputting the best route
        :param paths: the paths for walking
        :return: return the best route
        '''
        current_road = ""
        current_mile = 0.0
        current_dir = ""
        combined_results = []
        self.out_attra_info(end)
        print("\nThe best route from " + start + " to " + end + " is:\n")

        if user == "no":
            routenodes = nx.dijkstra_path(self, start, end)
        else:
            routenodes = nx.dijkstra_path(self.sub_graph(self.nodes), start, end)
        for x in range(len(routenodes) - 1):
            start_node = routenodes[x]
            end_node = routenodes[x + 1]
            if user == "no":
                paths = [self.get_edge_data(start_node, end_node)['path'],
                         self.get_edge_data(start_node, end_node)['weight'],
                         self.get_edge_data(start_node, end_node)['direction']]
            else:
                paths = [self.sub_graph(self.nodes).get_edge_data(start_node, end_node)['path'],
                         self.sub_graph(self.nodes).get_edge_data(start_node, end_node)['weight'],
                         self.sub_graph(self.nodes).get_edge_data(start_node, end_node)['direction']]

            if ((current_road == "" or current_road == paths[0]) and (x != len(routenodes) - 1)):
                current_road = paths[0]
                current_dir = paths[2]
                current_mile += paths[1]

            else:
                combined_results.append(
                    "Go %s road for %f mile with direction %s" % (current_road, current_mile, current_dir))
                current_road = paths[0]
                current_dir = paths[2]
                current_mile = paths[1]
                if x == len(routenodes) - 2:
                    combined_results.append(
                "Go %s road for %f mile with direction %s" % (current_road, current_mile, current_dir))
                else:
                    continue

        for print_result in combined_results:
            print(print_result)

def main():
    """

    :return:
    >>> G = MyGraph()
    >>> G.num_to_attra(1,5)
    ('astroorbiter', 'dumboflyingelephant')
    >>> G.out_attra_info('dumboflyingelephant')
    <BLANKLINE>
    Notice: dumboflyingelephant facility has the following information: min height 150 cm, min weight 130 pounds, handicap(Y), children(Y)

    #unidirectional test for dumbofyingelephant since railstation1 road is only for entry
    >>> G.output_best_route('astroorbiter', 'dumboflyingelephant', 'no')
    <BLANKLINE>
    Notice: dumboflyingelephant facility has the following information: min height 150 cm, min weight 130 pounds, handicap(Y), children(Y)
    <BLANKLINE>
    The best route from astroorbiter to dumboflyingelephant is:
    <BLANKLINE>
    Go adventure4 road for 0.300000 mile with direction N
    Go adventurelane road for 1.500000 mile with direction E
    Go fantasy road for 1.350000 mile with direction N
    Go railstation road for 0.200000 mile with direction E
    Go railstation1 road for 0.100000 mile with direction S

    #unidirectional test for dumboflyingelephant exit
    >>> G.output_best_route('dumboflyingelephant', 'waltdisneyworld', 'no')
    <BLANKLINE>
    Notice: waltdisneyworld facility has the following information: min height 150 cm, min weight 130 pounds, handicap(Y), children(Y)
    <BLANKLINE>
    The best route from dumboflyingelephant to waltdisneyworld is:
    <BLANKLINE>
    Go railstation5 road for 0.100000 mile with direction N
    Go railstation road for 0.150000 mile with direction E
    Go caseyjr road for 0.400000 mile with direction E
    Go caseyjr1 road for 0.100000 mile with direction N

    >>> G.output_best_route('barnstormer', 'villagehaus', 'no')
    <BLANKLINE>
    Notice: villagehaus facility has the following information: min height 150 cm, min weight 130 pounds, handicap(Y), children(Y)
    <BLANKLINE>
    The best route from barnstormer to villagehaus is:
    <BLANKLINE>
    Go caseyjr3 road for 0.100000 mile with direction N
    Go railstation road for 0.550000 mile with direction W
    Go phantom road for 0.600000 mile with direction NW
    Go fairytale road for 2.850000 mile with direction W
    Go magicworld road for 3.100000 mile with direction SW
    Go mw1 road for 0.200000 mile with direction W
    Go mw2 road for 0.300000 mile with direction W

    #doctest in case an attraction has a path in which non-handicapped path is available and user has entered no for handicap path
    >>> G.output_best_route('boattour', 'hauntedhouse', 'no')
    <BLANKLINE>
    Notice: hauntedhouse facility has the following information: min height 150 cm, min weight 130 pounds, handicap(Y), children(Y)
    <BLANKLINE>
    The best route from boattour to hauntedhouse is:
    <BLANKLINE>
    Go mw4 road for 0.300000 mile with direction E
    Go mw3 road for 0.010000 mile with direction E
    Go magicworld road for 0.400000 mile with direction SW
    Go haunted1 road for 1.000000 mile with direction S

    #doctest in case an attraction has 2 paths - one for both set of people and one for only non-handicapped, in such case
    #if yes is given for handicap requirement then the path in which handicap is allowed is displayed even if it is longer
    >>> G.output_best_route('boattour', 'hauntedhouse', 'yes')
    <BLANKLINE>
    Notice: hauntedhouse facility has the following information: min height 150 cm, min weight 130 pounds, handicap(Y), children(Y)
    <BLANKLINE>
    The best route from boattour to hauntedhouse is:
    <BLANKLINE>
    Go mw4 road for 0.300000 mile with direction E
    Go mw3 road for 0.010000 mile with direction E
    Go magicworld road for 0.400000 mile with direction SW
    Go mainstreet1 road for 0.200000 mile with direction W
    Go mainstreet2 road for 0.150000 mile with direction S
    Go mainstreet3 road for 0.850000 mile with direction E


    """
    G = MyGraph()

    inputs = input('\nEnter the number of start and end places (XXX XXX): ')
    startnum, endnum = inputs.split()
    start, end = G.num_to_attra(int(startnum), int(endnum))
    user = input("Do you need handicap path ( yes OR no):")

    G.output_best_route(start, end, user)
    a = []
    for reachable_node in nx.dfs_postorder_nodes(G, source=start):
        a.append(reachable_node)
    reachable_n = pd.read_csv("reachable.csv")
    y=reachable_n.values.T.tolist()
    ynew = [item for sublist in y for item in sublist]
    print("Node", start," is reachable to other nodes of the graph  :",all(x in ynew for x in a))

    while True:
        input1 = input("\nDo you want to go somewhere else? yes / no: ")
        if input1 == "yes":
            destination = input('\nEnter the number of end place or "quit": ')
            if destination == 'quit':
                print('Goodbye!')
                break
            else:
                start, end = G.num_to_attra(int(endnum), int(destination))
                G.output_best_route(start, end, user)
                endnum = destination
                a = []
                for reachable_node in nx.dfs_postorder_nodes(G, source=start):
                    a.append(reachable_node)
                ynew = [item for sublist in y for item in sublist]
                print("Node", start, " is reachable to other nodes of the graph  :", all(x in ynew for x in a))

        else:
            print('Goodbye!')
            break


if __name__ == "__main__":
    main()