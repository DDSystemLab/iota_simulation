import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx

from simulation.test_dag import build_test_dag

##############################################################################
# HELPER FUNCTIONS
##############################################################################

def anticone_test(graph, tx, block_1, voting_profile):
    """
    Determines whether the transaction passes or fails the anticone set condition
    """    
    
    #Identify transactions that conflict with tx and the blocks they are contained in
    conflict_dict = conflict(graph, tx, block_1.id)
#    print('conflicting transaction', list(conflict_dict.values()), 'block', list(conflict_dict.keys()))
    
    #Iterate through the transactions that conflict with the original transaction in the block
    for tx_2 in list(conflict_dict.values()):
        
        #Identify the blocks and transactions that conflict with tx2
    #                conflict_dict_2 = conflict(graph, tx_2, block_1.id)                
        
        #Extract the blocks that contain a conflicting transaction 
        block_conflict_tx2 = set(list(conflict_dict.keys()))
        print('block that contains a conflicting transaction', block_conflict_tx2)
    
        #Determine the anticone of block_1
        anticone_block_1 = anticone(block_1, graph) 
        print('anticone_block', anticone_block_1)
        
        #Calculate the intersection of conflicting blocks and anticone of block_1
        intersection = block_conflict_tx2.intersection(anticone_block_1)
        print('intersection', intersection)
        
        #Iterate through all blocks that are in the set of blocks that contain conflicting transactions
        #and are in the set of blocks that are not ordered by directly by the DAG
        for block_2 in intersection: 
            print('voting profile', voting_profile[block_1.id, block_2.id])
#            print('')
            if voting_profile[block_1.id, block_2.id] >= 0:
                return False
            else:
                return True           
    
     
def useful_attributes(graph):
    """
    General purpose function that takes an input graph and returns useful attributes 
    of the graph, including: 
        - the graph nodes as a set
        - a list of all the transactions in the graph
    """
    
    #Store the graph nodes
    graph_list = []
    
    #Store the transactions in the graph
    all_tx = []
    
    #Iterate through the graph and append useful attributes to relevant lists
    for block in graph:
        graph_list.append(block)
        all_tx.append(block.transactions)
    
        
    #Flatten the transactions list
    all_tx_flatten = [item for sublist in all_tx for item in sublist]
#    print('original', all_tx)
#    print('flattened', all_tx_flatten)
        
    #Convert to sets
    graph_set = set(graph_list)
#    print('all transactions', all_tx)
#    all_tx_set = set(all_tx_flatten)
#    print('raw all transc', all_tx_flatten)
#    print('raw set all transc', all_tx_set)

  
    return (graph_set, all_tx_flatten)

def tx_inputs(graph, block):
    """
    Returns all the input transactions to a block in the graph. This is a 
    work in progress - really it should be calculating the inputs to a particular
    transaction in a given block. For the time being, assuming that the inputs to a 
    particular transaction are all the transactions in the input blocks
    """
    #List to store input transactions
    transactions = []
    
    #Inputs to a block; in the directed blockDAG architecture are the immediate
    #descendants of the block
    successor_blocks = list(graph.successors(block))
    
    #Append the transactions of each successor block
    for block in successor_blocks:
        transactions.append(block.transactions)    
    
    return transactions
    
             
def anticone(block, graph):
    """
    Returns the anticone (the set of blocks that 
    the DAG does not directly orders with respect to z) of an input block
    
    First calculates the cone, and then the anti-cone. For the built in 
    Python set operators to work, all objects acted on need to be of type set
    """
    
    #Turn block into a set
    block_set = {block}
    
    #Find past of z
    """
    Have to iterate through the ancestors and append invididually to a list. This
    is because you can't convert nx.ancestors directly to a set, because it is
    not a hashable object and sets only allow hashable objects. 
    """
    past_list = []
    
    past = nx.ancestors(graph, block)
    
    for i in past:
        past_list.append(i)
    past_list = set(past_list)
#    print(past_list)
    
    #Find future of z
    future_list = []
    
    future = nx.descendants(graph, block)
    
    for j in future:
        future_list.append(j)
    future_list = set(future_list)
#    print(future_list)
    
    #Cone
    cone = block_set.union(past, future)
    
    #Convert the blockDAG to a set
    graph_set = []
    
    for k in graph:
        graph_set.append(k)
    graph_set = set(graph_set)
    
    #Anticone - difference between the blockDAG and the cone
    anticone_output = graph_set.difference(cone)
    
    return anticone_output
    
    
                
def conflict(graph, tx, current_block_id):
    """
    Returns a set of transactions that conflict with the 
    input transaction tx. 
    
    Outputs a dictionary that maps the conflicting block id to the conflicting 
    transaction - giving a record of both conflicting blocks and transactions
    
    Inputs:
        - current_block = this is the block that the current transaction is stored in
                            Necessary to know this to stop so that the legitimate transaction
                            isn't recognised as a conflict
    """
    
    #Store the conflicting transactions
    conflicts = {}
    
    for block in graph:
        if block.id != current_block_id:
            for transaction in block.transactions:
                if transaction == tx:
                    conflicts[block] = transaction
    
    return conflicts