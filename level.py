"""
Subcontroller module for Froggit

This module contains the subcontroller to manage a single level in the Froggit game.
Instances of Level represent a single game, read from a JSON.  Whenever you load a new
level, you are expected to make a new instance of this class.

The subcontroller Level manages the frog and all of the obstacles. However, those are
all defined in models.py.  The only thing in this class is the level class and all of
the individual lanes.

This module should not contain any more classes than Levels. If you need a new class,
it should either go in the lanes.py module or the models.py module.

Albina Chowdhury (ac2523)
December 21, 2020
"""
from game2d import *
from consts import *
from lanes  import *
from models import *

# PRIMARY RULE: Level can only access attributes in models.py or lanes.py using getters
# and setters. Level is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Level(object):
    """
    This class controls a single level of Froggit.

    This subcontroller has a reference to the frog and the individual lanes.  However,
    it does not directly store any information about the contents of a lane (e.g. the
    cars, logs, or other items in each lane). That information is stored inside of the
    individual lane objects.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lesson 27 for an example.  This class will be similar to that
    one in many ways.

    All attributes of this class are to be hidden.  No attribute should be accessed
    without going through a getter/setter first.  However, just because you have an
    attribute does not mean that you have to have a getter for it.  For example, the
    Froggit app probably never needs to access the attribute for the Frog object, so
    there is no need for a getter.

    The one thing you DO need a getter for is the width and height.  The width and height
    of a level is different than the default width and height and the window needs to
    resize to match.  That resizing is done in the Froggit app, and so it needs to access
    these values in the level.  The height value should include one extra grid square
    to suppose the number of lives meter.
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE

    # Attribute _width: width of the enitre window for the level object
    # Invariant: is an int >= 0

    # Attribute _height: height of the enitre window for the level object
    # Invariant: is an int >= 0

    # Attribute _lanes: Lanes needed to be drawn
    # Invariant: is a list of Lane objects

    # Attribute: _frog: Frog needed to be drawn
    # Invariant: is a Frog object

    # Attribute _displaytitle: displays the lives text
    # Invariant: GImage object

    # Attribute _lives: displays the frog heads for the lives
    # Invariant: Is a GTile object

    #Attribute _cooldown: controls the speed of the frog
    # Invariant: Is a frog speed


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getWidth(self):
        """
        Returns the width
        """
        return self._width

    def getHeight(self):
        """
        Returns the height
        """
        return self._height

    def getLanes(self):
        """
        Returns the list of lane objects
        """
        return self._lanes

    def getFrog(self):
        """
        Returns frog object
        """
        return self._frog

    def getLives(self):
        """
        Returns the amount of lives (frog heads) remaining
        """
        return self._lives

    # INITIALIZER (standard form) TO CREATE THE FROG AND LANES
    def __init__(self, json):
        """
        Initializes each level within the game.

        This method initializes each attribute needed in order to display the
        game. It must be called by the app in order make each level work.

        This method should make sure that all of the attributes satisfy the
        given invariants.

       parameter json: json that stores information about game objects
       precondition: json string
        """

        self._width = (json['size'][0])*GRID_SIZE

        self._height = (json['size'][1]+1)*GRID_SIZE

        self._makeLane(json)

        self._makeFrog(json)

        self._displayLives()

        self._cooldown = FROG_SPEED


    # UPDATE METHOD TO MOVE THE FROG AND UPDATE ALL OF THE LANES
    def update(self,dt,input,json):
        """
        method that updates the levels in order for the frog and obstacles on
        the lanes to move, according to each state the level is in.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input:
        Precondition: dt is a number (int or float)
        """
        if self._frog==None:
            self._frog = Frog(json["start"][0]*GRID_SIZE+GRID_SIZE//2,
            json['start'][1]*GRID_SIZE+GRID_SIZE//2)
            self._lives.pop()
        self._moveFrog(dt,input)
        for g in self._lanes:
            g.update(dt,input)
        self._frogCar(dt,input)
        self.remainingHedge(dt,input)


    # DRAW METHOD TO DRAW THE FROG AND THE INDIVIDUAL LANES
    def draw(self,the_view):
        """
        Method that Draws the game objects to the view.

        With this function, the levels contain all necessary images in order to
        function.

        parameter the_view: window that objects are drawn on
        precondition: GAMEAPP attribute
        """

        for y in self.getLanes():
            y.draw(the_view)
        if self._frog != None:
            self._frog.draw(the_view)

        for head in self._lives:
            head.draw(the_view)
        self._displaytitle.draw(the_view)

    def remainingHedge(self,dt,input):
        """
        Method that checks whether the amount of FROG_SAFE GImages occuppies
        every exit or lilly pad.
        """
        acc=[]
        fill=True
        for x in self._lanes:
            if isinstance(x,Hedge):
                for object in x.getObjs():
                    if object.source == 'exit.png':
                        acc.append(object)
        if len(acc)==len(x.getFrogHedge()):
            fill = True
            self._frog = None
            return fill
        return False

    def _makeFrog(self,json):
        """
        Helper function that calls Frog class.

        parameter json: json that stores information about game objects
        precondition: json string
        """
        self._frog = Frog(json['start'][0]*GRID_SIZE+GRID_SIZE//2,
        json['start'][1]*GRID_SIZE+GRID_SIZE//2)

    def _makeLane(self,json):
        """
        Helper function that Creates lane objects.

        parameter json: json that stores information about game objects
        precondition: json string

        """
        self._lanes = []

        for lane in range(len(json['lanes'])):
            t= json['lanes'][lane]['type']
            bot = lane*GRID_SIZE
            if json['lanes'][lane]['type'] == 'grass':
                x = Grass(t+'.png',GRID_SIZE,self._width,0,bot, json,lane)
                self._lanes.append(x)
            if json['lanes'][lane]['type'] == 'water':
                x= Water(t+'.png',GRID_SIZE, self._width,0,bot,json,lane)
                self._lanes.append(x)
            if json['lanes'][lane]['type'] == 'road':
                x= Road(t+'.png',GRID_SIZE,self._width,0,bot,json,lane)
                self._lanes.append(x)
            if json['lanes'][lane]['type'] == 'hedge':
                x= Hedge(t+'.png',GRID_SIZE,self._width,0,bot,json,lane)
                self._lanes.append(x)

    def _displayLives(self):
        """
        Helper function that Creates the display of lives.

        """
        self._lives=[]
        for position in range(FROG_LIVES):
            i = GImage(source=FROG_HEAD,width=GRID_SIZE,height=GRID_SIZE,
                x=self._width-(position*GRID_SIZE)-GRID_SIZE,y=self._height-GRID_SIZE/2)
            self._lives.append(i)
        self._displaytitle= GLabel(text= 'Lives',font_name= ALLOY_FONT,
        font_size=ALLOY_SMALL,x=self._width-(5*GRID_SIZE),
        y=self._height-GRID_SIZE/2,linecolor='dark green')

    def _moveFrog(self,dt,input):
        """
        Helper function that helps move the frog throughout the game.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: last update
        Precondition: last state or update method called

        """
        if self._frog !=None:
            frogpos = (self._frog.getX(),self._frog.getY())

            if self._frog.getX()-GRID_SIZE>0:
                self._leftMove(dt,input)

            if self._frog.getX()+GRID_SIZE<self._width:
                self._rightMove(dt,input)

            if self._frog.getY()+GRID_SIZE<self._height-GRID_SIZE/2:
                self._upMove(dt,input)

            if self._frog.getY()-GRID_SIZE>0:
                self._downMove(dt,input)

            if self._frogCollision(frogpos):
                self._frog.setX(frogpos[0])
                self._frog.setY(frogpos[1])

    def _leftArrow(self):
        """
        helper function that controls the movement of the frog if the
        left arrow key is being held down and when the cooldown attribute is
        less than or equal to 0.

        """
        self._frog.setX(self._frog.getX()-GRID_SIZE)
        self._frog.setAngle(FROG_WEST)
        self._cooldown = FROG_SPEED

    def _leftMove(self,dt,input):
        """
        helper function that controls the movement of the frog if the
        left arrow key is being held down.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: last update
        Precondition: last state or update method called

        """
        if input.is_key_down('left'):
            if self._cooldown <= 0:
                self._leftArrow()
            else:
                self._cooldown -= dt

    def _rightArrow(self):
        """
        helper function that controls the movement of the frog if the
        right arrow key is being held down and when the cooldown attribute is
        less than or equal to 0.

        """
        self._frog.setX(self._frog.getX()+GRID_SIZE)
        self._frog.setAngle(FROG_EAST)
        self._cooldown = FROG_SPEED

    def _rightMove(self,dt,input):
        """
        helper function that controls the movement of the frog if the
        right arrow key is being held down.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: last update
        Precondition: last state or update method called

        """
        if input.is_key_down('right'):
            if self._cooldown <= 0:
                self._rightArrow()
            else:
                self._cooldown -= dt

    def _upArrow(self):
        """
        helper function that controls the movement of the frog if the
        up arrow key is being held down and when the cooldown attribute is
        less than or equal to 0.

        """
        self._frog.setY(self._frog.getY()+GRID_SIZE)
        self._frog.setAngle(FROG_NORTH)
        self._cooldown = FROG_SPEED

    def _upMove(self,dt,input):
        """
        helper function that controls the movement of the frog if the
        Up arrow key is being held down.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: last update
        Precondition: last state or update method called

        """
        if input.is_key_down('up'):
            if self._cooldown <= 0:
                self._upArrow()
            else:
                self._cooldown -= dt

    def _downArrow(self):
        """
        helper function that controls the movement of the frog if the
        down arrow key is being held down.

        """
        self._frog.setY(self._frog.getY()-GRID_SIZE)
        self._frog.setAngle(FROG_SOUTH)
        self._cooldown = FROG_SPEED

    def _downMove(self,dt,input):
        """
        helper function that controls the movement of the frog if the
        down arrow key is being held down and when the cooldown attribute is
        less than or equal to 0.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: last update
        Precondition: last state or update method called

        """
        if input.is_key_down('down'):
            if self._cooldown <= 0:
                self._downArrow()
            else:
                self._cooldown -= dt

    def _frogCollision(self,v):
        """
        helper function that checks whether the frog collided with the hedge lane.
        It only allows the frog to go on the hedge lane if it is on a lilly
        pad and creates a GImage object of the safe frog.

        parameter v: tells where the frog is located
        precondition: is the coordinate points of the Frog object

        """
        collide=False
        v = self._frog.getX(),self._frog.getY()
        for lane in self._lanes:
            if isinstance(lane,Hedge):
                if self._frog.collides(lane.getGtile()):
                    collide = True
                    for object in lane.getObjs():
                        if object.contains(v):
                            collide=False
                            if object.source == 'exit.png':
                                r=GImage(source=FROG_SAFE,
                                width=GRID_SIZE,height=GRID_SIZE,
                                x=object.x, y=object.y)
                                lane.setFrogHedge(r)
                                if object.source == 'exit.png' and object.contains(v):
                                    collide=True

        return collide

    def _roadCollision(self):
        """
        helper function that checks whether the frog collided with the road lane.
        It checks whether the frog is on a car object.

        """
        if self._frog!=None:
            collide=False
            r = (self._frog.getX(),self._frog.getY())
            for lane in self._lanes:
                if isinstance(lane,Road):
                    if self._frog.collides(lane.getGtile()):
                        collide = False
                        for object in lane.getObjs():
                            if object.contains(r):
                                collide=True

            return collide

    def _frogCar(self,dt,input):
        """
        helper function that checks if a frog collided with a car object and sets the
        frog object to none, in order to kill the frog.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: last update
        Precondition: last state or update method called

        """
        if self._roadCollision():
            self._frog = None
