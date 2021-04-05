# Random Tree Generator

Random Tree Generator based on Random Tree Walk, Kruskal and Prim's algorithm for Minimium Spanning Trees.

## Diameter Function
### Run:
To change which file tree you will read, just change the value of `fileTreeName` variable.

You could also create your own tree file following the template bellow:

![image](https://user-images.githubusercontent.com/53497617/113449475-4c74b980-93d4-11eb-98d1-0f2e6da8ebb4.png)

Important: if you can't know the real diameter, please just remove these lines from code:

``  diameter = int(f.readline()) ``

`` G.diameterAssertion = diameter ``

`` assert d == T.diameterAssertion ``

