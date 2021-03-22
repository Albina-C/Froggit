"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Each lane is like its own level. It has hazards (e.g. cars) that the frog has to make
it past.  Therefore, it is a lot easier to program frogger by breaking each level into
a bunch of lane objects (and this is exactly how the level files are organized).

You should think of each lane as a secondary subcontroller.  The level is a subcontroller
to app, but then that subcontroller is broken up into several other subcontrollers, one
for each lane.  That means that lanes need to have a traditional subcontroller set-up.
They need their own initializer, update, and draw methods.

There are potentially a lot of classes here -- one for each type of lane.  But this is
another place where using subclasses is going to help us A LOT.  Most of your code will
go into the Lane class.  All of the other classes will inherit from this class, and
you will only need to add a few additional methods.

If you are working on extra credit, you might want to add additional lanes (a beach lane?
a snow lane?). Any of those classes should go in this file.  However, if you need additional
obstacles for an existing lane, those go in models.py instead.  If you are going to write
extra classes and are now sure where they would go, ask on Piazza and we will answer.

Albina Chowdhury (ac2523)
December 21, 2020
"""
from game2d import *
from consts import *
from models import *

# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.

class Lane(object):         # You are permitted to change the parent class if you wish
    """
    Parent class for an arbitrary lane.

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE

    #Attribute _gtile: contains GTile object for lanes
    # Invariant:is a GTile object

    # Attribute _objs: obstacle images within each lane
    # Invariant: list of GImage objects

    # Attribute _speed: How fast the objects are moving
    # Invariants: Object speed from JSON

    # Attribute _speed: How fast the objects are moving
    # Invariants: Object speed from JSON

    # Attribute _buffer: distance that all objects are allowed to go offscreen
    # Invariants: offscreen fron json


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getGtile(self):
        """
        Returns GTile object
        """
        return self._gtile

    def getObjs(self):
        """
        Returns list of GImage objects
        """
        return self._objs


    # INITIALIZER TO SET LANE POSITION, BACKGROUND,AND OBJECTS
    def __init__(self,s, h, w,l,b,json,lane):
        """
        Initializes each lane within each level.

        This method initializes each attribute needed in order to display the
        game. It must be called by Level in order make each level work.

        This method should make sure that all of the attributes satisfy the
        given invariants.

        parameter json: json that stores information about game objects
        precondition: json string

        parameter s: source of GTile or GImage objects
        precondition: image file

        parameter h: height of an image source
        precondition: int or float

        parameter w: width of an image source
        precondition: int or float

        parameter l: left coordinate of where Gtile or GImage object is placed
        precondition: int or float

        parameter b: bottom coordinate of where Gtile or GImage object is placed
        precondition: int or float

        parameter lane: lane position
        precondition: int or float
        """

        if 'speed' in json['lanes'][lane]:
            self._speed = json['lanes'][lane]["speed"]
        else:
            self._speed =0

        self._gtile= GTile(left=l,bottom=b,width=w,height=h,source=s)
        self._objs = []


        if 'objects' in json['lanes'][lane]:
            for x in json['lanes'][lane]['objects']:
                z = GImage(source=x['type']+'.png',
                x=x['position']*GRID_SIZE+(GRID_SIZE/2),y=b+(GRID_SIZE/2))
                if self._speed<0:
                    z.angle = 180
                self._objs.append(z)
        self._buffer = json['offscreen']


    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def draw(self, the_view):
        """
        Method that Draws the game objects to the view.

        With this function, the levels contain all necessary images in order to
        function.

        parameter the_view: window that objects are drawn on
        precondition: GAMEAPP attribute
        """
        self._gtile.draw(the_view)
        for k in self._objs:
            k.draw(the_view)


    def update(self,dt,input):
        """
        updates the levels in order for the frog and obstacles on the lanes
        to move.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: last update
        Precondition: last state or update method called
        """
        for movement in self._objs:
            if movement.x<0-self._buffer*GRID_SIZE:
                m = self._speed*dt
                movement.x=self._gtile.width +self._buffer*GRID_SIZE
                movement.x+=m
            elif movement.x>self._gtile.width +self._buffer*GRID_SIZE:
                m = self._speed*dt
                movement.x=0-self._buffer*GRID_SIZE
                movement.x+=m
            else:
                m = self._speed*dt
                movement.x+=m


