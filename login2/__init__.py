import streamlit.components.v1 as components

_component_funct = components.declare_component(
    "login2",
    path="./login2"
)

def login_events2():
    component_value = _component_funct()
    return component_value