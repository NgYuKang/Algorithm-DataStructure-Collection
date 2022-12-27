class End:
    def __init__(self):
        self.value = -1

    def __add__(self, other):
        self.value += other

    def __int__(self):
        return self.value


class Node:
    def __init__(self, is_leaf=False, size=27):
        self.is_leaf = is_leaf
        self.children = [None for i in range(size)]
        self.suffix_link = None
        self.suffix_id = -1


class Edge:
    def __init__(self, start, end, is_leaf=False):
        self.start = start
        self.end = end
        self.node = Node(is_leaf)


class UkkonenSuffixTree:
    def __init__(self, string):
        self.start_num = 97  # Increase to accommodate more char
        self.actual_string = string
        self.string = "".join([string, "$"])
        self.root = Node()
        self.root.suffix_link = self.root
        self.active_node = None
        self.active_edge = None
        self.active_length = 0
        self.global_end = End()
        self.build_tree()

    def ord_special(self, char):
        if char == '$':
            return 97
        else:
            return ord(char) + 1

    def traverse(self, end):
        while self.active_edge is not None and self.active_length + 1 > (self.active_edge.end.__int__() - self.active_edge.start + 1):
            self.active_length -= (self.active_edge.end.__int__() - self.active_edge.start + 1)
            new_active_edge = self.active_edge.node.children[self.ord_special(self.string[end - self.active_length])-self.start_num]
            self.active_node = self.active_edge.node
            self.active_edge = new_active_edge
        # If we did not find a path for the rest (No Edge found, rule 2 alternative)
        if self.active_edge is None:
            return False
        # We found exact match! Rule 3
        elif self.active_length == 0 or self.string[self.active_edge.start + self.active_length] == self.string[end]:
            return True
        # They don't match, rule 2 normal
        return False

    def build_tree(self):
        start_num = 97  # for ord('a') = 97

        self.active_node = self.root
        j = 0
        show_shopper = False
        for i in range(len(self.string)):
            # Rapid leaf extension trick
            self.global_end.value += 1
            new_node = None
            while j <= i:
                # Recalculate active length if we are at root
                if self.active_node == self.root:
                    self.active_length = i - j
                # Get new active edge if not showstopper
                if not show_shopper:
                    # Get the edge at where the active length currently is
                    # Accommodates when you use suffix link
                    self.active_edge = self.active_node.children[self.ord_special(self.string[i-(self.active_length)]) - start_num]
                show_shopper = False
                same_char = self.traverse(i)
                # Rule 1 (Redundant once leaf trick implemented so can be removed....)
                # if self.active_node.is_leaf:
                #     pass
                # Rule 2
                if not self.active_node.is_leaf and not same_char and self.active_edge is not None:
                    # Create new edge for existing edge
                    new_edge_existing = Edge(self.active_edge.start+self.active_length, self.global_end, True)
                    # Create new edge for new branch
                    new_edge_branch = Edge(i, self.global_end, True)
                    # Update existing edge to be non-leaf edge and also its data
                    self.active_edge.end = self.active_edge.start+self.active_length-1
                    self.active_edge.node.is_leaf = False
                    self.active_edge.node.suffix_link = self.root
                    if new_node is not None:
                        new_node.suffix_link = self.active_edge.node
                    new_node = self.active_edge.node
                    # Update nodes
                    self.active_edge.node.children[(self.ord_special(self.string[self.active_edge.start+self.active_length]))-start_num] = new_edge_existing
                    self.active_edge.node.children[(self.ord_special(self.string[i]))-start_num] = new_edge_branch
                    # When rule 2: Move through suffix link from active node
                    self.active_node = self.active_node.suffix_link
                # Rule 2 alt
                elif not self.active_node.is_leaf and not same_char and self.active_edge is None:
                    new_edge = Edge(i, self.global_end, True)
                    self.active_node.children[self.ord_special(self.string[i]) - start_num] = new_edge
                    # Move through suffix link
                    self.active_node = self.active_node.suffix_link

                # Rule 3, showstopper trick!
                elif not self.active_node.is_leaf and same_char:
                    show_shopper = True
                    self.active_length += 1
                    # Maintain skip count pointer by breaking
                    break
                j += 1


if __name__ == '__main__':
    a = UkkonenSuffixTree("abcabxabcyab")
    pass