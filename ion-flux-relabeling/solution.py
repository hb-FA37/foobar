def solution(h, q):
    """
    Args:
        h (int): height of the tree, (1->30).
        q (list(int)): list of indexes to get the parent index of,
            1 to 10000 distinct integers between 1 and 2^h-1
    """
    # Perfect binary tree notes:
    # * number of leaves is 2^h .
    # * number of total nodes is 2^h - 1 .
    #
    # Post-order Traversal: https://xlinux.nist.gov/dads/HTML/postorderTraversal.html
    #     postorder(tree)
    #     begin
    #         if tree is null, return;
    #
    #         postorder(tree.left_subtree);
    #         postorder(tree.right_subtree);
    #         print(tree.root);
    #     end

    # Sort the input nodes for ease of splitting them later.
    input_nodes = sorted(q)
    # Init everything to -1, we need to find explicit answers.
    answers = [-1] * len(q)

    # To return the answer in the correct order, lookup the original index
    # and store the parent label in the answer array.
    def store_answer(label, parent):
        answers[q.index(label)] = parent

    def recurse(nodes, depth, offset):
        """We make use of the fact that we have a perfect binary tree which is post-order labeled.
        This means that the right subtrees are basically the same as the left ones excluding an offset
        value. This offset we can calculate and accumulate when traversing the tree.

        During recursion we only consider left tree basically and apply the offset
        to get the actual node values to do right traversal.
        """
        if depth < 1 or nodes == []:
            # Stop going deeper.
            return

        # Calculate node values based on far left traversal.
        current_node = pow(2, depth) - 1
        left_node = pow(2, depth-1) - 1
        right_node = pow(2, depth) - 2

        # Add the calculated offset values.
        actual_current = current_node + offset
        actual_left = left_node + offset
        actual_right = right_node + offset

        # Edge case: need to remove the root node. More general, we only
        # label childs here, if a parent appears its a root.
        if not nodes:
            return
        if nodes[-1] == actual_current:
            nodes = nodes[:-1]

        # Split the nodes we still need to sort in what is potentially in the left
        # or right tree.
        left_nodes = []
        right_nodes = []
        for x in nodes:
            if x > actual_left:
                right_nodes.append(x)
            else:
                left_nodes.append(x)

        # Since we sorted and all elements are unique it stands that the ends
        # of the list or either the child value or a value lower then a child
        # value.
        if left_nodes and left_nodes[-1] == actual_left:
            store_answer(actual_left, actual_current)
            left_nodes = left_nodes[:-1]
        if right_nodes and right_nodes[-1] == actual_right:
            store_answer(actual_right, actual_current)
            right_nodes = right_nodes[:-1]

        # Recurse left-right trees. For the left we propagate the offset.
        # For the right we will examine nodes which are bigger then the left nodes
        # so we add its value to the offset.
        recurse(left_nodes, depth-1, offset=offset)
        recurse(right_nodes, depth-1, offset=offset+left_node)

    recurse(input_nodes, h, offset=0)
    return answers
