#This program was written by Ethan Rarity (erarity@masonlive.gmu.edu) and Steve Schluchter (steven.schluchter@gmail.com)
#
#	Notes:
#
#	- G 		- will become the graph that we test for self-duality.
#	- endind	- a counter used to enumerate the edges of the graph G.
#	- listlen	- variable to assist in the reading in of the users input file to help form a graph G.
#	-permlist	- stores the permutation provided in the file
#	-numberstoedges - dictionary used to look up an edge tuple from its label.
#	-edgestonumbers - dictionary mapping the end vertices of the edge to the edge label.

import networkx as nx
import sys

G = nx.Graph()
edgeind		= 0
listlen		= 0
numberstoedges 	= {}
edgestonumbers 	= {}
permlist 	= []

#Uses Heap's algorithm to generate all permutations of [1,...,N]
def permute(index, list):
	
	if(index == 1): 
		yield list
	else:
		for i in range(index-1):
			for hp in permute(index-1, list):
				yield hp
			j = 0 if (index % 2) == 1 else i
			list[j],list[index-1] = list[index-1],list[j]
		
		for hp in permute(index-1, list):
			yield hp

#Returns a list of edges incident to a given vertex.
#Note: Since networkx treats the undirected edge (0,1) as being distinct from the undirected edge (1,0), we make the choice to put the lower-numbered vertex in the first entry in each ordered pair.
def vertexStar(G,vertex):
	
	star = []
	
	for edge in G.edges(vertex):
		if(edge[0] > edge[1]):
			edgeTuple = (edge[1], edge[0])
		else:
			edgeTuple = (edge[0], edge[1])
		star.append(edgeTuple)
	
	return star

#Returns the result of permuting the edges in vstar using the permutation perm. 
def dualEdges(vstar,perm):
	
	dualEdges = []
	
	for edge in vstar:
		label = perm[edgestonumbers[edge]-1]
		edge = numberstoedges[label]
		dualEdges.append(edge)
	
	return dualEdges

#Determines if a 6-star permutes to edges including a cycle.
#Note: This is only run under the conditions that perm is an algebraic duality correspondence.
def checkCycles(perm):
	
	starSix = vertexStar(G,degreeSix)
	dualSix = dualEdges(starSix,perm)
	
	H = nx.Graph()
	H.add_edges_from(dualSix)

	#Iterate through the edges and ensure that they are all connected with degree 2.
	for node in H.nodes():
		if(H.degree(node) != 2):
			print "\nThis 6-star permutes to a bowtie. There is a node (%s) without two degrees (has %s)." % (node,H.degree(node))
			return False
	return True

#Returns true if a vertex star maps via the inverse permutation to edges inducing more than one component of G, thus detecting multiple umbrellas.
#Notes: This is not an exhaustive test since it is used if starSix maps to edges inducing a cycle.
def checkComponents(perm):
	
	starSix = vertexStar(G,degreeSix)
	inverseEdgeMap = []
	
	for edge in starSix:
		inverseEdgeMap.append(numberstoedges[perm.index(edgestonumbers[edge]) + 1])
	
	print "\nBuilt Graph from inverse edge map: %s" %(inverseEdgeMap)
	F = nx.Graph()
	F.add_edges_from(inverseEdgeMap)
	
	return (nx.number_connected_components(F) > 1)

