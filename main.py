import pystray
import flet as ft
from PIL import Image

# Load the image to be displayed in the tray
tray_image = Image.open("icon.png")
p: ft.Page  # Global variable for the Flet page

def exit_app(icon, query):
    """Handle exit action from the tray icon."""
    button_clicked(None)  # Trigger a button click event for feedback
    icon.stop()  # Stop the tray icon loop/display
    p.window.destroy()  # Close the Flet window
    print("The App was closed/exited successfully!")

def other_item_clicked(icon, query):
    """Handle clicks on non-default tray menu items."""
    button_clicked(None)  # Trigger a button click event for feedback
    print("A tray option button was pressed.")

def default_item_clicked(icon, query):
    """Show the Flet window when the default tray item is clicked."""
    icon.visible = True
    p.window.skip_task_bar = False  # Ensure the window shows on the taskbar
    p.window.visible = True  # Make the window visible
    p.window.focused = True  # Bring the window to focus
    p.window.minimized = False  # Restore window if minimized
    p.update()  # Update the page to reflect changes
    print("Tray button was pressed.")

def menu_item_clicked(icon, query):
    """Handle menu item clicks from the tray icon."""
    if str(query) == "Open App":
        default_item_clicked(icon, query)  # Reuse logic to show the app
    elif str(query) == "Close App":
        exit_app(icon, query)  # Reuse logic to exit the app
    else:
        print("A Non-Default button was pressed.")

def my_setup(icon):
    """Initial setup for the tray icon."""
    icon.visible = True  # Ensure the tray icon is visible at startup

# Define the tray icon with its menu and actions
tray_icon = pystray.Icon(
    name="Test",
    icon=tray_image,
    title="Flet in tray",
    menu=pystray.Menu(
        pystray.MenuItem("Open App", default_item_clicked, default=True),  # Default menu item
        pystray.MenuItem("Go Nowhere 1", other_item_clicked),
        pystray.MenuItem("Go Nowhere 2", other_item_clicked),
        pystray.MenuItem("Close App", exit_app)
    ),
    visible=True,
)

def button_clicked(e):
    """Handle button click events in the Flet app."""
    p.add(ft.Text("Button event handler was triggered!"))  # Feedback to user

def on_window_event(e):
    """Handle window events (minimize, restore, close)."""
    if e.data == "minimize":
        p.window.minimized = True  # Minimize the window
    elif e.data == "restore":
        p.window.skip_task_bar = False  # Show on taskbar
        p.window.visible = True  # Restore visibility
        p.window.focused = True  # Bring window to focus
    elif e.data == "close":
        p.window.skip_task_bar = True  # Remove from taskbar
        p.window.visible = False  # Hide the window

    p.update()  # Update the page to reflect changes

def main(page):
    """Main function to set up the Flet app."""
    global p  # Make the page variable accessible globally
    p = page

    page.window.on_event = on_window_event  # Set up window event handling
    page.window.prevent_close = True  # Prevent direct window closing
    page.title = "Flet in the sys-tray"  # Set window title

    # Add UI elements to the Flet page
    page.add(
        ft.Text("- Minimize this app to see in the tray. \n"
                "- Then press the flet tray icon button to make the window visible again."),
        ft.ElevatedButton("Button with 'click' event", on_click=button_clicked)
    )

# Start the tray icon in a detached mode to integrate with the Flet app
tray_icon.run_detached(setup=my_setup)

# Run the Flet app
ft.app(target=main)
