import sys
sys.path.append( '..' )

import inspect
import json

from kivy.adapters.dictadapter import DictAdapter
from kivy.adapters.listadapter import ListAdapter
from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.popup import Popup
from kivy.uix.selectableview import SelectableView
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

import time

Builder.load_file( 'progrid.kv' )

"""
Inspired by DevExpress CxGrid...

-- Features --

Rows :
    - Filtering
    - Sorting
    - Grouping ( not yet )

Columns :
    - Filtering
    - Sorting
"""
class ProGrid( FloatLayout ) :

    """
    Data to display, array of dictionaries.
    """
    data = ListProperty( [] )

    """
    Label for any column.
    """
    headers = DictProperty( {} )

    """
    List of columns to show, ordered.
    """
    columns = ListProperty( [] )

    """
    Dictionary containing functions used to filter data.
    """
    row_filters = DictProperty( {} )

    """
    List of sort rules to use.
    Only one rule is accepted in the current implementation.

    Example :

    [ ['surname','asc'], ['name','asc'], ['birth','desc'] ]

    Curzel  Federico    04/08/2014
    Curzel  Federico    01/04/2014
    Rossi   Mario       01/04/2014
    """
    row_sorting = ListProperty( [] )


    """
    Other properties of less interest...
    """

    header  = ObjectProperty( None )
    content = ObjectProperty( None )
    footer  = ObjectProperty( None )

    text_color = ListProperty( [ 0, 0, 0, .9 ] )
    grid_color = ListProperty( [ 0, 0, 0, .5 ] )
    grid_width = NumericProperty( 1 )

    content_font_name = StringProperty( 'font/Roboto-Light.ttf' )
    header_font_name = StringProperty( 'font/Roboto-Medium.ttf' )
    font_size = NumericProperty( 14 )
    row_height = NumericProperty( 28 )
    header_height = NumericProperty( 40 )
    footer_height = NumericProperty( 15 )

    _data = ListProperty( [] )

    header_background_color = ListProperty( [ .8, .8, .8, 1 ] )
    content_background_color = ListProperty( [ .93, .93, .93, 1 ] )
    footer_background_color = ListProperty( [ .8, .8, .8, 1 ] )


    def __init__( self, **kargs ) :
        kargs['orientation'] = 'vertical'
        super( ProGrid, self ).__init__( **kargs )

        #Inner layouts
        """
        self.content = GridLayout( 
            size_hint=(1,None), pos=(0,40), \
            cols=1, \
            background_color=self.content_background_color
        )
        self.add_widget( self.content ) 
        self.header  = BoxLayout( size_hint=(1,.1), pos=(0,0), background_color=self.header_background_color )
        self.footer  = BoxLayout( size_hint=(1,.1), background_color=self.footer_background_color )
        self.add_widget( self.header ) 
        self.add_widget( self.footer ) 
        """
        
        #Bindings...
        self.bind( data=self._render )
        self.bind( font_size=lambda o,v: self.setter('row_height')(o,v*2) )

        #Binding occurs after init, so we need to force first setup
        self._render( self.data )

    """
    Will re-render the grid.
    """
    def _render( self, data ) :

        self._setup_data( data )

        #Content
        self.content.clear_widgets()
        self.content.height = 0

        for line in self._data :
            row = self._gen_row( line, self.row_height, self.content_font_name )
            self.content.add_widget( row )
            self.content.height += row.height

        #Header
        self.header = self._gen_row( self.headers, self.header_height, self.header_font_name )

        #Footer
        ...
        

    """
    Will generate a single row.
    """
    def _gen_row( self, line, row_height, font_name ) :
        b = BoxLayout( height=row_height, orientation='horizontal' )

        for column in self.columns :
            lbl = Label( 
                text=line[column], color=self.text_color, \
                font_name=font_name, font_size=self.font_size
            )
            b.add_widget( lbl )

        return b


    """
    Will filter and order data rows.
    """
    def _setup_data( self, data ) :

        #Filtering
        temp = filter( self._validate_line, data )

        #Sorting
        field, mode = self.row_sorting[0]
        reverse = False if mode == 'asc' else True
        self._data = sorted( temp, key=lambda o: o[field], reverse=reverse )
         

    """
    Will apply given filters.
    """    
    def _validate_line( self, line ) :
        for k in self.row_filters :
            if not self.row_filters[k]( line[k] ) :
                return False
        return True



