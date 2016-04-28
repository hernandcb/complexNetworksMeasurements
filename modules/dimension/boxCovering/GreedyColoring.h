/*
 * GreedyColoring.h
 *
 *  Created on: 10.03.2016
 *      Author: Hernán D. Carvajal
 */

#ifndef GREEDYCOLORING_H_
#define GREEDYCOLORING_H_

#include <NetworKit/graph/Graph.h>

namespace BoxCovering {

/**
 * Class used to perform a box covering using the greedy coloring algorithm
 */
class GreedyColoring {

public:

  /**
  * This method choose a color randomly from the set of valid colors that is
  * not present in the not valid colors set.
  * If there are not valid colors it is returned a new color that is higher than
  * all the colors already present.
  */
  int  chooseColor(std::set<int> validColors, std::set<int> notValidColors);

  /**
  * This method computes the greedy coloring on the graph received by parameter
  * and returns a matrix with the boxes defined for all the possible box
  * lengths.
  */
  std::vector<std::vector<NetworKit::node>> greedyColoring(NetworKit::Graph g);

};

} /* namespace NetworKit */

#endif /* GREEDYCOLORING_H_ */
