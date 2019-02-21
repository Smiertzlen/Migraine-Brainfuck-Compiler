# If you want to use this to print your tree, just import this in your script 
# and use 
# tree_pprint.pprint(root_node, name_attr_data, name_attr_left, name_attr_right)
# 

try:
    from queue import Queue
except:
    from Queue import Queue

from copy import deepcopy as deepcopy
import sys

# 'name_attr_data' is the name of the data attribute
# 'name_attr_left' is the name of the left successor node attribute 
# 'name_attr_right' is the name of the right successor node attribute
#
def pprint(external_node, name_attr_data = "data", name_attr_left = "left", name_attr_right = "right"):
    internal_node = convert_tree(external_node, name_attr_data, name_attr_left, name_attr_right)
    internal_node.prettyPrint()
    
def convert_tree(external_node, name_attr_data = "data", name_attr_left = "left", name_attr_right = "right"):
    if not external_node:
        internal_node = None
    else:
        node_data = getattr(external_node, name_attr_data)
        node_left = getattr(external_node, name_attr_left)
        node_right = getattr(external_node, name_attr_right)
        internal_node = Node(node_data, convert_tree(node_left, name_attr_data, name_attr_left, name_attr_right), convert_tree(node_right, name_attr_data, name_attr_left, name_attr_right))
        return internal_node

class Node:
    def __init__(self, data = None, left = None, right = None):
        self.data = data
        self.left = left
        self.right = right

    def getHeight(self):
        return Node.getHeightHelper(self)

    @staticmethod
    def getHeightHelper(node):
        if not node:
            return 0
        else:
            return max(Node.getHeightHelper(node.left), Node.getHeightHelper(node.right)) + 1

    def fillTree(self, height):
        Node.fillTreeHelper(self, height)

    def fillTreeHelper(node, height):
        if height <= 1:
            return
        if node:
            if not node.left: node.left = Node(' ')
            if not node.right: node.right = Node(' ')
            Node.fillTreeHelper(node.left, height - 1)
            Node.fillTreeHelper(node.right, height - 1)


    def prettyPrint(self):
        """
        """
        # get height of tree
        total_layers = self.getHeight()

        tree = deepcopy(self)

        tree.fillTree(total_layers)
        # start a queue for BFS
        queue = Queue()
        # add root to queue
        queue.put(tree) # self = root
        # index for 'generation' or 'layer' of tree
        gen = 1 
        # BFS main
        extra_spaces_next = 1
        while not queue.empty():
            # copy queue
            # 
            copy = Queue()
            while not queue.empty():
                copy.put(queue.get())
            # 
            # end copy queue 

            first_item_in_layer = True
            edges_string = ""
            extra_spaces_next_node = False

            # modified BFS, layer by layer (gen by gen)
            while not copy.empty():

                node = copy.get()

                # -----------------------------
                # init spacing
                spaces_front = pow(2, total_layers - gen + 1) - 2
                spaces_mid   = pow(2, total_layers - gen + 2) - 2
                dash_count   = pow(2, total_layers - gen) - 2
                if dash_count < 0:
                    dash_count = 0
                spaces_mid = spaces_mid - (dash_count*2)
                spaces_front = spaces_front - dash_count
                init_padding = 2
                spaces_front += init_padding
                if first_item_in_layer:
                    edges_string += " " * init_padding
                # ----------------------------->

                # -----------------------------
                # construct edges layer
                edge_sym = "/" if node.left and node.left.data is not " " else " "
                if first_item_in_layer:
                    edges_string += " " * (pow(2, total_layers - gen) - 1) + edge_sym
                else:
                    edges_string += " " * (pow(2, total_layers - gen + 1) + 1) + edge_sym
                edge_sym = "\\" if node.right and node.right.data is not " " else " "
                edges_string += " " * (pow(2, total_layers - gen + 1) - 3) + edge_sym
                # ----------------------------->

                # -----------------------------
                # conditions for dashes
                if node.left and node.left.data == " ":
                    dash_left = " "
                else:
                    dash_left = "_"

                if node.right and node.right.data == " ":
                    dash_right = " "
                else:
                    dash_right = "_"
                # ----------------------------->

                # -----------------------------
                # handle condition for extra spaces when node lengths don't match or are even:
                if extra_spaces_next_node:
                    extra_spaces = extra_spaces_next
                    #print("hier1: "+str(extra_spaces))
                    extra_spaces_next_node = False
                else:
                    extra_spaces = 0
                # ----------------------------->
            
                # -----------------------------
                # account for longer data
                data_length = len(str(node.data))
                if data_length > 1:
                    #print("data: "+str(node.data))
                    if data_length % 2 == 1: # odd
                        if dash_count > 0:
                            dash_count -= int((data_length - 1)/2)
                        else:
                            spaces_mid -= int((data_length - 1)/2)
                            spaces_front -= int((data_length - 1)/2)
                            if data_length is not 1:
                                extra_spaces_next = int((data_length - 1)/2)
                                extra_spaces_next_node = True 
                    else: # even
                        if dash_count > 0:
                            dash_count -= int((data_length)/2) - 1
                            #dash_count += 1
                        else:
                            spaces_mid -= int((data_length)/2)
                            spaces_front -= int((data_length)/2)
                        extra_spaces_next_node = True
                        extra_spaces_next = int((data_length)/2 -1)
                # ----------------------------->
            
                # -----------------------------
                # print node with/without dashes
                if first_item_in_layer:
                    print(" " * spaces_front + dash_left * dash_count + node.data + dash_right * dash_count, end=" ")
                    first_item_in_layer = False
                else:
                    print(" " * (spaces_mid-extra_spaces) + dash_left * dash_count + node.data + dash_right * dash_count, end=" ")
                # ----------------------------->

                if node.left: queue.put(node.left)
                if node.right: queue.put(node.right)

              # print the fun squiggly lines
            if not queue.empty():
                    print("\n" + edges_string)

            # increase layer index
            gen += 1

