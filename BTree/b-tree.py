class Node:
    def __init__(self, t, is_leaf=True):
        self.item = [None for i in range((2 * t))]
        self.child = [None for i in range(2 * t)]
        self.count = 0
        self.is_leaf = is_leaf


class BTree:
    def __init__(self, t):
        self.t = t
        self.root = Node(t)
        self.min_item = t - 1
        self.max_item = (2 * t) - 1

    def search(self, key):
        """
        Unused linear search
        :param key: Key to search
        :return: the key, None if not found
        """
        current = self.root
        while current is not None:
            for i in range(current.count):
                if current.item[i] is None:
                    current = current.child[i]
                    break
                elif current.item[i] == key:
                    return current.item[i]
                elif current.item[i] > key:
                    current = current.child[i]
                    break
                elif i == current.count - 1:
                    current = current.child[i + 1]
                    break
        return None

    def binary_search(self, key, current):
        if current is None:
            return None
        else:
            high = current.count-1
            low = 0
            mid = 0
            while high >= low:
                mid = high + low // 2
                if current.item[mid] == key:
                    return current.item[mid]
                elif current.item[mid] < key:
                    low = mid + 1
                elif current.item[mid] > key:
                    high = mid - 1
            if key < current.item[mid]:
                return self.binary_search(key, current.child[mid])
            else:
                return self.binary_search(key, current.child[mid+1])

    def insert(self, key):
        if self.root.count >= self.max_item:
            median = self.root.count // 2
            median_key = self.root.item[median]

            new_root = Node(self.t, False)
            new_root.item[0] = median_key
            new_root.count += 1

            left_node = Node(self.t, self.root.is_leaf)
            right_node = Node(self.t, self.root.is_leaf)

            for i in range(median):
                left_node.item[i] = self.root.item[i]
                left_node.child[i] = self.root.child[i]
                left_node.count += 1

                right_node.item[i] = self.root.item[i + median + 1]
                right_node.child[i] = self.root.child[i + median + 1]
                right_node.count += 1

            left_node.child[left_node.count] = self.root.child[median]
            right_node.child[right_node.count] = self.root.child[(2 * self.t) - 1]

            new_root.child[0] = left_node
            new_root.child[1] = right_node
            old_root = self.root
            self.root = new_root

            # Delete via unreferencing for garbage collector
            old_root.child = None
            old_root.key = None
            del old_root

        self._insert_aux(key, self.root)

    def _insert_aux(self, key, current):
        if current.is_leaf:
            pos = 0
            while pos < current.count and current.item[pos] is not None and \
                    key > current.item[pos]:
                pos += 1

            # If already exists, dont insert
            if current.item[pos] == key:
                return

            for i in range(current.count, pos, -1):
                current.item[i] = current.item[i - 1]

            current.item[pos] = key
            current.count += 1
        else:
            pos = 0
            while pos < current.count and key > current.item[pos]:
                pos += 1
            next_node = current.child[pos]
            if next_node.count >= self.max_item:
                median = next_node.count // 2
                median_key = next_node.item[median]

                left_node = next_node
                right_node = Node(self.t, next_node.is_leaf)
                for i in range(median + 1, next_node.count):
                    right_node.item[i - median - 1] = left_node.item[i]
                    right_node.child[i - median - 1] = left_node.child[i]
                    left_node.child[i] = None
                    left_node.item[i] = None
                    right_node.count += 1
                right_node.child[right_node.count] = left_node.child[(self.t * 2) - 1]
                left_node.child[(self.t * 2) - 1] = None
                left_node.item[median] = None
                left_node.count = median - 1

                # Shift item for new key
                for i in range(current.count, pos, -1):
                    current.item[i] = current.item[i - 1]
                for i in range(current.count + 1, pos, -1):
                    current.child[i] = current.child[i - 1]

                current.item[pos] = median_key
                current.child[pos] = left_node
                current.child[pos + 1] = right_node
                current.count += 1
                current.is_leaf = False
                left_node.count = median
                if key < median_key:
                    next_node = left_node
                else:
                    next_node = right_node
            self._insert_aux(key, next_node)

    def find_predecessor_successor(self, current_node: Node, predecessor=True):
        if current_node.is_leaf:
            if predecessor:
                return current_node.item[current_node.count - 1]
            else:
                return current_node.item[0]
        else:
            if predecessor:
                return self.find_predecessor_successor(current_node.child[current_node.count], predecessor)
            else:
                return self.find_predecessor_successor(current_node.child[0])

    def merge_shift(self, current, pos, next_node, for_delete=False):
        """
        Merge both left, parent and right
        or shift
        """
        left_sibling = None
        left_sibling_min = True
        right_sibling = None
        right_sibling_min = True
        # get sibling
        if for_delete:
            left_sibling = current.child[pos]
            right_sibling = current.child[pos + 1]
            left_sibling_min = left_sibling.count == self.min_item
            right_sibling_min = right_sibling.count == self.min_item
        else:
            if pos > 0:
                left_sibling = current.child[pos - 1]
                left_sibling_min = left_sibling.count == self.min_item
            if pos <= current.count - 1:
                right_sibling = current.child[pos + 1]
                right_sibling_min = right_sibling.count == self.min_item

        # If both are min, merge
        if left_sibling_min and right_sibling_min:
            merge_sibling = right_sibling
            if left_sibling is None and right_sibling is None:
                raise Exception("Both siblings are none")
            elif left_sibling is None:
                merge_sibling = right_sibling
            elif right_sibling is None:
                merge_sibling = next_node
                next_node = left_sibling

            if current.item[pos] is None:
                next_node.item[next_node.count] = current.item[pos - 1]
            else:
                next_node.item[next_node.count] = current.item[pos]
                current.item[pos] = None
            next_node.count += 1

            for i in range(merge_sibling.count):
                next_node.item[next_node.count + i] = merge_sibling.item[i]
                next_node.child[next_node.count + i] = merge_sibling.child[i]

            next_node.count += merge_sibling.count
            next_node.child[next_node.count] = merge_sibling.child[merge_sibling.count]
            # shift current
            current.count -= 1
            for i in range(pos, current.count):
                current.item[i] = current.item[i + 1]
            current.item[current.count] = None
            for i in range(pos + 1, current.count + 1):
                current.child[i] = current.child[i + 1]
            current.child[current.count + 1] = None

            if current == self.root and self.root.count == 0:
                self.root = next_node

            # current.child[pos] = next_node
        else:
            # Shift successor of left to right
            if left_sibling is not None and not left_sibling_min:
                # Take successor of left
                successor = left_sibling.item[left_sibling.count - 1]
                successor_right_child = left_sibling.child[left_sibling.count]
                if pos > 0:
                    temp_pos = pos - 1
                else:
                    temp_pos = pos
                if current.item[temp_pos] is None:
                    temp_pos = pos - 1
                shift_down_item = current.item[temp_pos]

                # remove the stuff from left
                left_sibling.item[left_sibling.count - 1] = None
                left_sibling.child[left_sibling.count] = None
                left_sibling.count -= 1
                current.item[temp_pos] = successor

                # make space for shift down
                for i in range(next_node.count, 0, -1):
                    next_node.item[i] = next_node.item[i - 1]
                next_node.item[0] = shift_down_item
                for i in range(next_node.count + 1, -1, -1):
                    next_node.child[i] = next_node.child[i - 1]
                next_node.child[0] = successor_right_child
                next_node.count += 1
            # shift predecessor of right to left
            elif right_sibling is not None and not right_sibling_min:
                # Take predecessor of right
                predecessor = right_sibling.item[0]
                predecessor_left_child = right_sibling.child[0]
                temp_pos = pos
                if current.item[temp_pos] is None:
                    temp_pos = pos - 1
                shift_down_item = current.item[temp_pos]

                right_sibling.count -= 1
                # shift right sibling and remove prev
                for i in range(right_sibling.count):
                    right_sibling.item[i] = right_sibling.item[i + 1]
                for i in range(right_sibling.count + 1):
                    right_sibling.child[i] = right_sibling.child[i + 1]
                right_sibling.item[right_sibling.count] = None
                right_sibling.child[right_sibling.count + 1] = None

                current.item[temp_pos] = predecessor

                # put shift down
                next_node.item[next_node.count] = shift_down_item
                next_node.child[next_node.count + 1] = predecessor_left_child
                next_node.count += 1
        return next_node

    def delete(self, key):
        self._delete_aux(key, self.root)

    def _delete_aux(self, key, current):
        pos = 0
        while pos < current.count and key > current.item[pos]:
            pos += 1

        if current.item[pos] == key:
            if current.is_leaf:
                # Since is leaf, we not shifting child
                current.count -= 1
                for i in range(pos, current.count):
                    current.item[i] = current.item[i + 1]
                current.item[current.count] = None
                return
            else:
                # Rotate...
                # if you're not a leaf
                # you will always have child
                left_child = current.child[pos]
                right_child = current.child[pos + 1]


                new_key = key
                if left_child.count >= self.t:
                    new_key = self.find_predecessor_successor(left_child, False)
                    current.item[pos] = new_key
                    next_node = left_child
                elif right_child.count >= self.t:
                    new_key = self.find_predecessor_successor(right_child, False)
                    current.item[pos] = new_key
                    next_node = right_child
                # Both left and right child same amount of item
                elif left_child.count == self.min_item and right_child.count == self.min_item:
                    # merge this current item, with left and right
                    # then go in and delete
                    next_node = left_child
                    self.merge_shift(current, pos, next_node, True)

                self._delete_aux(new_key, next_node)
                return

        if current.child[pos] is None:
            return  # Not found, just stop

        next_node = current.child[pos]
        # Cannot enter if is minimum item
        if next_node.count == self.min_item:
            next_node = self.merge_shift(current, pos, next_node)
        self._delete_aux(key, next_node)


def in_order_traverse(node, file):
    for i in range(node.count):
        if not node.is_leaf:
            in_order_traverse(node.child[i], file)
        file.write("".join([node.item[i], "\n"]))
    if not node.is_leaf:
        in_order_traverse(node.child[node.count], file)