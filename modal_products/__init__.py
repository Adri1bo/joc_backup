import streamlit.components.v1 as components

_component_func = components.declare_component(
    "modal_products",
    path="./modal_products"
)

def modal_products_events(aDic):
    component_value = _component_func(aDic=aDic)
    return component_value
