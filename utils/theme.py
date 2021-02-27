theme_content = {
    "TCombobox":{
        "map": {
            "backgound": [("readonly", "white")]
        }
    },

    "TProgressbar": {
        "configure": {
            "foreground": "brown",
            "background": "brown",
        }
    },

    "TNotebook.Tab": {
        "configure": {
            "padding": [5, 2], # [space beetwen text and horizontal tab-button border, space between text and vertical tab_button border]
        },
        "map": {
            "expand": [("selected", [0, 10, 10, 0])] # [expanse of text]
        }
    },

    "TButton": {
        "configure": {
            "foreground": "brown4",
            "backgound": "white"
            },
        "map": {
            "background": [("active", "#ff0000"), ("disabled", "#f0f0f0")]
        }
    }
}

def theme():
    return theme_content
