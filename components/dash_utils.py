import re


def change_props(components, id, prop, value):
    '''Modifie une liste complète de dash components
    en modifiant la propriété prop de chaque composent avec id correspiondant à id.
    id peut être un regex
    '''
    if type(components)!=list:
        components = [components]
    for component in components:
        if type(component)==dict and 'props' in component:
            if component['props'].get('id') and re.match(id, component['props'].get('id')):
                component['props'][prop]=value
            if "children" in component['props']:
                change_props(component['props']['children'], id, prop, value)
    