By: Ethan Rarity (erarity@masonlive.gmu.edu), Steven Schluchter (steven.schluchter@gmail.com), and Justin Z. Schroeder (jzschroeder@gmail.com).

This README file was written to accompany the program SelfDualCheckerForSmallestGraph.py.

The program SelfDualCheckerForSmallestGraph.py was written as part of the research done in the article titled: The smallest self-dual graphs in a pseudosurface, by E.Rarity, S. Schluchter, and J.Z. Schroeder.

The program SelfDualCheckerForSmallestGraph.py runs on Python2 and requires the Python2 library networkx to be installed in order to execute.

In order to run the program, first download SelfDualCheckerForSmallestGraph.py and at least one of the graph files F1.txt, F2.txt, F3.txt, F4.txt, F5.txt.  Then, execute the following (this example is from a bash shell running ubuntu linux) shell command: python SelfDualCheckerForSmallestGraph.py F1.txt.  To run the program on the graph file F2.txt, substitute F2.txt in the aforementioned shell command.

When executing the program on the graph F1.txt, the file F1-results.txt file is created.


*********************************************************************
How to understand the graph setup.

The line "Read list as: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]" is a list of edges, which are enumerated by the numbers in the list.
The line "Adding edge 1 as: (1,2)" means that edge number 1 is an edge joining vertices 1 and 2.
The line "Found degree six vertex to be: 1" means that the vertex 1 is the only vertex of degree 6.
The line "Build vertex list as: [1,2,3,4,5,6,7]" means that there are 7 vertices in the graph, which are enumerated by the numbers in the list.

Read list as: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]  
Adding edge 1 as: (1,2)
Adding edge 2 as: (1,3)
Adding edge 3 as: (1,4)
Adding edge 4 as: (1,5)
Adding edge 5 as: (1,6)
Adding edge 6 as: (1,7)
Adding edge 7 as: (2,7)
Adding edge 8 as: (6,7)
Adding edge 9 as: (2,6)
Adding edge 10 as: (3,4)
Adding edge 11 as: (4,5)
Adding edge 12 as: (3,5)
Adding edge 13 as: (2,3)
Found degree six vertex to be: 1
Built vertex list as: [1, 2, 3, 4, 5, 6, 7]

*********************************************************************
How to understand the output of the program to a results file associated to a graph.

The two-line block that appears below means that the permutation 1->9, 2->12, 3->3, 4->11, 5->10, 6->6, 7->7, 8->8, 9->1, 10->5, 11->4, 12->2, 13->13 is a permutation of the edges of the corresponding graph that is a component-split algebric duality correspondence that makes that graph topologically self dual in a surface; the only 6-star maps to the edges inducing a cycle and the only vertex of degree 6 has only one umbrella.

Found INVALID solution:[9, 12, 3, 11, 10, 6, 7, 8, 1, 5, 4, 2, 13]
Solution did not contain two or more components - solution omitted.

The four-line block that appears below means that the permutation 1->2, 2->1, 3->3, 4->10, 5->6, 6->7, 7->9, 8->8, 9->5, 10->4, 11->11, 12->12, 13->13 is a permutation of the edges of the corresponding graph that is a component-split algebraic duality correspondence that makes that graph topologically self-dual in a pesudosurface (the pinched sphere in this case); the only 6-star maps to the edges of a bowtie graph, and the second set of passes (of the corresponding facial boundary walk) is the set of passes corresponding to the choice of facial boundary walk that will make the graph topologically-self dual in a pseudosurface.

Passes: (2, 3),(4, 7)
Passes: (2, 4),(3, 7)
Found a solution using the second set of passes.
Found VALID solution:[2, 1, 3, 10, 6, 7, 9, 8, 5, 4, 11, 12, 13]

The two lines below mean that there were 4 total permutations of the edges of the corresponding graph that were component-split algebraic duality correspondences (thus making the graph topologically self-dual in a 2-complex), and that 4 of these permutations made the graph self-dually embeddable in a pseudosurface.

There were 4 topological duals found.

There were 4 winners found.




