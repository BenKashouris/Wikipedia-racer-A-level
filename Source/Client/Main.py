from Pages import pages  # Import a tuple of the pages
import GUIController  # Import the multipage root widget
import Commands

IP = "192.168.1.105"

if __name__ == "__main__":
    x = GUIController.GUIController(pages)
    try: 
        Commands.connect_to_server(IP, 6677)
    except Exception as e:
        x.message_box("""A error occured when connecting to server please try again later \nError message: {0}""".format(e))
    x.attributes('-fullscreen', True)
    x.show_page("LogInPage") 
    x.mainloop()
