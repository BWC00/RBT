def createTreeItem(key,val):
    newItem = RedBlackTree()
    newItem.root = val
    newItem.searchKey = key
    return newItem

class RedBlackTree:
    def __init__(self):
        """
        Maakt een lege Rood Zwart Boom instantie aan.
        - geen invoerparameters
        - geen uitvoerparameters
        - geen preconditie
        postconditie:
            lege rood zwart boom object is gemaakt
        """
        self.left_child = None
        self.right_child = None
        self.root = None
        self.searchKey = None
        self.parent = None
        self.red = False

    def isEmpty(self):
        """
        Bepaalt ofdat de boom leeg is.
        - geen invoerparameters
        - geen uitvoerparameters
        - geen preconditie
        - geen postconditie
        """
        return self.root is None

    def determine_rotation_side(self):
        """
        Bepaalt de richting van de rotatie: boven, rechts of links.
        - geen invoerparameters
        - geen uitvoerparameters
        - geen preconditie
        - geen postconditie
        """
        if self.red and self.parent:
            if self.left_child and self.left_child.red and self.parent.left_child==self:
            #     A   A = zwart, B = rood, C = rood, geval x
            #    /
            #   B
            #  /
            # C
                return self.rotate(False)
            elif self.right_child and self.right_child.red and self.parent.right_child==self:
            # A       A = zwart, B = rood, C = rood, geval y
            #  \
            #   B
            #    \
            #     C
                return self.rotate(False)
            else:
            #  A      A = zwart, B = rood, C = rood, geval z
            #   \
            #    B (of gespiegeld)
            #   /
            #  C
                return self.rotate(True)

    def rotate(self,rotate_up):
        """
        Roteert de boom naar de gepaste richting.
        invoerparameters:
            rotate_up (bool): zegt ofdat de rotatie naar boven moet zijn of niet
        - geen uitvoerparameters
        - geen preconditie
        - geen postconditie
        """
        oldroot = RedBlackTree() #root veranderd, wordt in een aparte node gezet zodat het slechts nodig is om de root (value) en key te verplaatsen van nodes
        oldroot.root = self.parent.root
        oldroot.searchKey = self.parent.searchKey
        oldroot.parent = self.parent
        oldroot.red = True

        if rotate_up: #geval z
            if self.right_child and self.right_child.red:
                self.parent.root = self.right_child.root #het is enkel voldoende om de items te swappen van nodes (een node wordt herkent door zijn value en key)
                self.parent.searchKey = self.right_child.searchKey
                temp = self.parent.right_child
                self.parent.right_child = oldroot
                oldroot.right_child = temp
                if oldroot.right_child:
                    oldroot.right_child.parent = oldroot
                oldroot.left_child = self.right_child.right_child
                if self.right_child.right_child:
                    self.right_child.right_child.red = False
                    self.right_child.right_child.parent = oldroot
                self.right_child = self.right_child.left_child
                if self.right_child:
                    self.right_child.red = False
                    self.right_child.parent = self

            else: #geval z maar gespiegeld
                self.parent.root = self.left_child.root
                self.parent.searchKey = self.left_child.searchKey
                temp = self.parent.left_child
                self.parent.left_child = oldroot
                oldroot.left_child = temp
                if oldroot.left_child:
                    oldroot.left_child.parent = oldroot
                oldroot.right_child = self.left_child.left_child
                if self.left_child.left_child:
                    self.left_child.left_child.red = False
                    self.left_child.left_child.parent = oldroot
                self.left_child = self.left_child.right_child
                if self.left_child:
                    self.left_child.red = False
                    self.left_child.parent = self

        else: #de resterende 2 gevallen
            self.parent.root = self.root
            self.parent.searchKey = self.searchKey
            if self.left_child and self.left_child.red: #geval x
                self.root = self.left_child.root
                self.searchKey = self.left_child.searchKey
                temp = self.parent.right_child
                self.parent.right_child = oldroot
                oldroot.right_child = temp
                if oldroot.right_child:
                    oldroot.right_child.parent = oldroot
                oldroot.left_child = self.right_child
                if self.right_child:
                    self.right_child.parent = oldroot
                self.right_child = self.left_child.right_child
                if self.right_child:
                    self.right_child.parent = self
                self.left_child = self.left_child.left_child
                if self.left_child:
                    self.left_child.parent = self

            else: #geval y (gespiegeld)
                self.root = self.right_child.root
                self.searchKey = self.right_child.searchKey
                temp = self.parent.left_child
                self.parent.left_child = oldroot
                oldroot.left_child = temp
                if oldroot.left_child:
                    oldroot.left_child.parent = oldroot
                oldroot.right_child = self.left_child
                if self.left_child:
                    self.left_child.parent = oldroot
                self.left_child = self.right_child.left_child
                if self.left_child:
                    self.left_child.parent = self
                self.right_child = self.right_child.right_child
                if self.right_child:
                    self.right_child.parent = self

    def split(self):
        """
        Bepaalt de richting van de rotatie: boven, rechts of links.
        - geen invoerparameters
        - geen uitvoerparameters
        - geen preconditie
        - geen postconditie
        """
        self.left_child.red = False #bij een split worden de kinderen altijd zwart
        self.right_child.red = False

        if self.parent: #indien de parent bestaat -> node wordt rood (wordt toegevoegd aan de parent)
            self.red = True
            self.parent.determine_rotation_side() #bepaal ofdat er roteert moet worden en de rotatie richting

    def insertItem(self,newItem):
        """
        Insert een item (node) in de boom.
        invoerparameters:
            newItem (RedBlackTree): object van type RedBlackTree dat insert moet worden
        uitvoerparameters:
            succes (bool): True indien de operatie gelukt is
        preconditie:
            newItem moet van type "RedBlackTree" zijn
        postconditie:
            newItem met bepaalde key is toegevoegd in de boom
        """
        if self.isEmpty(): #indien de boom leeg is, kopieer de value en key van newItem naar self.root en self.searchKey
            self.root = newItem.root
            self.searchKey = newItem.searchKey
            return True

        else: #indien de boom niet leeg is
            if not(self.red): #het is enkel nuttig om bij zwarte nodes te checken ofdat ze vol zijn (rode nodes zitte in dezelfde knoop)
                if self.is4Node(): #enkel splitten indien het een 4-knoop is
                    self.split() #split

            if newItem.searchKey < self.searchKey: #naar links indien de searchKey van newItem kleiner is dan self.searchKey (in huidige knoop)
                if self.left_child:
                    return self.left_child.insertItem(newItem)

                else: #indien de linkerkind niet bestaat
                    self.left_child = newItem #voeg newItem aan de boom
                    self.left_child.parent = self
                    self.left_child.red = True
                    self.determine_rotation_side() #bepaal ofdat er een rotatie nodig is na het inserten
                    return True

            else: #naar rechts indien de searchKey van newItem groter is dan self.searchKey (in huidige knoop)
                if self.right_child:
                    return self.right_child.insertItem(newItem)

                else: #indien de reckterkind niet bestaat
                    self.right_child = newItem #voeg newItem aan de boom
                    self.right_child.parent = self
                    self.right_child.red = True
                    self.determine_rotation_side() #bepaal ofdat er een rotatie nodig is na het inserten
                    return True

    def retrieveItem(self,searchKey):
        """
        verkrjgt de gezochte item met key=searchKey
        invoerparameters:
            searchKey (int): key van naar te zoeken item
        uitvoerparameters:
            succes (bool): True indien de item gevonden is anders false
        preconditie:
            searchKey >= 0
        Postconditie:
            item wordt verkregen indien succes=True
        """
        if self.searchKey==searchKey:
            return (self.root,True)
        else:
            if searchKey < self.searchKey:
                if self.left_child:
                    return self.left_child.retrieveItem(searchKey)
                else:
                    return (None,False)
            else:
                if self.right_child:
                    return self.right_child.retrieveItem(searchKey)
                else:
                    return (None,False)

    def inorderTraverse(self,func):
        """
        inorder traversal van de boom (gelijkaardig aan BST).
        invoerparameters:
            func(functie): functie dat je op elk node wilt uitvoeren
        - geen uitvoerparameters
        preconditie:
            func moet een functie zjn
        postconditie:
            voert func om elke node uit
        """
        if self.left_child: #indien een linkerkind bestaat
            self.left_child.inorderTraverse(func) #ga naar links

        if not self.root is None:
            func(self.root) #voer func uit op de huidige node

        if self.right_child: #indien een rechterkind bestaat
            self.right_child.inorderTraverse(func) #ga naar rechts

    def inorderYielding(self):
        if self.left_child:
            yield from self.left_child.inorderYielding()
        yield self.root
        if self.right_child:
            yield from self.right_child.inorderYielding()

    def inorderSuccesor(self,goRight=True): #goRight = 1 keer naar rechts en dan de hele tijd naar links
        """
        Vindt inordersuccesor van de huidige node.
        - geen invoerparameters
        uitvoerparameters:
            node (RedBlackTree): de gevonden node
        - geen preconditie
        - geen postconditie
        """
        if goRight:
            return self.right_child.inorderSuccesor(goRight=False)
        if not(self.left_child):
            return self
        return self.left_child.inorderSuccesor(goRight=False)

    def save(self):
        """
        zet huidige rood zwart boom om in een dictionary voorstelling
        - geen invoerparameters
        uitvoerparameters:
            dict: dict voorstelling van rood zwart boom
        - geen preconditie
        - geen postconditie
        """
        if not(self.left_child) and not(self.right_child):
            if self.root != None:
                return {'root':self.searchKey,'color':['black','red'][self.red]}
            else:
                return None
        return {'root':self.searchKey,'color':['black','red'][self.red],'children':[None if not(self.left_child) else self.left_child.save(), None if not(self.right_child) else self.right_child.save()]}

    def load(self,d,clear=True): #clear: maak de boom 1 keer leeg
        """
        laadt van een dict de rood zwart boom.
        invoerparameters:
            d (dict): dict voorstelling van rood zwart boom
        - geen uitvoerparameters
        preconditie:
            d moet een rood zwart boom voorstellen als een dictionary
        postconditie:
            boom is geladen als een object
        """
        if clear:
            self.__init__()
            if not(d): return
        self.root = d.get("root",None)
        self.searchKey = d.get("root",None)
        self.red = d.get("color","s")=="red"

        if d.get("children",0):
            if d["children"][0]:
                self.left_child = RedBlackTree()
                self.left_child.parent = self
                self.left_child.load(d["children"][0],clear=False)

            if d["children"][1]:
                self.right_child = RedBlackTree()
                self.right_child.parent = self
                self.right_child.load(d["children"][1],clear=False)

    def make3Node4Node(self):
        """
        merged een node met een ouder en gepaste sibling
        - geen invoerparameters
        - geen uitvoerparameters
        - geen preconditie
        - geen postconditie
        """
        test = self.check_siblings() #check ofdat er siblings zijn die kunnen delen
        if not(test[0]): #test=False; indien er geen siblings zijn die kunnen delen
            if test[1]==1: #geval 1: huidige knoop (B) en sibling (C) hebben dezelfde ouder (A)
            #     A  geval 1
            #    / \
            #   B   C
                self.parent.red = False #kleuren veranderen is voldoende, A -> zwart, B -> rood, C -> rood
                self.parent.left_child.red = True
                self.parent.right_child.red = True

            else: #geval 2: C en D zijn siblings van elkaar maar hebben niet dezelfde ouder
            #     A  geval 2, B is rood (A en B vormen een 3 knoop)
            #   r/ \b
            #   B   C
            # b/ \b
            # E   D


            # Move values of A and B to preserve root
            #
            #      B
            #    r/ \b
            #    A   C
            #  b/ \b
            #  E   D


            #    B
            #   / \
            #  E   A
            #     / \
            #    D   C
            #
            # Rotatie dus

                #### Rotatie I guess
                if self.parent.right_child==self: #zit in de rechterkind van de ouder (zit in C)

                    A = self.parent
                    B = A.left_child
                    C = A.right_child
                    D = B.right_child
                    E = B.left_child

                    assert C is self

                    if A.parent: #indien A niet de root is van de boom
                        if A.parent.left_child == A: #indien A in de linkerkind van zijn ouder zit
                            A.parent.left_child = A.left_child #B wordt de linkerkind van de ouder van A
                        else:
                            A.parent.right_child = A.left_child #B wordt de rechterkind van de ouder van A
                    A.left_child.parent = A.parent

                    if A.left_child:
                        A.left_child.red = False

                    A.left_child = D #linkerkind van A wordt D
                    if A.left_child:
                        D.parent = A #ouder van D wordt A

                    A.parent = B #ouder van A wordt B
                    B.right_child = A #rechterkind van B wordt A
                    C.red = True #C wordt rood bij een merge

                    if D:
                        D.red = True #D wordt rood bij een merge

                    """
                    if self.parent.parent: #indien A niet de root is van de boom
                        if self.parent.parent.left_child==self.parent: #indien A in de linkerkind van zijn ouder zit
                            self.parent.parent.left_child = self.parent.left_child #B wordt de linkerkind van de ouder van A
                        else:
                            self.parent.parent.right_child = self.parent.left_child #B wordt de rechterkind van de ouder van A

                    self.parent.left_child.parent = self.parent.parent
                    if self.parent.left_child:
                        self.parent.left_child.red = False

                    temp = self.parent.left_child #deelboom BED behouden

                    self.parent.left_child = self.parent.left_child.right_child #linkerkind van A wordt D
                    if self.parent.left_child:
                        self.parent.left_child.parent = self.parent #ouder van D wordt A

                    self.parent.parent = temp #ouder van A wordt B
                    self.parent.parent.right_child = self.parent #rechterkind van B wordt A
                    self.red = True #C wordt rood bij een merge

                    if self.parent.left_child:
                        self.parent.left_child.red = True #D wordt rood bij een merge
                    """

                else: #zit in de linkerkind van de ouder (gespiegeld ten opzichte van de bovenste situatie)
                    """
                    A = self.parent
                    B = A.right_child
                    C = A.left_child
                    D = B.left_child
                    E = B.right_child

                    if A.parent:
                        if A.parent.left_child==A:
                            A.parent.left_child = A.right_child
                        else:
                            A.parent.right_child = A.right_child
                    A.right_child.parent = A.parent

                    if A.right_child:
                        A.right_child.red = False

                    temp = A.right_child

                    A.right_child = D
                    if A.right_child:
                        A.parent = A

                    A.parent = B
                    B.left_child = A
                    C.red = True

                    if D:
                        D.red = True
                    """
                    if self.parent.parent:
                        if self.parent.parent.left_child==self.parent:
                            self.parent.parent.left_child = self.parent.right_child
                        else:
                            self.parent.parent.right_child = self.parent.right_child
                    self.parent.right_child.parent = self.parent.parent
                    if self.parent.right_child:
                        self.parent.right_child.red = False
                    temp = self.parent.right_child
                    self.parent.right_child = self.parent.right_child.left_child
                    if self.parent.right_child:
                        self.parent.right_child.parent = self.parent
                    self.parent.parent = temp
                    self.parent.parent.left_child = self.parent
                    self.red = True
                    if self.parent.right_child:
                        self.parent.right_child.red = True

    def is2Node(self):
        """
        Bepaalt of een knoop een 2-knoop is
        - geen invoerparameters
        uitvoerparameters:
            succes (bool): True indien de knoop een 2-knoop is anders false
        - geen preconditie
        - geen postconditie
        """
        if self.red:
            return self.parent.is2Node() #ga naar de parent (dit is om ervoor te zorgen dat we niet naar boven ook moeten kijken ofdat de huidige knoop een 2 knoop is)
        if (self.left_child and self.left_child.red) or (self.right_child and self.right_child.red):
            return False
        return True

    def is3Node(self):
        """
        Bepaalt of een knoop een 3-knoop is
        - geen invoerparameters
        uitvoerparameters:
            succes (bool): True indien de knoop een 3-knoop is anders false
        - geen preconditie
        - geen postconditie
        """
        if self.red:
            return self.parent.is3Node() #ga naar de parent (dit is om ervoor te zorgen dat we niet naar boven ook moeten kijken ofdat de huidige knoop een 3 knoop is)
        if (self.left_child and self.left_child.red and (not(self.right_child) or not(self.right_child.red))) or (self.right_child and self.right_child.red and (not(self.left_child) or not(self.left_child.red))):
            return True
        return False

    def is4Node(self):
        """
        Bepaalt of een knoop een 4-knoop is
        - geen invoerparameters
        uitvoerparameters:
            succes (bool): True indien de knoop een 4-knoop is anders false
        - geen preconditie
        - geen postconditie
        """
        if self.red:
            return self.parent.is4Node() #ga naar de parent (dit is om ervoor te zorgen dat we niet naar boven ook moeten kijken ofdat de huidige knoop een 4 knoop is)
        if self.left_child and self.left_child.red and self.right_child and self.right_child.red:
            return True
        return False

    def distribute(self,case):
        """
        herverdeelt de items tussen een 2 knoop en een sibling met genoeg items
        invoerparameters:
            case (int): geeft aan in welk geval we zitten bij een redistribute
        uitvoerparameters:
            succes (bool,bool): True,True bij succes
        - geen preconditie
        postconditie:
            nodes worden herverdeeld
        """
        new_tree = RedBlackTree() #de ouder wordt altijd als een nieuwe knoop toegevoegd aan de 2 knoop
        new_tree.red = True

        if self.parent.right_child==self: #indien we in de rechterkind van de ouder zitten
            if case==1 or case==2:
            #     A  case=1, we zitten in C en B is de sibling die kan delen
            #    / \
            #   B   C
            #
            #     A  case=2, we zitten in C en D is de sibling die kan delen (B is rood, A en B vormen een 3 knoop)
            #    / \
            #   B   C
            #  / \
            # E   D
                
                new_tree.root = self.parent.root #in beide cases komt de ouder A bij de 2 knoop C als een nieuwe node terecht
                new_tree.searchKey = self.parent.searchKey
                new_tree.parent = self #ouder van A wordt C
                temp_tree = self.left_child
                self.left_child = new_tree #linkerkind van C wordt A
                new_tree.right_child = temp_tree
                if new_tree.right_child:
                    new_tree.right_child.parent = new_tree

                if case==1:
                    if self.parent.left_child.right_child and self.parent.left_child.right_child.red: #indien B nog een rechterkind heeft, moeten we die verwisselen met de parent C
                        self.parent.root = self.parent.left_child.right_child.root
                        self.parent.searchKey = self.parent.left_child.right_child.searchKey
                        new_tree.left_child = self.parent.left_child.right_child.right_child
                        if new_tree.left_child:
                            new_tree.left_child.parent = new_tree
                        self.parent.left_child.right_child = self.parent.left_child.right_child.left_child
                        if self.parent.left_child.right_child:
                            self.parent.left_child.right_child.parent = self.parent.left_child
                            self.parent.left_child.right_child.red = False
                    else: #indien B geen rechterkind heeft, moeten we B verwisselen met de parent van C
                        new_tree.left_child = self.parent.left_child.right_child
                        if new_tree.left_child:
                            new_tree.left_child.parent = new_tree
                        self.parent.root = self.parent.left_child.root
                        self.parent.searchKey = self.parent.left_child.searchKey
                        self.parent.left_child = self.parent.left_child.left_child
                        self.parent.left_child.parent = self.parent
                        self.parent.left_child.red = False

                else: #case=2
                    if self.parent.left_child.right_child.right_child and self.parent.left_child.right_child.right_child.red: #indien D nog een rechterkind heeft, moeten we die verwisselen met de parent
                        self.parent.root = self.parent.left_child.right_child.right_child.root
                        self.parent.searchKey = self.parent.left_child.right_child.right_child.searchKey
                        new_tree.left_child = self.parent.left_child.right_child.right_child.right_child
                        if new_tree.left_child:
                            new_tree.left_child.parent = new_tree
                        self.parent.left_child.right_child.right_child = self.parent.left_child.right_child.right_child.left_child
                        if self.parent.left_child.right_child.right_child:
                            self.parent.left_child.right_child.right_child.parent = self.parent.left_child.right_child

                    else: #indien D geen reckterkind heeft, moeten we D verwisselen met de parent
                        new_tree.left_child = self.parent.left_child.right_child.right_child
                        if new_tree.left_child:
                            new_tree.left_child.parent = new_tree
                        self.parent.root = self.parent.left_child.right_child.root
                        self.parent.searchKey = self.parent.left_child.right_child.searchKey
                        self.parent.left_child.right_child = self.parent.left_child.right_child.left_child
                        self.parent.left_child.right_child.parent = self.parent.left_child
                        self.parent.left_child.right_child.red = False

            else: #case=3 of case=4
            #     A  case=3, we zitten in D en C is de sibling die kan delen
            #    / \
            #   B   C
            #  / \
            # E   D
            #
            #     A  case=4, we zitten in D en F is de sibling die kan delen (B en C zjn rood en A is zwart en vormen een 4 knoop)
            #    / \
            #   B   C
            #  / \ / \
            # E  D F  Y
                new_tree.root = self.parent.parent.root #in beide cases komt de ouder A bij de knoop D als een nieuwe node terecht
                new_tree.searchKey = self.parent.parent.searchKey
                new_tree.parent = self #ouder van A wordt D
                temp_tree = self.right_child #behoudt rechterkind van D
                self.right_child = new_tree #rechterkind van D wordt A
                new_tree.left_child = temp_tree #linkerkind van A wordt de originele rechterkind van D
                if new_tree.left_child: #indien de originele rechterkind van D niet None is verander zijn parent
                    new_tree.left_child.parent = new_tree

                if case==3:
                    if self.parent.parent.right_child.left_child and self.parent.parent.right_child.left_child.red: #indien C nog een linkerkind heeft, moeten we die verwisselen met de parent A
                        self.parent.parent.root = self.parent.parent.right_child.left_child.root
                        self.parent.parent.searchKey = self.parent.parent.right_child.left_child.searchKey
                        new_tree.right_child = self.parent.parent.right_child.left_child.left_child
                        if new_tree.right_child:
                            new_tree.right_child.parent = new_tree
                        self.parent.parent.right_child.left_child = self.parent.parent.right_child.left_child.right_child
                        if self.parent.parent.right_child.left_child:
                            self.parent.parent.right_child.left_child.parent = self.parent.parent.right_child

                    else: #indien C geen linkerkind heeft, moeten we C verwisselen met de parent A
                        new_tree.right_child = self.parent.parent.right_child.left_child
                        if new_tree.right_child:
                            new_tree.right_child.parent = new_tree
                        self.parent.parent.root = self.parent.parent.right_child.root
                        self.parent.parent.searchKey = self.parent.parent.right_child.searchKey
                        self.parent.parent.right_child = self.parent.parent.right_child.right_child
                        self.parent.parent.right_child.parent = self.parent.parent
                        self.parent.parent.right_child.red = False

                else: #case=4
                    if self.parent.parent.right_child.left_child.left_child and self.parent.parent.right_child.left_child.left_child.red: #indien F nog een linkerkind heeft, moeten we die verwisselen met de parent A
                        self.parent.parent.root = self.parent.parent.right_child.left_child.left_child.root
                        self.parent.parent.searchKey = self.parent.parent.right_child.left_child.left_child.searchKey
                        new_tree.right_child = self.parent.parent.right_child.left_child.left_child.left_child
                        if new_tree.right_child:
                            new_tree.right_child.parent = new_tree
                        self.parent.parent.right_child.left_child.left_child = self.parent.parent.right_child.left_child.left_child.right_child
                        if self.parent.parent.right_child.left_child.left_child:
                            self.parent.parent.right_child.left_child.left_child.parent = self.parent.parent.right_child.left_child

                    else: #indien F geen linkerkind heeft, moeten we F verwisselen met de parent A
                        new_tree.right_child = self.parent.parent.right_child.left_child.left_child
                        if new_tree.right_child:
                            new_tree.right_child.parent = new_tree
                        self.parent.parent.root = self.parent.parent.right_child.left_child.root
                        self.parent.parent.searchKey = self.parent.parent.right_child.left_child.searchKey
                        self.parent.parent.right_child.left_child = self.parent.parent.right_child.left_child.right_child
                        self.parent.parent.right_child.left_child.parent = self.parent.parent.right_child
                        self.parent.parent.right_child.left_child.red = False

        else: #spiegeling ten opzichte van geval waarbij self.parent.rechterkind==self
            if case==1 or case==2:
                new_tree.root = self.parent.root
                new_tree.searchKey = self.parent.searchKey
                new_tree.parent = self
                temp_tree = self.right_child
                self.right_child = new_tree
                new_tree.left_child = temp_tree
                if new_tree.left_child:
                    new_tree.left_child.parent = new_tree

                if case==1:
                    if self.parent.right_child.left_child and self.parent.right_child.left_child.red:
                        self.parent.root = self.parent.right_child.left_child.root
                        self.parent.searchKey = self.parent.right_child.left_child.searchKey
                        new_tree.right_child = self.parent.right_child.left_child.left_child
                        if new_tree.right_child:
                            new_tree.right_child.parent = new_tree
                        self.parent.right_child.left_child = self.parent.right_child.left_child.right_child
                        if self.parent.right_child.left_child:
                            self.parent.right_child.left_child.parent = self.parent.right_child
                            self.parent.right_child.left_child.red = False

                    else:
                        new_tree.right_child = self.parent.right_child.left_child
                        if new_tree.right_child:
                            new_tree.right_child.parent = new_tree
                        self.parent.root = self.parent.right_child.root
                        self.parent.searchKey = self.parent.right_child.searchKey
                        self.parent.right_child = self.parent.right_child.right_child
                        self.parent.right_child.parent = self.parent
                        self.parent.right_child.red = False

                else:
                    if self.parent.right_child.left_child.left_child and self.parent.right_child.left_child.left_child.red:
                        self.parent.root = self.parent.right_child.left_child.left_child.root
                        self.parent.searchKey = self.parent.right_child.left_child.left_child.searchKey
                        new_tree.right_child = self.parent.right_child.left_child.left_child.left_child
                        if new_tree.right_child:
                            new_tree.right_child.parent = new_tree
                        self.parent.right_child.left_child.left_child = self.parent.right_child.left_child.left_child.right_child
                        if self.parent.right_child.left_child.left_child:
                            self.parent.right_child.left_child.left_child.parent = self.parent.right_child.left_child

                    else:
                        new_tree.right_child = self.parent.right_child.left_child.left_child
                        if new_tree.right_child:
                            new_tree.right_child.parent = new_tree
                        self.parent.root = self.parent.right_child.left_child.root
                        self.parent.searchKey = self.parent.right_child.left_child.searchKey
                        self.parent.right_child.left_child = self.parent.right_child.left_child.right_child
                        self.parent.right_child.left_child.parent = self.parent.right_child
                        self.parent.right_child.left_child.red = False

            else:
                new_tree.root = self.parent.parent.root
                new_tree.searchKey = self.parent.parent.searchKey
                new_tree.parent = self
                temp_tree = self.left_child
                self.left_child = new_tree
                new_tree.right_child = temp_tree
                if new_tree.right_child:
                    new_tree.right_child.parent = new_tree

                if case==3:
                    if self.parent.parent.left_child.right_child and self.parent.parent.left_child.right_child.red:
                        self.parent.parent.root = self.parent.parent.left_child.right_child.root
                        self.parent.parent.searchKey = self.parent.parent.left_child.right_child.searchKey
                        new_tree.left_child = self.parent.parent.left_child.right_child.right_child
                        if new_tree.left_child:
                            new_tree.left_child.parent = new_tree
                        self.parent.parent.left_child.right_child = self.parent.parent.left_child.right_child.left_child
                        if self.parent.parent.left_child.right_child:
                            self.parent.parent.left_child.right_child.parent = self.parent.parent.left_child

                    else:
                        new_tree.left_child = self.parent.parent.left_child.right_child
                        if new_tree.left_child:
                            new_tree.left_child.parent = new_tree
                        self.parent.parent.root = self.parent.parent.left_child.root
                        self.parent.parent.searchKey = self.parent.parent.left_child.searchKey
                        self.parent.parent.left_child = self.parent.parent.left_child.left_child
                        self.parent.parent.left_child.parent = self.parent.parent
                        self.parent.parent.left_child.red = False

                else:
                    if self.parent.parent.left_child.right_child.right_child and self.parent.parent.left_child.right_child.right_child.red:
                        self.parent.parent.root = self.parent.parent.left_child.right_child.right_child.root
                        self.parent.parent.searchKey = self.parent.parent.left_child.right_child.right_child.searchKey
                        new_tree.left_child = self.parent.parent.left_child.right_child.right_child.right_child
                        if new_tree.left_child:
                            new_tree.left_child.parent = new_tree
                        self.parent.parent.left_child.right_child.right_child = self.parent.parent.left_child.right_child.right_child.left_child
                        if self.parent.parent.left_child.right_child.right_child:
                            self.parent.parent.left_child.right_child.right_child.parent = self.parent.parent.left_child.right_child

                    else:
                        new_tree.left_child = self.parent.parent.left_child.right_child.right_child
                        if new_tree.left_child:
                            new_tree.left_child.parent = new_tree
                        self.parent.parent.root = self.parent.parent.left_child.right_child.root
                        self.parent.parent.searchKey = self.parent.parent.left_child.right_child.searchKey
                        self.parent.parent.left_child.right_child = self.parent.parent.left_child.right_child.left_child
                        self.parent.parent.left_child.right_child.parent = self.parent.parent.left_child
                        self.parent.parent.left_child.right_child.red = False
        return (True,True)

    def check_siblings(self):
        """
        checked of er siblings bestaan die kunnen delen met de huidige 2 knoop
        - geen invoerparameters
        - geen uitvoerparameters
        - geen preconditie
        - geen postconditie
        """
        if self.parent.right_child==self: #indien we in de rechterkind van de parent zitten
            if self.parent.is2Node(): #indien de parent A een 2-knoop is
            #     A  we zitten in C
            #    / \
            #   B   C
                if self.parent.left_child and not(self.parent.left_child.is2Node()): #indien de sibling B geen 2 knoop is
                    return self.distribute(1) #redistribute case=1
                else:
                    return (False,1) #return false voor merge geval

            elif self.parent.is3Node(): #indien de parent A een 3 knoop is
            #     A  we zitten in C
            #    / \
            #   B   C
            #  / \
            # E   D
                if self.parent.left_child and self.parent.left_child.red: #indien B rood is
                    if self.parent.left_child.right_child and not(self.parent.left_child.right_child.is2Node()): #indien D geen 2 knoop is
                        return self.distribute(2) #redistribute case=2
                    else:
                        return (False,2) #return false voor merge geval

                else: #we zitten in D en zoeken ofdat E kan delen
                    if not(self.parent.left_child.is2Node()): #indien E geen knoop is
                        return self.distribute(1) #redistribute case=1
                    elif self.parent.red and self.parent.parent and self.parent.parent.left_child and self.parent.parent.left_child==self.parent and self.parent.parent.right_child and not(self.parent.parent.right_child.is2Node()): #we zitten in D en zoeken ofdat C kan delen
                        return self.distribute(3) #redistrivut4e case=3
                    else:
                        return (False,1) #return false voor merge geval

            elif self.parent.is4Node():
            #     A  we zitten in D
            #    / \
            #   B   C
            #  / \ / \
            # E  D F  Y
                if self.parent.left_child and not(self.parent.left_child.is2Node()): #indien E geen 2 knoop is
                    return self.distribute(1) #redistribute case=1
                else:
                    if self.parent.parent and self.parent.parent.left_child and self.parent.parent.left_child==self.parent:
                        if self.parent.parent.right_child and self.parent.parent.right_child.left_child and not(self.parent.parent.right_child.left_child.is2Node()): #indien F geen 2 knoop is
                            return self.distribute(4) #redistribute case=4
                    return (False,1) #return false voor merge geval

        else: #spiegeling ten opzichte van geval bij self.parent.right_child==self
            if self.parent.is2Node():
                if self.parent.right_child and not(self.parent.right_child.is2Node()):
                    return self.distribute(1)
                else:
                    return (False,1)

            elif self.parent.is3Node():
                if self.parent.right_child and self.parent.right_child.red:
                    if self.parent.right_child.left_child and not(self.parent.right_child.left_child.is2Node()):
                        return self.distribute(2)
                    else:
                        return (False,2)

                else:
                    if self.parent.right_child and not(self.parent.right_child.is2Node()):
                        return self.distribute(1)
                    elif self.parent.red and self.parent.parent and self.parent.parent.right_child and self.parent.parent.right_child==self.parent and self.parent.parent.left_child and not(self.parent.parent.left_child.is2Node()):
                        return self.distribute(3)
                    else:
                        return (False,1)

            elif self.parent.is4Node():
                if self.parent.right_child and not(self.parent.right_child.is2Node()):
                    return self.distribute(1)
                else:
                    if self.parent.parent.right_child and self.parent.parent.right_child==self.parent:
                        if self.parent.parent.left_child and self.parent.parent.left_child.right_child and not(self.parent.parent.left_child.right_child.is2Node()):
                            return self.distribute(4)
                    return (False,1)

    def deleteItem(self,searchKey,check_key=True,findsuccesor=False):
        """
        delete item met bepaalde searchKey van de boom
        invoerparameters:
            searchKey (int): key van de te verwijderen item
        uitvoerparameters:
            succes (bool): True indien de item verwijderd is, anders false
        - geen preconditie
        postconditie:
            item met searchKey=searchKey wordt verwijderd
        """

        was_root = self.parent is None
        def fix_root():
            """
                P              R
               / \\    =>     / \\
              R   z          P   z
             / \\           / \\
            x   y          x   y


                P              R
               / \\    =>     / \\
              z   R          z   P
                 / \\           / \\
                y   x          y   x
            """
            if not was_root:
                return # wasn't root
            R = self
            P = self.parent
            if P is None:
                return # already root
            P.root, R.root = R.root, P.root
            P.searchKey, R.searchKey = R.searchKey, P.searchKey
            if R is P.left_child:
                x, y, z = R.left_child, R.right_child, P.right_child
                P.left_child = x
                if x:
                    x.parent = P
                P.right_child = y
                if y:
                    y.parent = P
                R.right_child = z
                if z:
                    z.parent = R
                R.left_child = P
                P.parent = R
                R.parent = None
            else:
                x, y, z = R.right_child, R.left_child, P.left_child
                P.right_child = x
                if x:
                    x.parent = P
                P.left_child = y
                if y:
                    y.parent = P
                R.left_child = z
                if z:
                    z.parent = R
                R.right_child = P
                P.parent = R
                R.parent = None


        if check_key: #check eerst ofdat de item bestaat voor het deleten
            if not(self.retrieveItem(searchKey)[1]):
                fix_root()
                return False

        if self.parent and not(self.red): #check alleen nodes die zwart zijn (rode nodes zitte in dezelfde knoop)
            if self.is2Node(): #indien de huidige knoop een 2 knoop is
                self.make3Node4Node() #check voor siblings en merge geval

        if searchKey==self.searchKey: #indien de te verwijderen item gevonden is
            if not(self.right_child): #check of het een inordersuccesor heeft
                if not(self.left_child): #indien het ook geen linkerkind heeft = blad

                    if not(self.parent): #indien het ook geen parent heeft
                        self.__init__() #wis de hele boom (het bevat 1 node hier)

                    else: #de te verwijdern item zit in een blad
                        if self.parent.left_child==self:
                            self.parent.left_child = None
                        else:
                            self.parent.right_child = None

                else: #de te verwijderen item heeft nog een linkerkind = shift de nodes
                    self.root = self.left_child.root
                    self.searchKey = self.left_child.searchKey
                    self.right_child = self.left_child.right_child
                    self.left_child = self.left_child.left_child #wijzig self.red?

            else: #indien er een inordersuccesor bestaat
                node = self.right_child.deleteItem(searchKey,check_key=False,findsuccesor=True) #vind de inordersuccesor

                if node!=True: #indien de terugwaarde een node is
                    temp = self.root
                    self.root = node.root #swap de root met de inordersuccesor
                    self.searchKey = node.searchKey #swap de searchKey met de inordersuccesor

                    node.root = temp
                    node.searchKey = searchKey #stel de searchKey van de inordersuccesor gelijk aan de gezochte key
                    ret = node.deleteItem(searchKey,check_key=False) #run recursief de delete op de inordersuccesor
                    fix_root()
                    return ret
            fix_root()
            return True

        else: #indien de item niet gevonden is
            if searchKey < self.searchKey: #indien de searchKey van de te verwijderen item kleiner is dan de searchKey van de huidige knoop
                if self.left_child: #indien de linkerkind bestaat
                    ret = self.left_child.deleteItem(searchKey,findsuccesor=findsuccesor,check_key=False) #run recursief de delete op de linkerkind van de huidige knoop
                    fix_root()
                    return ret
                elif findsuccesor: #indien de parameter 'findsuccessor' op true staat (maw we zijn aan het zoeken naar de inordersuccesor)
                    fix_root()
                    return self #return de inordersuccesor
                else:
                    fix_root()
                    return False #item is niet gevonden

            else: #indien de searchKey van de te verwijderen item groter is dan de searchKey van de huidige knoop
                if self.right_child: #indien de rechterkind bestaat
                    ret = self.right_child.deleteItem(searchKey,check_key=False) #run recursief de delete op de rechterkind van de huidige knoop
                    fix_root()
                    return ret
                else:
                    fix_root()
                    return False #item is niet gevonden

class RedBlackTreeTable:
    def __init__(self):
        self.data_structure = RedBlackTree()

    def tableIsEmpty(self):
        return self.data_structure.isEmpty()

    def tableLength(self):
        return str(self.data_structure.save()).count("{")

    def tableInsert(self,newItem):
        instance = RedBlackTree()
        instance.root = newItem.getValue()
        instance.searchKey = newItem.getKey()
        return self.data_structure.insertItem(instance)

    def tableRetrieve(self,searchKey):
        return self.data_structure.retrieveItem(searchKey)

    def traverseTableYielding(self):
        return self.data_structure.inorderYielding()

    def traverseTable(self,k):
        return self.data_structure.inorderTraverse(k)

    def save(self):
        return self.data_structure.save()

    def load(self,d):
        return self.data_structure.load(d)

    def tableDelete(self,searchKey):
        return self.data_structure.deleteItem(searchKey)
