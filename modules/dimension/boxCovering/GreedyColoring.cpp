#include "GreedyColoring.h"
#include <NetworKit/graph/Graph.h>
#include <NetworKit/distance/Diameter.h>
#include <NetworKit/graph/APSP.h>
#include <iostream>
#include <algorithm>

namespace BoxCovering {

  int  GreedyColoring::chooseColor(std::set<int> validColors, std::set<int> notValidColors)
  {
    std::vector<int> possibleValues;

    // possibleValues =  validColors - notValidColors
    std::set_difference(validColors.begin(), validColors.end(),
                        notValidColors.begin(), notValidColors.end(),
                        std::inserter(possibleValues, possibleValues.begin()));

    if(possibleValues.size() > 0)
    {
      // Pick a random color from the list of possible values
      std::random_device rd;	std::mt19937 engine{rd()};
  	  std::uniform_int_distribution<int> dist(0, possibleValues.size() - 1);

      int n = dist(engine);
      return possibleValues[n];
    }
    else
    {
      // Return the maximun number plus one from both sets
      int max1 = *std::max_element(validColors.begin(), validColors.end());
      int max2 = *std::max_element(notValidColors.begin(), notValidColors.end());

      return (max1 > max2) ? max1 +1 : max2 + 1;
    }
  }

  std::vector<std::vector<NetworKit::node>>  GreedyColoring::greedyColoring(NetworKit::Graph g)
  {
    NetworKit::APSP apsp(g);
    int numberOfNodes = g.numberOfNodes();
    int diameter = NetworKit::Diameter::exactDiameter(g);

    std::vector<std::vector<NetworKit::node>> c(numberOfNodes, std::vector<NetworKit::node>(diameter+1));
    std::vector<NetworKit::node> ordered_nodes = g.nodes();
    std::vector<NetworKit::node> nodes = g.nodes();

    // shuffle nodes
    std::random_device rd; std::mt19937 gen(rd());
    std::shuffle(nodes.begin(), nodes.end(), gen);

    auto it = std::find(ordered_nodes.begin(), ordered_nodes.end(), 3);
    int index = std::distance(ordered_nodes.begin(), it);

    // Give color 0 to the first node
    for(int i = 0; i < diameter+1; i++)
    {
      c[index][i] = 0;
    }

    // Calculate all the distances
    apsp.run();

    for(int i=1; i<numberOfNodes; i++)
    {
      NetworKit::node node_i = nodes[i];

      // Find the index of node_i in the original list of nodes
      int nodei_index = find(ordered_nodes.begin(), ordered_nodes.end(), node_i) - ordered_nodes.begin();

      for(int lb=0; lb < diameter+1; lb++)
      {
        std::set<int> notValidColors;
        std::set<int> validColors;

        for(int j=0; j<i; j++)
        {
          NetworKit::node node_j = nodes[j];

          // Find the index of node_j in the original list of nodes
          auto it = std::find(ordered_nodes.begin(), ordered_nodes.end(), node_j);
          int nodej_index = std::distance(ordered_nodes.begin(), it);

          if( apsp.getDistance(node_i, node_j) >= lb+1 )
          {
            notValidColors.insert(c[nodej_index][lb]);
          }
          else
          {
            validColors.insert(c[nodej_index][lb]);
          }

        }

        int color = chooseColor(validColors, notValidColors);

        c[nodei_index][lb] = color;
      }
    }

    return c;
  }

} /* namespace NetworKit */