#Returns a boolean indicating that a permutation mapping the edges of a 6-star to the edges of a bowtie will produce an embedding in a pseudosurface.
#Note: H is the constructed graph representing the "bowtie."
def checkBowtie(G,perm):

	sequence = []

	#Build the bowtie from the edges of the image of the 6-star edges.
	starSix = vertexStar(G,degreeSix)
	dualSix = dualEdges(starSix,perm)
	H = nx.Graph()
	H.add_edges_from(dualSix)

	#Determine which vertex is degree four and remove it.
	degrees = H.degree(H.nodes())
	V = -1;
	withoutFour = H.nodes();
	print "Built degree dictionary as: %s" % (degrees)
	
	for node in degrees.items():
		if(node[1] == 4):
			if(node[0] == 1):
				withoutFour.remove(node[0])
				V = node[0]
				print "Found degree four vertex to be %s and removed it." % (node[0])
				break
			else:
				print "The dual vertex of the bowtie was not 1. Checking alternative."
				return checkComponents(perm)
	if(len(withoutFour) > 4):
		print "Degree four vertex was not found or not properly removed."
		return False
	if(V == -1):
		print "Could not find a vertex with degree four."
		return False
	
	#Select a starting point for the sequence
	alpha = withoutFour[0]
	beta = 0
	gamma = 0
	delta = 0
	withoutFour.remove(alpha)
	
	#This code assigns beta and gamma to be the two non-neighbors of alpha
	#and assigns delta to be the neightbor of alpha in the bowtie.
	for node in withoutFour:
		if(len(withoutFour) < 1):
			print("Could not find a valid non-neighbor to alpha. All options exhausted.")
			return False
		if(not H.has_edge(alpha,node)):
			beta = node
			withoutFour.remove(node)
			break
		else:
			delta = node
			withoutFour.remove(node)
	
	if(len(withoutFour) == 2):
		if(not H.has_edge(alpha,withoutFour[0])):
			gamma = withoutFour[0]
			delta = withoutFour[1]
		else:
			delta = withoutFour[0]
			gamma = withoutFour[1]

	if(len(withoutFour) == 1):
		gamma = withoutFour[0]

	#Now that alpha and beta are determined, construct a pass through the degree four vertex, V
	sequence.append((alpha, beta))
	#The other pass through V is made using gamma and delta
	sequence.append((gamma, delta))

	#Find out what other facial boundary walks contain V.
	findNodes = list(G.nodes())
	#We have already considered the 6-star vertex, so we remove it from the list.
	findNodes.remove(degreeSix)

	#Determine if V is in the boundary of each face, and if so, add the neighbors of V
	#in the facial boundary angle as a tuple to sequence.
	for node in findNodes:
		cuts = vertexStar(G,node)
		cycles = dualEdges(cuts,perm)
		T = nx.Graph()
		T.add_edges_from(cycles)
		for node in T.nodes():
			if (node == 1):
				neighbors = nx.all_neighbors(T,node)
				neighborsList = []
				for n in neighbors:
					neighborsList.append(n)
				sequence.append((neighborsList[0],neighborsList[1]))	

	print "Built sequence list as: %s" %(sequence)
	print perm

	fi.write('\nPasses: ')
	fi.write(str(sequence[0]))
	fi.write(',')
	fi.write(str(sequence[1]))

	rotationSequence = list(sequence) #Builds a separate list

	passed = rotationScheme(rotationSequence)
	print "Sequence contains two umbrellas: %s" %(passed)
	if(passed):
		fi.write('\nFound a solution using the first set of passes.')
		return True

	#Build the alternate sequence, effectively switching beta and gamma.
	firple = sequence[0]
	secple = sequence[1]
	if(H.has_edge(firple[0],secple[1])):
		sequence[0] = (firple[0],secple[0])
		sequence[1] = (firple[1],secple[1])
	else:
		sequence[0] = (firple[0],secple[1])
		sequence[1] = (secple[0],firple[1])

	print "Built alternate sequence list as: %s" %(sequence)
	print perm

	#Write the passes to the file.
	fi.write('\nPasses: ')
	fi.write(str(sequence[0]))
	fi.write(',')
	fi.write(str(sequence[1]))

	rotationSequence = list(sequence)

	passed = rotationScheme(rotationSequence)
	print "Sequence contains two umbrellas: %s" %(passed)
	if(passed):
		fi.write('\nFound a solution using the second set of passes.')
		return True
	else:
		fi.write('\nCould not find a solution after using both sets of passes.')
		return False

