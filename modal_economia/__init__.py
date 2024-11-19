import streamlit.components.v1 as components

_component_func = components.declare_component(
    "modal_economia",
    path="./modal_economia"
)

def modal_economia_events(aJugador):
    component_value = _component_func(aJugador = aJugador)
    return component_value