from engine.property.object import ObjectProperty
from engine.ui.styles.border import Border


class BorderBehavior:

    border      : Border = ObjectProperty( Border(), Border )
    border_hover: Border = ObjectProperty( None, Border )

    def __init__(self, *args, **kwargs):

        border      : Border = kwargs.pop("border", None)
        border_hover: Border = kwargs.pop("border_hover", None)

        super().__init__(*args, **kwargs)
        self.border = border
        self.border_hover = border_hover