#Takes, as input, a sequence of tuples indicating the facial boundary passed through a vertex.
#Note: rotationScheme returns true if the passes form more than one umbrella. Otherwise, returns false.
#Note: v is the current umbrella being filled in order of tuples in sequence.
#Note: r is a list of lists of vertices appearing in cyclic orders in each umbrella of the vertex in question.
def rotationScheme(sequence):
	
	l = sequence
	r = []
	v = []
	
	lVal = l[0]
	v.append(lVal[0])
	v.append(lVal[1])
	l.remove(lVal)
	
	for i in range(len(l)-1):
		x = v[len(v)-1]
		for y in l:
			if(y[0] == x):
				if(y[1] == v[0]):
					r.append(v)
					v = []
					l.remove(y)
					lVal = l[0]
					v.append(lVal[0])
				else:
					v.append(y[1])
					l.remove(y)
				break
			elif(y[1] == x):
				if(y[0] == v[0]):
					r.append(v)
					v = []
					l.remove(y)
					lVal = l[0]
					v.append(lVal[0])
				else:
					v.append(y[0])
					l.remove(y)
				break

	#Solver for the last element in the sequence.
	x = v[len(v)-1]

	lVal = l[0]
	
	if(x == lVal[0]):
		if(v[0] == lVal[1]):
			r.append(v)
		else:
			print "Could not properly form a facial boundary. Perm: %s" %(perm)
			#sys.exit(1) uncomment this is you want the program to exit here
	elif(x == lVal[1]):
		if(v[0] == lVal[0]):
			r.append(v)
		else:
			print "Could not properly form a facial boundary. Perm: %s" %(perm)
			#sys.exit(1) uncomment this if you want the program to exit here
	else:
		print "\nGiven sequence creates a malformed edge list. No facial boundary can be constructed. Perm: %s\nList: %s\nRotations: %s" %(perm, v, r)
		#sys.exit(1) uncomment this if you want the program to exit here

	print "Rotation scheme: %s" %(r)

	return (len(r) > 1)



#Builds the graph from the structure provided in the input file.
#Notes: See files: F1.txt, F2.txt, etc. in the GitHub repository for proper notation.
#Pull the file name from the command line args.
if(len(sys.argv) == 2):
	filename = sys.argv[1]
elif(len(sys.argv) > 2):
	print "Additional arguments supplied. Try: python <<program name>> <<filename>>"
	#sys.exit(1) uncomment this if you want the program to exit here
else:
	print "Too few arguments supplied. Try: python <<program name>> <<filename>>"
	#sys.exit(1) uncomment this if you want the program to exit here

#Open the file and construct the graph from the formatted instructions.
f = open(filename, 'r')

#Second file for writing output.
filenamelist = filename.split('.')
fileN = filenamelist[0]
fi = open(fileN + '-results.txt','w')

for line in f:
	words = line.split()
	if(len(words) <= 0):
		continue
	if(words[0] == "LEN"):
		if(words[1] is None):
			print "Error parsing length of permuation list. Check input file."
			#sys.exit(1) uncomment this if you want the program to exit here
		else:
			listlen = int(words[1]);
	elif(words[0] == "LIST"):
		for i in range(1,listlen + 1):
			permlist.append(int(words[i]))
		print "Read list as: %s" % permlist
		fi.write('Read list as: ')
		fi.write(str(permlist))

	elif(words[0] == "AE"):
		edgeind = edgeind + 1
		if(words[1] is None or words[2] is None):
			print "Error forming Graph edge from supplied arguments."
			#sys.exit(1) uncomment this if you want the program to exit here
		else:

			if(int(words[1]) > int(words[2])):
				edgeTuple = (int(words[2]), int(words[1]))
			else:
				edgeTuple = (int(words[1]), int(words[2]))

			G.add_edge(edgeTuple[0],edgeTuple[1])
			numberstoedges[edgeind] 	= (edgeTuple)
			edgestonumbers[(edgeTuple)] 	= edgeind
			print "Adding edge %02d as: (%s, %s)" % (edgeind,edgeTuple[0],edgeTuple[1])
			fi.write('\nAdding edge ')
			fi.write(str(edgeind))
			fi.write(' as: (')
			fi.write(str(edgeTuple[0]))
			fi.write(',')
			fi.write(str(edgeTuple[1]))
			fi.write(')')


