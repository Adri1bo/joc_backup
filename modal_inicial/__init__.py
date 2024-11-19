import streamlit.components.v1 as components

_component_func = components.declare_component(
    "modal_inicial",
    path="./modal_inicial"
)

def modal_inicial_events():
    component_value = _component_func()
    return component_value