import goody
import prompt
from collections import defaultdict


def read_graph(file : open) -> {str:{str}}:
    result_dict = defaultdict(set)
    for line_number, text in enumerate(file):
        result_dict[text[0]].add(text[2])
    return dict(result_dict)


def graph_as_str(graph : {str:{str}}) -> str:

    output, converted_list = '', sorted([(source_node, sorted(list(des_nodes))) for
                                         source_node, des_nodes in graph.items()], key=lambda x: x[0])
    for source_node, des_nodes in converted_list:
        output += "  {} -> {}\n".format(source_node, des_nodes)
    return output


def reachable(graph : {str:{str}}, start : str, trace : bool = False) -> {str}:
    reached_set = set()
    exploring_list = list(start)
    while True:
        if len(exploring_list) == 0:
            return reached_set
        else:
            if trace:
                print("reached set    = " + str(reached_set))
                print("exploring list = " + str(exploring_list))
            curr_node = exploring_list.pop(0)
            reached_set.add(curr_node)
            if graph.get(curr_node, None) is not None:
                for x in graph[curr_node]:
                    if x not in reached_set:
                        exploring_list.append(x)
            if trace:
                print("transferring node {} from the exploring list to the reached set".format(curr_node))
                print("after adding all nodes reachable directly from {} but not already "
                      "in reached, exploring = {}\n".format(curr_node, exploring_list))


if __name__ == '__main__':
    # Write script here
    file = goody.safe_open('Input the file name detailing the graph: ', 'r', 'Illegal file name', default='graph1.txt')
    graph = read_graph(file)
    print("\nGraph: str (source node) -> [str] (sorted destination nodes)\n" + graph_as_str(graph))

    while True:
        node = input("Input one starting node (or input done): ")

        if node == 'done':
            break
        elif node not in graph:
            print("  Entry Error: '{}'; Illegal: not a source node\n  Please enter a legal String\n".format(node))
        else:
            trace = False if input("Input tracing algorithm option[True]: ") == "False" else True
            print("From the starting node {}, its reachable nodes are: {}\n".format(node, reachable(graph, node, trace)))
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc1.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
