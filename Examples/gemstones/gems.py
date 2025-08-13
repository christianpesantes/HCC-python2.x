
#--------------------------------------------
# gems! - regex project
#--------------------------------------------

#--------------
# characters:
#--------------

# A -> amethyst : p -> purple
# D -> diamond  : w -> white
# E -> emerald  : g -> green
# R -> ruby     : r -> red
# S -> sapphire : b -> blue
# T -> topaz    : y -> yellow

#--------------------------------------------


def main():

    # SETUP
    import gemsClass
    game = gemsClass.gems()

    # INTRO
    game.intro()

    # GAME LOOP
    while game.isAlive:
        game.run()

    # EXIT
    print game    
    return


if __name__ == "__main__":
    main()
