'''
Created on 10/11/2014

@organization: Lancaster University & University of Leeds
@version: 1.0
Created on 11/12/2014

@author: Victor Padilla
@contact: v.padilla@lancaster.ac.uk

Class related to Phylogenetic trees

'''
import copy
import numpy
from Bio import Phylo
from cStringIO import StringIO

class cluster:
    '''
    cluster object for Clustering class
    '''
    pass
    
class Clustering:
    '''
    This class allows to transform a triangular matrix
    in a philogenetic tree cutting it at some point 
    
    
    usage:
    ###  The omr name array
    species = [ "omr1", "omr2", "omr3", "omr4", "omr5","omr6" ]
    matr = [ [ 0., 6., 8., 1., 2. ,6. ],
             [ 0., 0., 8., 6., 6. ,4. ],
             [ 0., 0., 0., 8., 8. ,8. ],
             [ 0., 0., 0., 0., 2. ,6. ],
             [ 0., 0., 0., 0., 0. ,6. ],
             [ 0., 0., 0., 0., 0. ,0. ], ]
    
    clustering=Clustering()
    ### Transforms the triangular matrix in a complete matrix
    matr= clustering.getCompleteMatrix(matr)
    
    ### establishes the clusters
    clu = clustering.make_clusters(species)  
    
    ### Regroup the cluster 
    tree = clustering.regroup(clu, matr)
    
    ### get the string in newick format
    strTree=clustering.getStringTree(tree,tree.height,"")
    
    print(strTree)
    clustering.showTree(strTree)
    
    ### Takes the main tree with 5 branches
    maintree=clustering.getBetterTree(tree,5)
    strTree=clustering.getStringTree(maintree,maintree.height,"")
    print(strTree)
    clustering.showTree(strTree)
        
    '''
    
    def make_clusters(self,species):
        '''
        Organises the cluster based on the species array
        '''
        clusters = {}
        Id = 1
        for s in species:
            c = cluster()
            c.id = Id
            c.data = s
            c.size = 1
            c.height = 0
            clusters[c.id] = c
            Id = Id + 1
        return clusters
    
    def __find_min(self,clu, d):
        '''
        finding the minimum distance
        private function
        '''
        mini = None
        i_mini = 0
        j_mini = 0
        for i in clu:
            for j in clu:
                if j>i:
                    tmp = d[j -1 ][i -1 ]
                    if not mini:
                        mini = tmp
                    if tmp <= mini:
                        i_mini = i
                        j_mini = j
                        mini = tmp
        return (i_mini, j_mini, mini)
    
    def regroup(self,clusters, dist):
        '''
        organizing the cluster
        '''
        i, j, dij = self.__find_min(clusters, dist)
        ci = clusters[i]
        cj = clusters[j]
        # create new cluster
        k = cluster()
        k.id = max(clusters) + 1
        k.data = (ci, cj)
        k.size = ci.size + cj.size
        k.height = dij / 2.
        # remove clusters
        del clusters[i]
        del clusters[j]
        # compute new distance values and insert them
        dist.append([])
        for l in range(0, k.id -1):
            dist[k.id-1].append(0)
        for l in clusters:
            dil = dist[max(i, l) -1][min(i, l) -1]
            djl = dist[max(j, l) -1][min(j, l) -1]
            dkl = (dil * ci.size + djl * cj.size) / float (ci.size + cj.size)
            dist[k.id -1][l-1] = dkl
        # insert the new cluster
        clusters[k.id] = k
    
        if len(clusters) == 1:
            # we're through !
            return clusters.values()[0]
        else:
            return self.regroup(clusters, dist)
    
    def __pprint(self,tree, length):
        '''
        print the tree in newick format 
        (A:0.1,B:0.2,(C:0.3,D:0.4):0.5);       distances and leaf names
        '''
        if tree.size > 1:
            # it's an internal node
            print "(",
            self.__pprint(tree.data[0], tree.height)
            print ",",
            self.__pprint(tree.data[1], tree.height)
            print ("):%2.2f" % (length - tree.height)),
        else :
            # it's a leaf
            print ("%s:%2.2f" % (tree.data, length)),
    
    def getStringTree(self,tree, length,strOut):
        '''
        returns the string of the tree in newick format
        (A:0.1,B:0.2,(C:0.3,D:0.4):0.5);       distances and leaf names
        '''
        if tree.size > 1:
            # it's an internal node
            strOut+="("
            strOut=self.getStringTree(tree.data[0], tree.height,strOut)
            strOut+=","
            strOut=self.getStringTree(tree.data[1], tree.height,strOut)
            strOut+="):"+str(length- tree.height)
        else :
            # it's a leaf
            strOut+=str(tree.data)+":"+str(length)
        return strOut
    
    
    def createClusters(self,tree,length):
        '''
        separates the tree at the point determined by length
        '''
        clusters=[]
        self.__separateClusters(clusters,tree,length)
        self.clusters=self.__filterClusters(clusters,length)
        return clusters
    
    def getLeafs(self,tree):
        '''
        returns the number of leafs from a tree
        '''
        leafs=[]
        self.getTreeLeafs(leafs,tree,tree.height)
        return leafs
    
    def __separateClusters(self,clusters,tree,length):
        '''
        divides the main tree in multiples trees based on the length
        '''
        if tree.size > 1:
            if tree.height>=length:
                clusters.append(tree.data[0])
                clusters.append(tree.data[1])
            else:
                pass
            self.__separateClusters(clusters,tree.data[0], length) 
            self.__separateClusters(clusters,tree.data[1], length)
        
    def __filterClusters(self,clusters,length): 
        '''
        removes trees higher than length
        ''' 
        clustersOut=[]  
        for c in clusters:
            if c.height<length:
                clustersOut.append(c)
        return clustersOut
    
    def getTreeLeafs(self,leafs,tree,length):
        '''
        returns the number of leafs from a tree. Recursive function
        '''
        if tree.size > 1:
            # it's an internal node
            self.getTreeLeafs(leafs,tree.data[0], tree.height)
            self.getTreeLeafs(leafs,tree.data[1], tree.height)
        else :
            # it's a leaf
            leafs.append(tree.data)
            
    def getBetterTree(self,tree,numberLeafs):
        '''
        takes the smallest tree that has <= numberLeafs
        '''
        while True:
            leafs=self.getLeafs(tree)
            if len(leafs)<=numberLeafs:
                return tree
            clusters=self.createClusters(tree,tree.height)
            tree=self.getMainTree(clusters)
    
    
    def getAverageDistance(self,matr):
        '''
        returns the average distance from the matrix
        '''
        sumat=0
        lengthMatrix=len(matr[0])
        length=lengthMatrix*lengthMatrix-lengthMatrix
        for i in range(lengthMatrix):
            for j in range(lengthMatrix):
                    sumat=sumat+matr[i][j]
        return (sumat/length)/2
    
    def getMaximumDistance(self,matr):
        '''
        returns the maximum distance from the matrix
        '''
        maxValue=0
        lengthMatrix=len(matr[0])
        for i in range(lengthMatrix):
            for j in range(lengthMatrix):
                    if matr[i][j]>maxValue:
                        maxValue=matr[i][j]
        return maxValue/2
    
    def getMainTree(self,clusters):
        '''
        Takes the tree with the higher number of leafs
        '''
        maxim=0
        indexmax=0
        for i in range(len(clusters)):
            leafs=self.getLeafs(clusters[i])
            if len(leafs)>maxim:
                maxim=len(leafs)
                indexmax=i
                
        return clusters[indexmax]
            
    def getCompleteMatrix(self,matr):
        '''
        return the complete matrix from a 
        triangular matrix
        '''
        newMatrix=copy.copy(matr)
        if isinstance(matr,numpy.ndarray):
            newMatrix=newMatrix.tolist()
        lengthMatrix=len(matr[0])
        for i in range(lengthMatrix):
            for j in range(i,lengthMatrix): 
                newMatrix[j][i]=matr[i][j]
        return newMatrix
    
    def showTree(self,strTree): 
        '''
        Shows a graphical representation from a newick tree format
        '''  
        handle = StringIO(strTree)
        tree = Phylo.read(handle, 'newick')
        tree.ladderize()   
    #     Phylo.draw(tree) 
        Phylo.draw_ascii(tree) 
         
         
