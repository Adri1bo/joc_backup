import streamlit.components.v1 as components

_component_funct = components.declare_component(
    "login",
    path="./login"
)

def login_events():
    component_value = _component_funct()
    return component_value