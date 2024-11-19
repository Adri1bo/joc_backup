import streamlit.components.v1 as components

_component_func = components.declare_component(
    "sidebar",
    path="./sidebar"
)

def sidebar_events(aDic, aAliments, aHabitatge, aOci, aTransport, aHabitatgeBlock, aHabitatgeComprat, aTransportComprat):
    component_value = _component_func(aDic=aDic, aAliments = aAliments, aHabitatge = aHabitatge, aOci = aOci, aTransport = aTransport, aHabitatgeBlock = aHabitatgeBlock, aHabitatgeComprat = aHabitatgeComprat, aTransportComprat = aTransportComprat)
    return component_value
