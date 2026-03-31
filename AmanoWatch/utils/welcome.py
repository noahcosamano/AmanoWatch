def welcome():
    # I would like to make welcome message print better, looks sloppy at the moment
    print("\n" + "="*40)
    print("            NIDS CLI INTERFACE")
    print("="*40)

    print("\nAvailable Commands:\n")

    print("  view [protocol | port] -wait=[ms]")
    print("    • View filtered traffic in real time")
    print("    • Examples:")
    print("        view tcp -wait=500")
    print("        view 80  -wait=500")

    print("\n  exit")
    print("    • Exit the program")

    print("\n" + "="*40 + "\n")