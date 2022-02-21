# import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
iris = load_iris()

class Node:


    def __init__(self, X=None, y=None, depth=0, gini=10, feature_index=0, threshold=0, left=None, right=None, value=None):
        self.X = X
        self.y = y
        self.depth = depth
        self.gini = gini
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        self.indent = " "

    def __str__(self):
        return f"{self.depth*'  '}{self.gini}, {self.depth}, {self.feature_index}, {self.threshold}"

class MyDecisionTreeClassifier:

    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.root = None
        self.value = None
    def gini(self, y):
        """
        classes = [[0],[1],[2]]
        A Gini score gives an idea of how good a split is by how mixed the
        classes are in the two groups created by the split.

        A perfect separation results in a Gini score of 0,
        whereas the worst case split that results in 50/50
        classes in each group result in a Gini score of 0.5
        (for a 2 class problem).
        """
        gini = 0
        all = len(y)
        for cls in range(3):
            sum_classes = []
            for i in range(all):
                clas = int(y[i])
                if clas == cls:
                    sum_classes.append(clas)
            p = len(sum_classes) / all
            gini += p ** 2
        gini = 1 - gini
        return gini


    def split_data(self, X, y):
        IG = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        num_features = iris.feature_names
        for feature_index in range(len(num_features)):
            possible_thresholds = sorted(np.unique(X[:, feature_index]), reverse=True)
            for threshold in possible_thresholds:
                data_left = []
                data_right = []
                y_left = []
                y_right = []
                for i in range(len(X)):
                    pi = X[i, feature_index]
                    if pi <= threshold:
                        data_left.append(X[i])
                        y_left.append(y[i])
                    else:
                        data_right.append(X[i])
                        y_right.append(y[i])
                data_parent = X
                data_left = np.array(data_left)
                data_right = np.array(data_right)
                y_left = np.array(y_left)
                y_right = np.array(y_right)
                if len(data_left) > 0 and len(data_right) > 0:
                    gini_p = self.gini(y)
                    gini_l = self.gini(y_left)
                    gini_r = self.gini(y_right)
                    weight_l = len(data_left) / len(data_parent)
                    weight_r = len(data_right) / len(data_parent)
                    ig = gini_p - (weight_l * gini_l + weight_r * gini_r)
                    if ig > IG[0]:
                        IG[0] = ig
                        IG[1] = data_left
                        IG[2] = data_right
                        IG[3] = data_parent
                        IG[4] = threshold
                        IG[5] = feature_index
                        IG[6] = y_left
                        IG[7] = y_right
                        IG[8] = gini_p
        return IG

    def build_tree(self, node):
        X = node.X
        y = node.y
        depth = node.depth
        if node != None:
            if depth <= self.max_depth:
                split = self.split_data(X, y)
                if split[8] == 0:
                    node.value = f"A leaf with {split[3]} flowers, threshold = {split[4]}, feature = {split[5]}"
                if split[0] > 0:
                    node.left = self.build_tree(Node(X=split[1], y=split[6], depth=depth + 1, gini=split[0], feature_index=split[5], threshold=split[4]))
                    print(node.left)
                    node.right = self.build_tree(Node(X=split[2], y=split[7], depth=depth + 1, gini=split[0], feature_index=split[5], threshold=split[4]))
                    print(node.right)
                    return node


    def fit(self, tree):
        ''' function to train the tree '''
        if not tree:
            tree = self.root
        if tree.value is not None:
            print(tree.value)
        tr = self.split_data(iris.data, iris.target)
        tree_nd_class = Node(tr[3], iris.target, 0, tr[0], tr[5], tr[4], left=None, right=None)
        self.root = self.build_tree(tree_nd_class)

if __name__ == "__main__":
    my_tree = MyDecisionTreeClassifier(10)
    tree = my_tree.fit(my_tree)