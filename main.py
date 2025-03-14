from gui.layout import set_custom_styles
from gui.navigation import render_sidebar, render_page

def main():
    set_custom_styles()

    selected_page = render_sidebar()
    render_page(selected_page)


if __name__ == "__main__":
    main()