"""
Models module for Froggit

This module contains the model classes for the Frogger game. Anything that you
interact with on the screen is model: the frog, the cars, the logs, and so on.

Just because something is a model does not mean there has to be a special class for
it. Unless you need something special for your extra gameplay features, cars and logs
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object.

That is why this module contains the Frog class.  There is A LOT going on with the
frog, particularly once you start creating the animation coroutines.

If you are just working on the main assignment, you should not need any other classes
in this module. However, you might find yourself adding extra classes to add new
features.  For example, turtles that can submerge underneath the frog would probably
need a custom model for the same reason that the frog does.

If you are unsure about  whether to make a new class or not, please ask on Piazza. We
will answer.

Albina Chowdhury (ac2523)
December 21, 2020
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from a lane or level object, then it
# should be a parameter in your method.


class Frog(GImage):         # You will need to change this by Task 3
    """
    A class representing the frog

    The frog is represented as an image (or sprite if you are doing timed animation).
    However, unlike the obstacles, we cannot use a simple GImage class for the frog.
    The frog has to have additional attributes (which you will add).  That is why we
    make it a subclass of GImage.

    When you reach Task 3, you will discover that Frog needs to be a composite object,
    tracking both the frog animation and the death animation.  That will like caused
    major modifications to this class.
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        returns the x-coordinate position of the frog.
        """
        return self.x
    def getY(self):
        """
        returns the y-coordinate position of the frog.
        """
        return self.y
    def setX(self,value):
        """
        sets the x-coordinate position of the frog.

        parameter value: input of the user for the y-coordinate position of the
        frog.
        precondition: int or float
        """
        self.x=value
    def setY(self,value):
        """
        sets the y-coordinate position of the frog.

        parameter value: input of the user for the y-coordinate position of the
        frog.
        precondition: int or float
        """
        self.y=value
    def setAngle(self,value):
        """
        sets the angle of the frog.

        parameter value: input of the user for the y-coordinate position of the
        frog.
        precondition: int or float
        """
        self.angle=value

    # INITIALIZER TO SET FROG POSITION
    def __init__(self,posx,posy):
        """
        Intializes the Frog class and its attributes.

        Parameter posx: The x-coordinate position of the frog.
        precondition: int or float; range within the window object is called in

        Parameter posx: The y-coordinate position of the frog.
        precondition: int or float; range within the window object is called in
        """
        super().__init__(source = FROG_IMAGE, x=posx, y=posy)
        self.angle = FROG_NORTH
    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)


# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