f.close()

#Determine which vertex has a degree of six.
#Note: In our problem, a 13-edge self-dual embeddable graph in a pseudosurface has only one vertex of degree six.
#Note: This code block identifies which vertex that is, and will later exit the program should no valid one be found.

degreeSix = -1
degrees = G.degree(G.nodes())
print "Built degree dictionary as: %s" % (degrees)
for node in degrees.items():
	if(node[1] == 6):
		degreeSix = node[0]
		print "Found degree six vertex to be: %s" % (node[0])
		fi.write('\nFound degree six vertex to be: ')
		fi.write(str(node[0]))
		break
if(degreeSix == -1):
	print "No vertex of degree six found."

#Invokes the permute() function to generate all possible permutations of [1,...,N] using Heap's algorithm
perms = permute(len(permlist),permlist)

#Creation of nodel
#Note: nodel (node list) is a list of the numbered vertices contained in the graph.
#Note: nodel is 0-indexed, but nodel[0] will contain 1, as the vertices are 1-indexed.
nodel = []
for i in range(1,len(G)+1):
	nodel.append(i)

print "Built vertex list as: %s" % nodel
fi.write('\nBuilt vertex list as: ')
fi.write(str(nodel))
fi.write('\n\n')

print "\nFinding solutions, please wait. . .\n"

#Begin finding "winners" among all possible permutations of [1...N]
#This block introduces: winners, a counter that increments each time a winner is found, and
#topDuals, a counter that increments each time a topological dual is found.

winners  = 0
topDuals = 0
for perm in perms:

	selfDual = True
	for node in nodel:
		star = vertexStar(G,node)
		dstar = dualEdges(star,perm)

		#NOTE: H is the induced graph containing only the permuted edges from star.
		H = nx.Graph()
		H.add_edges_from(dstar)
		if(not nx.is_eulerian(H)):
			selfDual = False
			break

	if (selfDual == True):
		topDuals = topDuals + 1;
		print "\nA topological dual was found using permutation:\n%s\n" %(perm)
		if(degreeSix == -1):
			print "Found no valid vertex of degree six. Exiting program."
			break
		else:
			cycles = checkCycles(perm)
			if(cycles):
				components = checkComponents(perm)
				if(components):
					print "\nFound VALID solution:"
					print perm
					fi.write('\nFound VALID solution:')
					fi.write(str(perm))
					winners = winners + 1;
				else:
					print "Found INVALID solution:"
					print perm
					print "Solution did not contain two or more components - solution omitted."
					fi.write('Found INVALID solution:')
					fi.write(str(perm))
					fi.write('\nSolution did not contain two or more components - solution omitted.')
			else:
				validBowtie = checkBowtie(G,perm)
				if(validBowtie):
					print "\nFound VALID solution:"
					print perm
					fi.write('\nFound VALID solution:')
					fi.write(str(perm))
					winners = winners + 1;
				else:
					print "Found INVALID solution:"
					print perm
					print "Solution did not contain a valid 'bowtie' structure"
					fi.write('Found INVALID solution:')
					fi.write(str(perm))
					fi.write('\nSolution did not contain a valid bowtie structure')

print "\nFinished testing all permutations."

#Check Results - identifies how many topological duals and winners were found and writes the result to the <graph_filename>-results.txt file.
if(topDuals >= 1):
	print "\nThere were %s topological duals found.\n" %(topDuals)
	fi.write('\nThere were ')
	fi.write(str(topDuals))
	fi.write(' topological duals found.\n')
elif(topDuals == 0):
	print "\nThere were no topological duals found.\n"
	fi.write('\nThere were no topological duals found.\n')
if(winners >= 1):
	print "\nThere were %s winners found.\n" %(winners)
	fi.write('\nThere were ')
	fi.write(str(winners))
	fi.write(' winners found.\n')
elif(winners == 0):
	print "\nThere were no winners found.\n"
	fi.write('\nThere were no winners found.\n')


fi.close()
print "Results written to %s-results.txt" %(fileN)
