from flet import *
import sqlite3


deviceWidth = 360
deviceHeight = 720
# Create SQLite database and a table
def init_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()


# Initialize the database
init_db()

# Define the Flet app
def main(page:Page):
    page.title = "Flet CRUD with SQLite"
    page.window_width = deviceWidth
    page.window_height = deviceHeight
    page.window_always_on_top = True
    page.window_maximizable = False
    page.theme_mode = ThemeMode.LIGHT
    page.scroll = ScrollMode.ADAPTIVE
    page.theme = Theme(color_scheme_seed='green')
    
    
    def view_pop(view):
        page.views.pop()
        page.go(page.route)
        page.update()
        
    def route_change(route):
        page.views.clear()
        page.views.append(
            pages[page.route]
            
        )
        page.update()
    
    
    # Add a new item to the database
    def add_item(name):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        if name: 
            c.execute("INSERT INTO items (name) VALUES (?)", (name,))
        else:
           
            page.close_bottom_sheet() 
            page.update()
        conn.commit()
        conn.close()

    # Get all items from the database
    def get_items():
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute("SELECT * FROM items")
        items = c.fetchall()
        conn.close()
        return items

    # Update an item in the database
    def update_item(id, name):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute("UPDATE items SET name = ? WHERE id = ?", (name, id))
        conn.commit()
        conn.close()

    # Delete an item from the database
    def delete_item(id):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute("DELETE FROM items WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    def load_items():
        items = get_items()
        items_list.controls.clear()
        for item in items:
            items_list.controls.append(
                Row([
                    
                    Text(value=item[1],overflow=TextOverflow.ELLIPSIS,width=200,no_wrap=False),
                    Row([
                        IconButton(
                        icons.EDIT, on_click=lambda e, id=item[0]: on_edit_item(id)),
                    
                    IconButton(
                        icons.DELETE, on_click=lambda e, id=item[0]: on_delete_item(id))
                    ])
                    
                ],alignment=MainAxisAlignment.SPACE_BETWEEN, height=40
            ))
        page.close_bottom_sheet()
        page.update()

    def on_add_item(e):
        page.close_bottom_sheet()
        add_item(input_name.value)
        input_name.value = ""
        load_items()

    def on_edit_item(id):
        item = next((i for i in get_items() if i[0] == id), None)
        if item:
            input_name.value = item[1]
            add_button.text = "Update"
            add_button.on_click = lambda e: on_update_item(id)
        page.show_bottom_sheet(bottom_sheet=bs)
        page.update()

    def on_update_item(id):
        update_item(id, input_name.value)
        input_name.value = ""
        add_button.text = "Add"
        add_button.on_click = on_add_item
        load_items()

    def on_delete_item(id):
        delete_item(id)
        load_items()

    input_name = TextField(label="Item name",border=InputBorder.UNDERLINE)
    add_button = ElevatedButton(text="Add",on_click=on_add_item)
    items_list = Column(height=500,scroll=ScrollMode.AUTO)
    text = Text('Item',weight=FontWeight.W_700 ,size=25,text_align=TextAlign.CENTER)

    load_items()

    
    landing = Column(
        [
           Container(
               content=Text(value='Welcome to a CRUD app with SQLite',
                text_align=TextAlign.CENTER,size=17,weight=FontWeight.W_900,color='white'
                ),width=deviceWidth,bgcolor="green",height=deviceHeight-9,
               alignment=alignment.center,on_click=lambda _: page.go('/home')
           )
        ],expand=1,width=deviceWidth,
        
    )
    
    bs = BottomSheet(
        content= Container(
            content= Column(
                [
                    text,input_name,add_button
                ],height=160,alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER
            ),padding=20
        )
    )

    actBtn = ElevatedButton(
        'Add item', on_click=lambda _: page.show_bottom_sheet(bottom_sheet=bs)
    )
    
    crudPage = Column(
        [
            items_list,actBtn
        ]
    )
    
    ap = AppBar(
        leading=IconButton(icon=icons.ARROW_BACK, on_click=lambda _: page.go('/')),
        title= Text('CRUD HOME'),
        actions=[IconButton(icon=icons.SETTINGS)]
    )
    
    pages = {
        '/': View( "/", [landing,], padding=0,),
        '/home': View( "/home", [crudPage],padding=8, appbar=ap), # type: ignore
    }
    


        
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    


app(target=main)

