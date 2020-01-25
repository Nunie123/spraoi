'''
The goal of this excercise is to implement a function that allows you to query the type of 
a keypath in a jsonschema. This function will accept a valid jsonschema 
(https://json-schema.org/specification.html) as dict, a key_path (eg: foo.bar.baz) and 
return the type of the property.

Note:

There are only two fields in the schema you have to pay attention to: properties and definitions.
if the dictionary associated with the field has a field named $ref it means that its refering to 
another schema stored under the top level schema. You have follow the link to get to the actual definition.
For the sake of this excercise you can assume that all values for $ref will start wiht #/<key_path>.
You should see a schema and some assert statements under "Test" section. You should NOT have to change 
anything under the "Test" section. If you can get our code to pass the tests, then it means your function 
works as expected.
Feel free to use whatever libraries you need to use except any libraries that actually allow you to query 
the jsonschema
'''
from typing import Union

def get_type_for_key_path(schema: dict, key_path: str) -> str: 
    key_path_list = key_path.split('.')
    try:                                                                # handle if provided path is inside "properties" or "definitions" attribute.
        final_path_list = generate_path_list(schema, key_path_list)
    except ValueError:
        try:
            properties_key_path_list = ['properties'] + key_path_list
            final_path_list = generate_path_list(schema, properties_key_path_list)
        except ValueError:
            try:
                definitions_key_path_list = ['definitions'] + key_path_list
                final_path_list = generate_path_list(schema, definitions_key_path_list)
            except ValueError:
                return None                                             # return None if path not found.
    data_type = get_value_by_key_path_list(schema, final_path_list + ['type'])
    return data_type
    

def generate_path_list(schema: dict, original_key_path: list) -> list:
    # Resolves internal references in schema into an absolute path.
    current_key_path = list()
    new_key_path = list()
    for i, key in enumerate(original_key_path):     # loop to search for internal references.
        current_key_path.append(key)
        current_value = get_value_by_key_path_list(schema, current_key_path)
        if type(current_value) is dict and '$ref' in current_value.keys():      # handle internal references in the schema.
            referenced_key_path = current_value['$ref'][2:].split('/')
            try:
                get_value_by_key_path_list(schema, referenced_key_path + ['properties'])    # check if referenced path in "properties" atrtribute.
                combined_key_path = referenced_key_path + ['properties'] + original_key_path[i+1:]
            except:
                get_value_by_key_path_list(schema, referenced_key_path + ['definitions'])   # check if referenced path in "definitions" atrtribute.
                combined_key_path = referenced_key_path + ['definitions'] + original_key_path[i+1:]
            new_key_path = generate_path_list(schema, combined_key_path)        # recursion to handle additional references, if any.
            break
    final_key_path = (new_key_path or current_key_path)
    return final_key_path



def get_value_by_key_path_list(schema: dict, key_path: list) -> Union[str, int]:
    #Simple dict lookup with variable path length. Does not follow internal references (throws ValueError). Checks for valid path at every step.
    value = schema.get(key_path[0])
    if value is None:
        raise ValueError()
    if len(key_path) == 1:
        return value
    else:
        new_key_path = key_path[1:]
        return get_value_by_key_path_list(schema=value, key_path=new_key_path)      # recursion to traverse entire path.
        
    
        
    
