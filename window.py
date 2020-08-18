# I want to move all of my rendering code to something independent, that I can use for different games.
# It's gonna be a wrapper around some other stuff; all that's needed to display a screen and draw and place.

"""
Viewport takes the player's GameMap and X, Y coordinates and displays them. Things we need to tie into it:
1. Entities.
2. Walls, floors.
(Walls, floors are kinds of entities honestly. But we do want to distinguish floors, probably.)

They're a type of Entity: always passable, have a display tile and the lowest possible RENDER LAYER.
Passing over them can have effects.

render_entity:
    Entities define their own methods about what to render?
    Or better: have each entity have a "tile_id" and render those according to the order.
    Might want to account for compound objects, which span multiple tiles (or just make those into 4 Entities, which all die if one of them dies.
        CompoundEntity, extension of Entity.

Screen resizing:
Have a maximum size, center it automatically.
    On each screen resize event, recalculate draw origin.
    Add a pretty border.
    If trying to resize less than the full size, just stop it.
"""

class Screen:
    def __init__(self, context, console, min_width: int, min_height: int):
        self.context = context
        self.console = console
        self.min_width = min_width
        self.min_height = min_height

        self.tileset = None

    
class Renderer:
    def render_entity(entity: Entity, x: int, y: int):
        pass
