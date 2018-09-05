import timeit
import pickle
import numpy as np
import scipy.stats as st
import networkx as nx
import matplotlib.pyplot as plt

from simulation.helpers import update_progress, csv_export, create_random_graph_distances
from simulation.plotting import print_graph, print_tips_over_time, \
print_tips_over_time_multiple_agents, print_tips_over_time_multiple_agents_with_tangle, \
print_attachment_probabilities
from simulation.simulation import Single_Agent_Simulation
from simulation.simulation_multi_agent import Multi_Agent_Simulation

#############################################################################
# SIMULATION: SINGLE AGENT
#############################################################################

#Parameters: no_of_transactions, lambda, no_of_agents, alpha, latency (h), tip_selection_algo
#Tip selection algorithms: Choose among "random", "weighted", "unweighted" as input

# simu = Single_Agent_Simulation(100, 50, 1, 0.005, 1, "unweighted")
# simu.setup()
# simu.run()
# simu.calc_exit_probabilities()
# print_graph(simu)
# print_tips_over_time(simu)

# simu.calc_confirmation_confidence()

#############################################################################
# SIMULATION: MULTI AGENT
#############################################################################

#Parameters: no_of_transactions, lambda, no_of_agents, alpha, distance, tip_selection_algo
# latency (default value 1), agent_choice (default vlaue uniform distribution, printing)
#Tip selection algorithms: Choose among "random", "weighted", "unweighted" as input

# partitioning_values = []
# average_partitioning_across_simus = []

start_time = timeit.default_timer()
runs = 1
# counter = 0

number_of_agents = 10
distances = create_random_graph_distances(number_of_agents)

# distances = [[0.0, 80.0, 40.0, 60.0, 80.0, 40.0, 40.0, 20.0, 60.0, 40.0], [80.0, 0.0, 80.0, 60.0, 40.0, 80.0, 80.0, 60.0, 20.0, 40.0], [40.0, 80.0, 0.0, 60.0, 80.0, 40.0, 20.0, 20.0, 60.0, 40.0], [60.0, 60.0, 60.0, 0.0, 60.0, 60.0, 60.0, 40.0, 40.0, 20.0], [80.0, 40.0, 80.0, 60.0, 0.0, 80.0, 80.0, 60.0, 20.0, 40.0], [40.0, 80.0, 40.0, 60.0, 80.0, 0.0, 40.0, 20.0, 60.0, 40.0], [40.0, 80.0, 20.0, 60.0, 80.0, 40.0, 0.0, 20.0, 60.0, 40.0], [20.0, 60.0, 20.0, 40.0, 60.0, 20.0, 20.0, 0.0, 40.0, 20.0], [60.0, 20.0, 60.0, 40.0, 20.0, 60.0, 60.0, 40.0, 0.0, 20.0], [40.0, 40.0, 40.0, 20.0, 40.0, 40.0, 40.0, 20.0, 20.0, 0.0]]

for i in range(runs):

    simu2 = Multi_Agent_Simulation(10000, 50, number_of_agents, 0.1, distances, "weighted", _printing=True)
    simu2.setup()
    simu2.run()

    # print(simu2.record_attachment_probabilities)

    with open('scenario1.pkl', 'wb') as handle:
        pickle.dump(simu2.record_attachment_probabilities, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # csv_export(simu2)

    # partitioning_values.append(simu2.measure_partitioning())
    # average_partitioning_across_simus.append(np.mean(partitioning_values))

    # update_progress(i/runs, str(i))
    # counter += 1

    #Sanity checks
    print("SANITY CHECKS:\n")
    for agent in simu2.agents:
        # print("VALID TIPS OF AGENT " + str(agent) + ":   " + str(agent.tips))
        print("SUM OF EXIT PROBS FOR ALL TIPS:   " + str(sum(tip.exit_probability_multiple_agents[agent] for tip in agent.tips)) + "\n")
    #
    #     for transaction in simu2.DG.nodes:
    #             print(str(transaction) + "   " + str(transaction.cum_weight_multiple_agents[agent]))
    #             print(str(transaction) + "   " + str(transaction.cum_weight_multiple_agents_2[agent]))
    #             # print(str(transaction) + "   " + str(transaction.exit_probability_multiple_agents[agent]))
    #             # print(str(transaction) + "   " + str(transaction.confirmation_confidence_multiple_agents[agent]))

print("TOTAL simulation time: " + str(np.round(timeit.default_timer() - start_time, 3)) + " seconds\n")

# print(partitioning_values)
# print(np.mean(partitioning_values))
# print(np.var(partitioning_values))

#############################################################################
# PLOTTING
#############################################################################

# print_graph(simu2)
# print_tips_over_time(simu2)
# print_tips_over_time_multiple_agents(simu2, simu2.no_of_transactions)
# print_tips_over_time_multiple_agents_with_tangle(simu2, simu2.no_of_transactions)
print_attachment_probabilities(simu2)
# simu2.measure_partitioning_alon()


#Plotting the partitioning values for multiple simulations, cumulative mean and 95% confidence interval


# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.plot(simu2.arrival_times, simu2.record_desc, 'b')
# ax1.plot(np.unique(simu2.arrival_times), np.poly1d(np.polyfit(simu2.arrival_times, simu2.record_desc, 1))(np.unique(simu2.arrival_times)), label="Best Fit Line", linestyle='--')
# ax1.set_ylabel('Total number of descendants', color='b')
#
# ax2 = ax1.twinx()
# ax2.plot(simu2.arrival_times, simu2.record_desc_ratio, 'r-')
# ax2.set_ylabel('Ratio of descendants / total transactions in Tangle', color='r')
# # for tl in ax2.get_yticklabels():
# #     tl.set_color('r')
# ax2.set_xlabel('Time (s)')



# plt.plot(simu2.arrival_times, simu2.record_desc_ratio)
# # plt.plot(np.unique(simu2.arrival_times), np.poly1d(np.polyfit(simu2.arrival_times, simu2.record_desc, 1))(np.unique(simu2.arrival_times)), label="Best Fit Line", linestyle='--')
# plt.xlabel("Time (s)")
# plt.ylabel("Descendants of incoming transaction / total current transactions in Tangle")
# plt.plot(simu2.record_attachment_probabilities)
# lower_bound_95_confidence_interval = st.t.interval(0.80, len(partitioning_values)-1, loc=np.mean(partitioning_values), scale=st.sem(partitioning_values))[0]
# upper_bound_95_confidence_interval = st.t.interval(0.80, len(partitioning_values)-1, loc=np.mean(partitioning_values), scale=st.sem(partitioning_values))[1]
# plt.axhline(y=lower_bound_95_confidence_interval, color='r', linestyle='-')
# plt.axhline(y=upper_bound_95_confidence_interval, color='r', linestyle='-')
# plt.show()
