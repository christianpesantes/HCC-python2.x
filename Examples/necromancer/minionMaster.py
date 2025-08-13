

if __name__ == "__main__":
    
    # SETUP
    import necroClass
    necromancer = necroClass.necro()

    # INTRO
    necromancer.intro()

    # GAME LOOP
    while necromancer.isAlive:
        necromancer.run()

    # EXIT
    print necromancer