class Grass(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a 'safe' grass area.

    You will NOT need to actually do anything in this class.  You will only do
    anything with this class if you are adding additional features like a snake
    in the grass (which the original Frogger does on higher difficulties).
    """
    pass
    # ONLY ADD CODE IF YOU ARE WORKING ON EXTRA CREDIT EXTENSIONS.


class Road(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a roadway with cars.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, roads are different
    than other lanes as they have cars that can kill the frog. Therefore, this class
    does need a method to tell whether or not the frog is safe.
    """

    # DEFINE ANY NEW METHODS HERE

class Water(Lane):
    """
    A class representing a waterway with logs.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, water is very different
    because it is quite hazardous. The frog will die in water unless the (x,y) position
    of the frog (its center) is contained inside of a log. Therefore, this class needs a
    method to tell whether or not the frog is safe.

    In addition, the logs move the frog. If the frog is currently in this lane, then the
    frog moves at the same rate as all of the logs.
    """
    pass

    # DEFINE ANY NEW METHODS HERE


class Hedge(Lane):
    """
    A class representing the exit hedge.

    This class is a subclass of lane because it does want to use a lot of the features
    of that class. But there is a lot more going on with this class, and so it needs
    several more methods.  First of all, hedges are the win condition. They contain exit
    objects (which the frog is trying to reach). When a frog reaches the exit, it needs
    to be replaced by the blue frog image and that exit is now "taken", never to be used
    again.

    That means this class needs methods to determine whether or not an exit is taken.
    It also need to take the (x,y) position of the frog and use that to determine which
    exit (if any) the frog has reached. Finally, it needs a method to determine if there
    are any available exits at all; once they are taken the game is over.

    These exit methods will require several additional attributes. That means this class
    (unlike Road and Water) will need an initializer. Remember to user super() to combine
    it with the initializer for the Lane.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE

    # Attribute _frogHedge: safe frogs that appear when frog goes on lilly pad.
    # Invariants: list of GImages


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getFrogHedge(self):
        """
        Returns list of GImage objects
        """
        return self._frogHedge
    def setFrogHedge(self,value):
        """
        sets the list of GImage objects.

        parameter value: GImage object of FROG_SAFE
        precondition: GImage object
        """
        bool=False
        for frog in self._frogHedge:
            if frog.x == value.x and frog.y == value.y:
                bool=True

        if bool == False:
            self._frogHedge.append(value)

    # INITIALIZER TO SET ADDITIONAL EXIT INFORMATION

    def __init__(self,s, h, w,l,b,json,lane):
        """
        Initializes each lane within each level.

        This method initializes each attribute needed in order to display the
        game. It must be called by Level in order make each level work.

        This method should make sure that all of the attributes satisfy the
        given invariants.

        parameter json: json that stores information about game objects
        precondition: json string

        parameter s: source of GTile or GImage objects
        precondition: image file

        parameter h: height of an image source
        precondition: int or float

        parameter w: width of an image source
        precondition: int or float

        parameter l: left coordinate of where Gtile or GImage object is placed
        precondition: int or float

        parameter b: bottom coordinate of where Gtile or GImage object is placed
        precondition: int or float

        parameter lane: lane position
        precondition: int or float
        """
        super().__init__(s, h, w,l,b,json,lane)
        self._frogHedge=[]


    # ANY ADDITIONAL METHODS

# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
    def draw(self, the_view):
        """
        Method that Draws the game objects to the view.

        With this function, the levels contain all necessary images in order to
        function.

        parameter the_view: window that objects are drawn on
        precondition: GAMEAPP attribute
        """
        super().draw(the_view)
        if self._frogHedge!=[]:
            for z in self._frogHedge:
                z.draw(the_view)
